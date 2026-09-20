import asyncio
import html
import logging

from langchain_core.messages import HumanMessage
from langgraph.graph.message import add_messages
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from app.agent import graph
from app.conversation.manager import ConversationManager
from app.gateway.telegram.parser import parse_update
from app.gateway.telegram.sanitizer import escape_telegram_html
from app.integrations.manager import manager as integration_manager
from app.tools.browser.executor import register_approval_callback

logger = logging.getLogger(__name__)


def split_message(text: str, max_length: int = 4096) -> list[str]:
	"""Splits a message into chunks of up to max_length characters.

	Tries to split at newlines or spaces to avoid cutting words/sentences in
	half.
	"""
	if len(text) <= max_length:
		return [text]

	chunks = []
	text_to_chunk = text
	while text_to_chunk:
		if len(text_to_chunk) <= max_length:
			chunks.append(text_to_chunk)
			break

		# Try to split at a newline near max_length
		split_idx = text_to_chunk.rfind("\n", 0, max_length)
		if (
			split_idx <= 0 or split_idx < max_length * 0.7
		):  # If no newline or too far back, try space
			split_idx = text_to_chunk.rfind(" ", 0, max_length)
		if (
			split_idx <= 0 or split_idx < max_length * 0.7
		):  # If still no space or too far back, hard split
			split_idx = max_length

		chunks.append(text_to_chunk[:split_idx].rstrip())
		text_to_chunk = text_to_chunk[split_idx:].lstrip()
	return chunks


