"""Two-tier Capability Router using BGE Reranker and Task Decomposition."""

import logging
import re
import requests
from typing import Any

from app.config.settings import settings
from app.tools import (
    retrieve_memory,
    web_search,
    read_file,
    write_file,
    manage_file,
    list_files,
    search_files,
    send_file,
    execute_python_code,
    execute_node_code,
    execute_bash_command,
    gmail_search,
    gmail_read,
    gmail_send,
    gmail_reply,
    gmail_download_attachment,
    list_calendar,
    manage_event,
    manage_task,
    calendar_free_busy,
    browser_open,
    browser_interact,
    browser_navigate,
    browser_scroll,
    browser_file,
    browser_close,
    start_sandbox_server,
    stop_sandbox_server,
    get_sandbox_preview,
    tools as all_tools,
)

logger = logging.getLogger("openclaw-agent")

# Map tool groups to their respective tool objects
TOOL_GROUP_MAP = {
    "memory": [
        retrieve_memory,
    ],
    "web": [
        web_search,
    ],
    "coding": [
        read_file,
        write_file,
        manage_file,
        list_files,
        search_files,
        send_file,
        execute_python_code,
        execute_node_code,
        execute_bash_command,
    ],
    "gmail": [
        gmail_search,
        gmail_read,
        gmail_send,
        gmail_reply,
        gmail_download_attachment,
    ],
    "calendar": [
        list_calendar,
        manage_event,
        manage_task,
        calendar_free_busy,
    ],
    "browser": [
        browser_open,
        browser_interact,
        browser_navigate,
        browser_scroll,
        browser_file,
        browser_close,
    ],
    "sandbox": [
        start_sandbox_server,
        stop_sandbox_server,
        get_sandbox_preview,
    ],
}

# Document descriptions used by the BGE Reranker
TOOL_GROUP_DOCUMENTS = {
    "gmail": "Gmail tools: Search, read, send, reply to, and download email messages and attachments. Use these tools when the user asks about emails, Gmail, inbox messages, senders, recipients, email threads, or attachments.",
    "memory": "Memory tools: Retrieve relevant information from previous conversations, persistent user facts, preferences, project decisions, historical discussions, and past debugging sessions. and user information",
    "web": "Web tools: Search the internet for fresh or current information, websites, news, documentation, prices, external facts, and online resources.",
    "calendar": "Calendar tools: List calendars, events, meetings, tasks, and check availability or free/busy periods. Create, update, or delete calendar events and tasks.",
    "coding": "Coding and filesystem export tools: Read, search, create, modify, send_file, compress, zip, attach, send, export, and execute code and files inside the workspace. Use for programming, debugging, testing, sending codebase/folder as zip/files, sharing files, compilation, and development tasks.",
    "browser": "Browser tools: Open websites, navigate pages, interact with page elements, click, type, select, scroll, and upload or download files through a browser.",
    "sandbox": "Sandbox tools: Start, stop, and inspect long-running development servers and obtain preview URLs for applications running in the sandbox.",
}

TOOL_GROUP_NAMES = list(TOOL_GROUP_DOCUMENTS.keys())

# Keywords that indicate a coding‑related request
CODING_KEYWORDS = [
    "build",
    "compile",
    "run",
    "test",
    "execute",
    "debug",
    "code",
    "script",
    "make",
    "install",
    "deploy",
    "package",
    "send",
    "attach",
    "zip",
    "export",
    "share",
    "portfolio",
    "workspace",
    "file",
    "files",
]

def contains_coding_keywords(query: str) -> bool:
    """Return True if the query contains any coding‑related keyword.
    Uses a simple word‑boundary regex for detection, case‑insensitive.
    """
    pattern = re.compile(r"\b(" + "|".join(CODING_KEYWORDS) + r")\b", re.IGNORECASE)
    return bool(pattern.search(query))
DOCUMENTS_LIST = [TOOL_GROUP_DOCUMENTS[name] for name in TOOL_GROUP_NAMES]

COMMON_VERBS = [
    "make", "create", "build", "find", "search", "start", "stop", "open",
    "check", "send", "reply", "email", "get", "list", "run", "read", "write",
    "update", "delete", "format", "inspect", "navigate", "download", "save", "look",
    "attach", "zip", "export", "share"
]

CONVERSATIONAL_PATTERNS = [
    r"^(hi|hello|hey|howdy|sup|yo|greetings|good\s+(morning|afternoon|evening))\b",
    r"^(how\s+are\s+you|how\s+is\s+it\s+going|what'?s\s+up)\b",
    r"^(who\s+are\s+you|what\s+is\s+your\s+name|what\s+can\s+you\s+do)\b",
    r"^(tell\s+me\s+a\s+joke|make\s+a\s+joke|say\s+something\s+funny)\b",
    r"^(thank\s+you|thanks|thx|bye|goodbye|see\s+you)\b",
]


def is_conversational_query(query: str) -> bool:
    """Detects pure conversational/small-talk prompts that do not require external tools."""
    clean_q = query.strip().lower()
    # Strip trailing punctuation
    clean_q = re.sub(r"[?!.,]+$", "", clean_q).strip()

    if len(clean_q.split()) <= 5:
        for pattern in CONVERSATIONAL_PATTERNS:
            if re.search(pattern, clean_q):
                return True
    return False


