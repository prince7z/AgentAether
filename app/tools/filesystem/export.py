from __future__ import annotations

import os
import zipfile
from pathlib import Path
from typing import Any

from langchain.tools import tool
from langchain_core.runnables import RunnableConfig

from app.tools.filesystem._common import make_result, to_path

IGNORED_PATTERNS = {
    ".git",
    "__pycache__",
    "node_modules",
    "dist",
    ".venv",
    "venv",
    ".idea",
    ".vscode",
    ".next",
    "build",
    "openclaw.db",
}


def prepare_file_for_export(target_path: str, config: RunnableConfig = None) -> dict[str, Any]:
    """Prepares a file or folder for exporting/sending in chat.

    - Single File: Prepares the file directly without zipping.
    - Folder: Compresses the folder into a ZIP file (excluding heavy build dirs) and returns the zip path.
    """
    try:
        path = None
        try:
            path = to_path(target_path, config=config)
        except Exception:
            pass

        if not path or not path.exists():
            direct_path = Path(target_path).resolve()
            if direct_path.exists():
                path = direct_path
            else:
                return make_result(False, None, f"Path does not exist: {target_path}")

        # CASE 1: Single file -> send directly
        if path.is_file():
            abs_path = str(path.resolve(strict=False))
            return {
                "success": True,
                "is_folder": False,
                "file_path": abs_path,
                "filename": path.name,
                "message": f"File ready to send directly: {path.name}",
            }

        # CASE 2: Directory/Folder -> compress into ZIP archive
        elif path.is_dir():
            output_zip = path.parent / f"{path.name}.zip"
            with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for root, dirs, files in os.walk(path):
                    # Exclude unwanted build/system directories
                    dirs[:] = [d for d in dirs if d not in IGNORED_PATTERNS]
                    for file in files:
                        file_path = Path(root) / file
                        if file_path == output_zip:
                            continue
                        arcname = file_path.relative_to(path)
                        zip_file.write(file_path, arcname)

            abs_zip_path = str(output_zip.resolve(strict=False))
            return {
                "success": True,
                "is_folder": True,
                "file_path": abs_zip_path,
                "filename": output_zip.name,
                "message": f"Folder successfully compressed into ZIP archive: {output_zip.name}",
            }

        return make_result(False, None, f"Unsupported path type: {target_path}")
    except Exception as exc:
        return make_result(False, None, str(exc))


@tool
def send_file(path: str, config: RunnableConfig = None) -> dict[str, Any]:
    """Export and send a file or folder in the chat.

    Use this tool when the user asks to send, attach, download, or share code, files, or folders.
    - If path points to a single file (e.g. 'main.py' or 'App.jsx'), it sends the file directly.
    - If path points to a directory/folder (e.g. './src' or 'portfolio'), it zips the folder first and sends the ZIP file.
    """
    res = prepare_file_for_export(path, config=config)
    if res.get("success"):
        file_path = res["file_path"]
        is_folder = res["is_folder"]
        filename = res["filename"]

        attachment_tag = f"[ATTACH_FILE:{file_path}]"

        if is_folder:
            status_str = f"{attachment_tag} Compressed directory '{filename}' into a ZIP file and attached it."
        else:
            status_str = f"{attachment_tag} Attached file '{filename}' directly."

        return {
            "success": True,
            "file_path": file_path,
            "filename": filename,
            "is_folder": is_folder,
            "attachment_tag": attachment_tag,
            "status": status_str,
        }
    else:
        return res