class TelegramMessageHandler:
	async def _handle_gmail_command(self, message, text: str) -> None:
		parts = text.split(maxsplit=1)
		if len(parts) == 1:
			res = integration_manager.connect("gmail")
			if res.get("connected"):
				status = integration_manager.status("gmail")
				email = status.get("email") or "unknown"
				await message.reply_text(
					f"✅ Gmail integration is already connected to: {email}"
				)
			else:
				auth_url = res.get("auth_url")
				await message.reply_text(
					"🔐 Gmail Authentication Required\n\n"
					"Please click the link below to authorize access:\n"
					f"{auth_url}\n\n"
					"After authorizing, reply with the code in this format:\n"
					"/gmail <code>"
				)
		else:
			arg = parts[1].strip()
			if arg.lower() == "status":
				status = integration_manager.status("gmail")
				if status.get("connected"):
					email = status.get("email") or "unknown"
					await message.reply_text(
						f"✅ Gmail integration is connected to: {email}"
					)
				else:
					await message.reply_text(
						"❌ Gmail integration is not connected. Use /gmail to connect."
					)
			elif arg.lower() == "disconnect":
				integration_manager.disconnect("gmail")
				await message.reply_text("🔌 Gmail integration has been disconnected.")
			else:
				await message.reply_text("🔄 Completing authentication, please wait...")
				res = integration_manager.complete_auth("gmail", arg)
				if res.get("success"):
					status = integration_manager.status("gmail")
					email = status.get("email") or "unknown"
					await message.reply_text(
						f"✅ Gmail integration successfully connected to: {email}"
					)
				else:
					error = res.get("error") or "Unknown error"
					await message.reply_text(f"❌ Authentication failed:\n{error}")

	async def _handle_calendar_command(self, message, text: str) -> None:
		parts = text.split(maxsplit=1)
		if len(parts) == 1:
			res = integration_manager.connect("calendar")
			if res.get("connected"):
				status = integration_manager.status("calendar")
				email = status.get("email") or "unknown"
				await message.reply_text(
					f"✅ Calendar integration is already connected to: {email}"
				)
			else:
				auth_url = res.get("auth_url")
				await message.reply_text(
					"🔐 Google Calendar Authentication Required\n\n"
					"Please click the link below to authorize access:\n"
					f"{auth_url}\n\n"
					"After authorizing, reply with the code in this format:\n"
					"/calendar <code>"
				)
		else:
			arg = parts[1].strip()
			if arg.lower() == "status":
				status = integration_manager.status("calendar")
				if status.get("connected"):
					email = status.get("email") or "unknown"
					scopes_str = "\n".join([f"- {s}" for s in status.get("scopes", [])])
					expires = status.get("expires_at") or "never"
					await message.reply_text(
						"📊 Google Calendar Connection Status:\n\n"
						f"✅ Connected: True\n"
						f"📧 Email: {email}\n"
						f"⏳ Expires At: {expires}\n"
						f"🔑 Scopes:\n{scopes_str}"
					)
				else:
					await message.reply_text(
						"❌ Calendar integration is not connected. Use /calendar to connect."
					)
			elif arg.lower() == "disconnect":
				integration_manager.disconnect("calendar")
				await message.reply_text(
					"🔌 Calendar integration has been disconnected."
				)
			elif arg.lower() == "reconnect":
				integration_manager.disconnect("calendar")
				res = integration_manager.connect("calendar")
				auth_url = res.get("auth_url")
				await message.reply_text(
					"🔄 Google Calendar Reconnection Started\n\n"
					"Please click the link below to re-authorize access:\n"
					f"{auth_url}\n\n"
					"After authorizing, reply with the code in this format:\n"
					"/calendar <code>"
				)
			elif arg.lower() == "help":
				await message.reply_text(
					"📅 Google Calendar & Tasks Integration Commands:\n\n"
					"/calendar - Connect to Google Calendar & Tasks\n"
					"/calendar status - Show current connection details\n"
					"/calendar disconnect - Disconnect integration\n"
					"/calendar reconnect - Force re-authorization\n"
					"/calendar help - Show this message\n"
					"/calendar <code> - Submit callback code/URL to complete sign-in"
				)
			else:
				await message.reply_text("🔄 Completing authentication, please wait...")
				res = integration_manager.complete_auth("calendar", arg)
				if res.get("success"):
					status = integration_manager.status("calendar")
					email = status.get("email") or "unknown"
					await message.reply_text(
						f"✅ Calendar integration successfully connected to: {email}"
					)
				else:
					error = res.get("error") or "Unknown error"
					await message.reply_text(f"❌ Authentication failed:\n{error}")

	async def handle_message(
		self, update: Update, context: ContextTypes.DEFAULT_TYPE
	) -> None:
		parsed = parse_update(update)
		logger.info("telegram update parsed=%s", parsed)

		message = update.effective_message
		if message is None:
			logger.info("telegram update without message: %s", update.to_dict())
			return

		if parsed.text is None:
			logger.info("telegram update without text: %s", update.to_dict())
			return

		text = parsed.text.strip()

		if text.lower() == "ping":
			await message.reply_text("pong")
			return

		if text.lower().startswith("/gmail"):
			await self._handle_gmail_command(message, text)
			return

		if text.lower().startswith("/calendar"):
			await self._handle_calendar_command(message, text)
			return

		if text.lower() == "/end":
			status_message = await message.reply_text(
				"📝 <i>Archiving conversation, please wait...</i>", parse_mode="HTML"
			)
			conv_mgr = ConversationManager()
			try:
				result = await conv_mgr.end(update.effective_chat.id)
				title = result["title"]
				summary = result["summary"]
				response_text = (
					"✅ <b>Conversation Successfully Archived</b>\n\n"
					f"📌 <b>Title:</b> {html.escape(title)}\n"
					f"📖 <b>Summary:</b> {html.escape(summary)}\n\n"
					"<i>Active conversation context deleted. Start typing to begin a new thread!</i>"
				)
				await status_message.edit_text(response_text, parse_mode="HTML")
			except Exception as exc:
				logger.error(f"Failed to end conversation: {exc}")
				await status_message.edit_text(
					f"❌ <b>Failed to end conversation:</b>\n<code>{html.escape(str(exc))}</code>",
					parse_mode="HTML",
				)
			return

		# Handle agent query execution
		status_message = await message.reply_text(
			"🤖 <i>Agent is initializing...</i>", parse_mode="HTML"
		)

		conv_manager = ConversationManager()
		state = await conv_manager.append_user_message(
			chat_id=update.effective_chat.id, message=HumanMessage(content=parsed.text)
		)

		config = {"configurable": {"thread_id": f"tg-{update.effective_chat.id}"}}

		bot_data = context.application.bot_data
		if "pending_approvals" not in bot_data:
			bot_data["pending_approvals"] = {}

		chat_id = update.effective_chat.id
		approval_event = asyncio.Event()
		bot_data["pending_approvals"][chat_id] = {
			"event": approval_event,
			"decision": False,
		}

		async def telegram_approval_callback(
			session_name: str, action: str, danger_reason: str
		) -> bool:
			keyboard = [
				[
					InlineKeyboardButton(
						"✅ Approve", callback_data=f"approve_{chat_id}"
					),
					InlineKeyboardButton("❌ Deny", callback_data=f"deny_{chat_id}"),
				]
			]
			reply_markup = InlineKeyboardMarkup(keyboard)

			prompt = (
				"⚠️ <b>Dangerous Browser Action Warning!</b>\n\n"
				f"• <b>Session:</b> <code>{html.escape(session_name)}</code>\n"
				f"• <b>Action:</b> <code>{html.escape(action)}</code>\n"
				f"• <b>Reason:</b> {html.escape(danger_reason)}\n\n"
				"Do you want to allow this action?"
			)
			approval_event.clear()
			await message.reply_text(
				prompt, reply_markup=reply_markup, parse_mode="HTML"
			)
			await approval_event.wait()
			return bot_data["pending_approvals"][chat_id]["decision"]

		loop = asyncio.get_running_loop()
		register_approval_callback(telegram_approval_callback, loop)

		executed_tools = []
		final_response = None

		try:
			async for event in graph.astream(state, config):
				for node_name, node_output in event.items():
					for key, val in node_output.items():
						if key == "messages":
							state["messages"] = add_messages(
								state.get("messages") or [], val
							)
						else:
							state[key] = val

					if node_name == "tools":
						tool_outputs = node_output.get("tool_outputs") or []
						for out in tool_outputs:
							if out not in executed_tools:
								executed_tools.append(out)

						status_lines = []
						for idx, out in enumerate(executed_tools, start=1):
							status_lines.append(
								f"🛠 <b>{idx}.</b> <code>{html.escape(out['tool'])}</code> ({out['execution_time']:.2f}s)"
							)

						status_text = (
							"🤖 <i>Agent is executing tools...</i>\n\n"
							+ "\n".join(status_lines)
						)
						try:
							await status_message.edit_text(
								status_text, parse_mode="HTML"
							)
						except Exception:
							pass

					elif node_name == "planner":
						if "final_response" in node_output:
							final_response = node_output["final_response"]

			escaped_resp = (
				escape_telegram_html(final_response)
				if final_response
				else "(No response content returned)"
			)

			tool_log = ""
			if executed_tools:
				tool_log += "\n\n<b>🛠 Tool Executions Log</b>\n"
				for idx, out in enumerate(executed_tools, start=1):
					args_str = html.escape(str(out["args"]))
					if len(args_str) > 150:
						args_str = args_str[:147] + "..."
					tool_log += f"<b>{idx}.</b> <code>{html.escape(out['tool'])}</code>\n"
					tool_log += f"   • Args: <code>{args_str}</code>\n"
					tool_log += (
						f"   • Duration: <code>{out['execution_time']:.2f}s</code>\n"
					)

			final_msg = f"{escaped_resp}{tool_log}"
			try:
				await status_message.edit_text(final_msg, parse_mode="HTML")
			except Exception as html_err:
				logger.warning(
					"Failed to edit status message with HTML formatting: %s. Falling back to plain text.",
					html_err,
				)
				plain_tool_log = ""
				if executed_tools:
					plain_tool_log += "\n\n🛠 Tool Executions Log\n"
					for idx, out in enumerate(executed_tools, start=1):
						args_str = str(out["args"])
						if len(args_str) > 150:
							args_str = args_str[:147] + "..."
						plain_tool_log += f"{idx}. {out['tool']}\n"
						plain_tool_log += f"   • Args: {args_str}\n"
						plain_tool_log += f"   • Duration: {out['execution_time']:.2f}s\n"
				plain_msg = (
					f"{final_response or '(No response content returned)'}"
					f"{plain_tool_log}"
				)

				chunks = split_message(plain_msg)
				try:
					await status_message.edit_text(chunks[0], parse_mode=None)
				except Exception as edit_err:
					logger.error(
						"Failed to edit status message with plain text chunk: %s",
						edit_err,
					)

				for chunk in chunks[1:]:
					try:
						await message.reply_text(chunk, parse_mode=None)
					except Exception as send_err:
						logger.error(
							"Failed to send message chunk: %s", send_err
						)

			# Process file attachments tagged with [ATTACH_FILE:<path>]
			import re
			from pathlib import Path
			raw_check_text = (final_response or "") + str(executed_tools)
			attachment_matches = re.findall(r"\[ATTACH_FILE:(.*?)\]", raw_check_text)
			for attach_path in set(attachment_matches):
				try:
					p = Path(attach_path.strip())
					if p.exists() and p.is_file():
						with open(p, "rb") as doc:
							await message.reply_document(
								document=doc,
								filename=p.name,
								caption=f"📎 Attached: {p.name}",
							)
				except Exception as att_err:
					logger.error("Failed to send document attachment %s: %s", attach_path, att_err)

			await conv_manager.save(update.effective_chat.id, state)

		except Exception as exc:
			logger.exception("Error during Telegram agent execution:")
			exc_str = str(exc)
			if len(exc_str) > 3500:
				exc_str = exc_str[:3400] + "... [TRUNCATED]"
			try:
				await status_message.edit_text(
					f"❌ <b>An error occurred while running the pipeline:</b>\n<code>{html.escape(exc_str)}</code>",
					parse_mode="HTML",
				)
			except Exception as edit_err:
				logger.error(
					"Failed to update status message with error context: %s",
					edit_err,
				)
		finally:
			register_approval_callback(None)
			bot_data["pending_approvals"].pop(chat_id, None)

	async def handle_callback_query(
		self, update: Update, context: ContextTypes.DEFAULT_TYPE
	) -> None:
		query = update.callback_query
		if not query:
			return
		await query.answer()

		data = query.data
		if not data or "_" not in data:
			return

		action, chat_id_str = data.split("_", 1)
		try:
			chat_id = int(chat_id_str)
		except ValueError:
			return

		pending = context.application.bot_data.get("pending_approvals", {})
		if chat_id in pending:
			pending[chat_id]["decision"] = action == "approve"
			pending[chat_id]["event"].set()

			decision_text = "✅ Approved" if action == "approve" else "❌ Denied"
			try:
				await query.edit_message_text(
					text=query.message.text_html
					+ f"\n\n<b>Decision:</b> {decision_text}",
					parse_mode="HTML",
				)
			except Exception as e:
				logger.warning(
					"Failed to edit callback query message with HTML: %s. Falling back to plain text.",
					e,
				)
				await query.edit_message_text(
					text=query.message.text + f"\n\nDecision: {decision_text}",
					parse_mode=None,
				)