def normalize_infinity_url(raw_url: str) -> str:
    """Strips trailing endpoint paths to get the root host URL."""
    url = raw_url.rstrip("/")
    for suffix in ["/rerank", "/v1/rerank", "/embeddings", "/v1/embeddings"]:
        if url.endswith(suffix):
            url = url[:-len(suffix)].rstrip("/")
    return url


def decompose_query_to_tasks(query: str) -> list[str]:
    """Action verb & clause-aware task decomposition for dynamic tool routing."""
    query = query.strip()
    if not query:
        return []

    # First split on explicit delimiters (and then, then, after that, comma, semicolon, and)
    delimiters = r"\b(?:and\s+then|then|after\s+that|plus|as\s+well\s+as|and)\b|;|,"
    raw_clauses = re.split(delimiters, query, flags=re.IGNORECASE)

    tasks = []
    verb_pattern = re.compile(rf"\b({'|'.join(COMMON_VERBS)})\b", re.IGNORECASE)

    for clause in raw_clauses:
        clause = clause.strip()
        if not clause:
            continue
        
        # Check if clause contains multiple action verbs without explicit delimiters
        matches = list(verb_pattern.finditer(clause))
        if len(matches) > 1:
            last_pos = 0
            for i in range(1, len(matches)):
                split_pos = matches[i].start()
                sub = clause[last_pos:split_pos].strip()
                if sub:
                    tasks.append(sub)
                last_pos = split_pos
            remaining = clause[last_pos:].strip()
            if remaining:
                tasks.append(remaining)
        else:
            tasks.append(clause)

    return tasks if tasks else [query]

# Helper to check for coding intent before reranking
# (Already defined above as contains_coding_keywords)



def rerank_task(task_text: str, infinity_url: str) -> list[tuple[str, float]]:
    """Calls the BGE reranker API for a single query string against the 7 tool group definitions."""
    base_url = normalize_infinity_url(infinity_url)
    endpoint = f"{base_url}/rerank"
    payload = {
        "model": "BAAI/bge-reranker-base",
        "query": task_text,
        "documents": DOCUMENTS_LIST,
    }
    try:
        resp = requests.post(endpoint, json=payload, timeout=4.0)
        if resp.status_code == 200:
            data = resp.json()
            results = []
            for item in data.get("results", []):
                idx = item["index"]
                score = item["relevance_score"]
                results.append((TOOL_GROUP_NAMES[idx], score))
            results.sort(key=lambda x: x[1], reverse=True)
            return results
    except Exception as exc:
        logger.warning(f"[tool_router] Reranker API call failed for '{task_text[:30]}...': {exc}")
    return []


def route_tools_for_query(query: str, threshold: float = 0.0001) -> tuple[list[Any], list[str]]:
    """Two-tier Capability Router:
    
    1. Conversational Query -> Expose 0 tools (Pure LLM mode, saving 100% tool tokens).
    2. Single Action Query (1 group) -> Rerank directly on full query.
    3. Multi Action Query (2+ groups) -> Decompose into T1, T2, T3 -> Rerank per task -> Deduplicate groups.
    
    Returns:
        tuple of (selected_tool_objects, selected_group_names)
    """
    if not settings.enable_tool_router:
        return all_tools, list(TOOL_GROUP_MAP.keys())

    # Fast-path check for purely conversational queries (hello, tell me a joke, thanks, etc.)
    if is_conversational_query(query):
        logger.info("[capability_router] Conversational chit-chat query detected. Exposing 0 tools (Pure LLM response).")
        return [], []

    infinity_url = settings.infinity_url or "http://72.62.247.193:7997"
    tasks = decompose_query_to_tasks(query)

    selected_groups = set()
    # Fast‑path: include coding tools if query contains coding keywords
    if contains_coding_keywords(query):
        selected_groups.add("coding")
        logger.info("[capability_router] Coding keywords detected - exposing coding tools.")

    if len(tasks) <= 1:
        # PATH A: Single Group Direct Reranking
        logger.info("[capability_router] Single-action query detected. Direct reranking...")
        results = rerank_task(query, infinity_url)
        if results:
            top_group, top_score = results[0]
            if top_score >= threshold:
                selected_groups.add(top_group)
                if len(results) > 1 and results[1][1] >= threshold and results[1][1] >= (0.25 * top_score):
                    selected_groups.add(results[1][0])
    else:
        # PATH B: Multi-Action Query -> Decompose into T1, T2, T3 -> Rerank per task
        logger.info(f"[capability_router] Multi-action query detected ({len(tasks)} tasks: {tasks}). Task-by-task reranking...")
        for task in tasks:
            results = rerank_task(task, infinity_url)
            if results:
                top_group, top_score = results[0]
                if top_score >= threshold:
                    selected_groups.add(top_group)
                    if len(results) > 1 and results[1][1] >= threshold and results[1][1] >= (0.25 * top_score):
                        selected_groups.add(results[1][0])

    # Fallback to all tools if empty selection or error on action query
    if not selected_groups:
        logger.info("[capability_router] No specific tool group selected or reranker unavailable. Exposing default full tool set.")
        return all_tools, list(TOOL_GROUP_MAP.keys())

    selected_tools = []
    for group_name in sorted(list(selected_groups)):
        selected_tools.extend(TOOL_GROUP_MAP.get(group_name, []))

    logger.info(
        f"[capability_router] Selected Groups: {sorted(list(selected_groups))} "
        f"(Exposing {len(selected_tools)}/{len(all_tools)} tools to bind_tools)"
    )

    return selected_tools, sorted(list(selected_groups))
