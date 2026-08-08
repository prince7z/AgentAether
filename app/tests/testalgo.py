import json
import sys
from pathlib import Path

# Reconfigure stdout for safe unicode printing on Windows
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Define allowed tool groups strictly as per specification
ALLOWED_TOOL_GROUPS = {
    "memory",
    "web",
    "coding",
    "gmail",
    "calendar",
    "browser",
    "sandbox",
}

# Master dataset of 100 queries with golden classifications and atomic task breakdowns
DATASET = [
    # -------------------------------------------------------------------------
    # SINGLE-TASK QUERIES (1 - 56)
    # -------------------------------------------------------------------------
    {
        "id": 1,
        "query": "Find the email from Cisco about my interview.",
        "classification": "single",
        "tasks": [
            {
                "task": "Find the email from Cisco about my interview.",
                "tool_groups": ["gmail"],
            }
        ],
    },
    {
        "id": 2,
        "query": "What did we discuss about SalesAkart?",
        "classification": "single",
        "tasks": [
            {
                "task": "Retrieve conversation and project notes about SalesAkart from memory.",
                "tool_groups": ["memory"],
            }
        ],
    },
    {
        "id": 3,
        "query": "Check whether I am free tomorrow.",
        "classification": "single",
        "tasks": [
            {
                "task": "Check calendar events and availability for tomorrow.",
                "tool_groups": ["calendar"],
            }
        ],
    },
    {
        "id": 4,
        "query": "Search the web for the latest Next.js release.",
        "classification": "single",
        "tasks": [
            {
                "task": "Search the web for news and notes on the latest Next.js release.",
                "tool_groups": ["web"],
            }
        ],
    },
    {
        "id": 5,
        "query": "List the files in my workspace.",
        "classification": "single",
        "tasks": [
            {
                "task": "List files and directories in the workspace.",
                "tool_groups": ["coding"],
            }
        ],
    },
    {
        "id": 6,
        "query": "Open Google.",
        "classification": "single",
        "tasks": [
            {
                "task": "Navigate browser to Google homepage.",
                "tool_groups": ["browser"],
            }
        ],
    },
    {
        "id": 7,
        "query": "What is the capital of France?",
        "classification": "single",
        "tasks": [
            {
                "task": "State that Paris is the capital of France.",
                "tool_groups": [],
            }
        ],
    },
    {
        "id": 8,
        "query": "Find the invoice PDF in my Gmail.",
        "classification": "single",
        "tasks": [
            {
                "task": "Search Gmail messages for an invoice PDF.",
                "tool_groups": ["gmail"],
            }
        ],
    },
    {
        "id": 9,
        "query": "Schedule a meeting with Alex for 3 PM tomorrow.",
        "classification": "single",
        "tasks": [
            {
                "task": "Create a calendar entry with Alex for 3 PM tomorrow.",
                "tool_groups": ["calendar"],
            }
        ],
    },
    {
        "id": 10,
        "query": "Can you explain what Docker containers are?",
        "classification": "single",
        "tasks": [
            {
                "task": "Explain the concept of Docker containers.",
                "tool_groups": [],
            }
        ],
    },
    {
        "id": 11,
        "query": "Where did we decide to host the API database?",
        "classification": "single",
        "tasks": [
            {
                "task": "Recall the hosting decision for the API database from memory.",
                "tool_groups": ["memory"],
            }
        ],
    },
    {
        "id": 12,
        "query": "Look up python-telegram-bot documentation on the web.",
        "classification": "single",
        "tasks": [
            {
                "task": "Search the web for python-telegram-bot documentation.",
                "tool_groups": ["web"],
            }
        ],
    },
    {
        "id": 13,
        "query": "Format this JSON string for me.",
        "classification": "single",
        "tasks": [
            {
                "task": "Format the provided JSON string cleanly.",
                "tool_groups": [],
            }
        ],
    },
    {
        "id": 14,
        "query": "Check if there are any syntax errors in app/main.py.",
        "classification": "single",
        "tasks": [
            {
                "task": "Inspect app/main.py for python syntax errors.",
                "tool_groups": ["coding"],
            }
        ],
    },
    {
        "id": 15,
        "query": "Navigate to https://github.com/trending.",
        "classification": "single",
        "tasks": [
            {
                "task": "Open https://github.com/trending in browser.",
                "tool_groups": ["browser"],
            }
        ],
    },
    {
        "id": 16,
        "query": "Stop the dev server running on port 3000.",
        "classification": "single",
        "tasks": [
            {
                "task": "Stop the sandbox development server active on port 3000.",
                "tool_groups": ["sandbox"],
            }
        ],
    },
    {
        "id": 17,
        "query": "Find my flight confirmation email from Delta.",
        "classification": "single",
        "tasks": [
            {
                "task": "Search Gmail for Delta flight confirmation.",
                "tool_groups": ["gmail"],
            }
        ],
    },
    {
        "id": 18,
        "query": "Do I have any events scheduled for this afternoon?",
        "classification": "single",
        "tasks": [
            {
                "task": "Check calendar events scheduled for this afternoon.",
                "tool_groups": ["calendar"],
            }
        ],
    },
    {
        "id": 19,
        "query": "Summarize the tech stack preferences saved in my profile.",
        "classification": "single",
        "tasks": [
            {
                "task": "Fetch tech stack preferences from memory profile.",
                "tool_groups": ["memory"],
            }
        ],
    },
    {
        "id": 20,
        "query": "Search Google for recent news on quantum computing.",
        "classification": "single",
        "tasks": [
            {
                "task": "Search the web for news about quantum computing.",
                "tool_groups": ["web"],
            }
        ],
    },
    {
        "id": 21,
        "query": "Read lines 40 to 100 in app/agent/planner.py.",
        "classification": "single",
        "tasks": [
            {
                "task": "Read specified line range from app/agent/planner.py.",
                "tool_groups": ["coding"],
            }
        ],
    },
    {
        "id": 22,
        "query": "Click on the login button on the open web page.",
        "classification": "single",
        "tasks": [
            {
                "task": "Interact with browser to click the login button.",
                "tool_groups": ["browser"],
            }
        ],
    },
    {
        "id": 23,
        "query": "Is port 8000 currently open on the sandbox environment?",
        "classification": "single",
        "tasks": [
            {
                "task": "Inspect sandbox active ports for port 8000.",
                "tool_groups": ["sandbox"],
            }
        ],
    },
    {
        "id": 24,
        "query": "Write a Python function to compute the fibonacci sequence.",
        "classification": "single",
        "tasks": [
            {
                "task": "Generate Python function for computing fibonacci sequence.",
                "tool_groups": [],
            }
        ],
    },
    {
        "id": 25,
        "query": "Check my inbox for unread messages.",
        "classification": "single",
        "tasks": [
            {
                "task": "Search Gmail for unread inbox emails.",
                "tool_groups": ["gmail"],
            }
        ],
    },
    {
        "id": 26,
        "query": "What time is my meeting with Sarah on Friday?",
        "classification": "single",
        "tasks": [
            {
                "task": "Check calendar for meeting with Sarah on Friday.",
                "tool_groups": ["calendar"],
            }
        ],
    },
    {
        "id": 27,
        "query": "Retrieve our team's coding conventions from memory.",
        "classification": "single",
        "tasks": [
            {
                "task": "Retrieve stored team coding conventions from memory.",
                "tool_groups": ["memory"],
            }
        ],
    },
    {
        "id": 28,
        "query": "Search arXiv for papers on LLM agents.",
        "classification": "single",
        "tasks": [
            {
                "task": "Search web and arXiv for papers on LLM agents.",
                "tool_groups": ["web"],
            }
        ],
    },
    {
        "id": 29,
        "query": "Grep for `TelegramGateway` across the project files.",
        "classification": "single",
        "tasks": [
            {
                "task": "Grep search project files for symbol `TelegramGateway`.",
                "tool_groups": ["coding"],
            }
        ],
    },
    {
        "id": 30,
        "query": "Take a screenshot of the current browser tab.",
        "classification": "single",
        "tasks": [
            {
                "task": "Capture screenshot of current page in browser.",
                "tool_groups": ["browser"],
            }
        ],
    },
    {
        "id": 31,
        "query": "Start a preview server for the frontend workspace.",
        "classification": "single",
        "tasks": [
            {
                "task": "Start sandbox preview server for frontend workspace.",
                "tool_groups": ["sandbox"],
            }
        ],
    },
    {
        "id": 32,
        "query": "Translate 'Good morning' into Spanish.",
        "classification": "single",
        "tasks": [
            {
                "task": "Translate phrase 'Good morning' to Spanish.",
                "tool_groups": [],
            }
        ],
    },
    {
        "id": 33,
        "query": "Find emails containing 'project report'.",
        "classification": "single",
        "tasks": [
            {
                "task": "Search Gmail messages for keyword 'project report'.",
                "tool_groups": ["gmail"],
            }
        ],
    },
    {
        "id": 34,
        "query": "Clear my afternoon schedule for today.",
        "classification": "single",
        "tasks": [
            {
                "task": "Remove all calendar events scheduled for this afternoon.",
                "tool_groups": ["calendar"],
            }
        ],
    },
    {
        "id": 35,
        "query": "What user preferences do you remember about my dark mode setting?",
        "classification": "single",
        "tasks": [
            {
                "task": "Look up dark mode preference in memory.",
                "tool_groups": ["memory"],
            }
        ],
    },
    {
        "id": 36,
        "query": "Look up the weather forecast in Tokyo today.",
        "classification": "single",
        "tasks": [
            {
                "task": "Search web for today's weather forecast in Tokyo.",
                "tool_groups": ["web"],
            }
        ],
    },
    {
        "id": 37,
        "query": "Run the unit test suite in app/tests.",
        "classification": "single",
        "tasks": [
            {
                "task": "Execute pytest suite in app/tests.",
                "tool_groups": ["coding"],
            }
        ],
    },
    {
        "id": 38,
        "query": "Scroll down to the footer of the active web page.",
        "classification": "single",
        "tasks": [
            {
                "task": "Scroll browser page down to footer element.",
                "tool_groups": ["browser"],
            }
        ],
    },
    {
        "id": 39,
        "query": "Inspect the health status of the running sandbox containers.",
        "classification": "single",
        "tasks": [
            {
                "task": "Check container health in sandbox environment.",
                "tool_groups": ["sandbox"],
            }
        ],
    },
    {
        "id": 40,
        "query": "Help me outline an essay on renewable energy.",
        "classification": "single",
        "tasks": [
            {
                "task": "Draft an outline for an essay on renewable energy.",
                "tool_groups": [],
            }
        ],
    },
    {
        "id": 41,
        "query": "Locate the email with subject 'Monthly Invoice'.",
        "classification": "single",
        "tasks": [
            {
                "task": "Search Gmail for email with subject 'Monthly Invoice'.",
                "tool_groups": ["gmail"],
            }
        ],
    },
    {
        "id": 42,
        "query": "Add a reminder to call the dentist at 5 PM on Monday.",
        "classification": "single",
        "tasks": [
            {
                "task": "Add calendar event to call dentist at 5 PM on Monday.",
                "tool_groups": ["calendar"],
            }
        ],
    },
    {
        "id": 43,
        "query": "Recall what my favorite programming language is.",
        "classification": "single",
        "tasks": [
            {
                "task": "Query memory for favorite programming language.",
                "tool_groups": ["memory"],
            }
        ],
    },
    {
        "id": 44,
        "query": "Search DuckDuckGo for Rust async frameworks.",
        "classification": "single",
        "tasks": [
            {
                "task": "Search web for Rust async web frameworks.",
                "tool_groups": ["web"],
            }
        ],
    },
    {
        "id": 45,
        "query": "Create a new file named utils/helpers.py.",
        "classification": "single",
        "tasks": [
            {
                "task": "Create empty file utils/helpers.py in workspace.",
                "tool_groups": ["coding"],
            }
        ],
    },
    {
        "id": 46,
        "query": "Fill out the username input field on the page.",
        "classification": "single",
        "tasks": [
            {
                "task": "Type username into browser input field.",
                "tool_groups": ["browser"],
            }
        ],
    },
    {
        "id": 47,
        "query": "Check the logs of the running development container.",
        "classification": "single",
        "tasks": [
            {
                "task": "Fetch runtime container logs in sandbox.",
                "tool_groups": ["sandbox"],
            }
        ],
    },
    {
        "id": 48,
        "query": "Draft a polite decline response text for an event invitation.",
        "classification": "single",
        "tasks": [
            {
                "task": "Write polite decline text for invitation.",
                "tool_groups": [],
            }
        ],
    },
    {
        "id": 49,
        "query": "Show all emails sent by John last week.",
        "classification": "single",
        "tasks": [
            {
                "task": "Search Gmail for messages sent by John from last week.",
                "tool_groups": ["gmail"],
            }
        ],
    },
    {
        "id": 50,
        "query": "List all my calendar categories.",
        "classification": "single",
        "tasks": [
            {
                "task": "Retrieve list of calendar categories.",
                "tool_groups": ["calendar"],
            }
        ],
    },
    {
        "id": 51,
        "query": "Search past memory for our discussion on database migrations.",
        "classification": "single",
        "tasks": [
            {
                "task": "Query memory for past notes on database migrations.",
                "tool_groups": ["memory"],
            }
        ],
    },
    {
        "id": 52,
        "query": "Search the web for FastAPI websocket benchmarks.",
        "classification": "single",
        "tasks": [
            {
                "task": "Search web for FastAPI websocket benchmarks.",
                "tool_groups": ["web"],
            }
        ],
    },
    {
        "id": 53,
        "query": "Check git log for the last 5 commits.",
        "classification": "single",
        "tasks": [
            {
                "task": "Run git log command to inspect last 5 commits.",
                "tool_groups": ["coding"],
            }
        ],
    },
    {
        "id": 54,
        "query": "Download the file from the current browser link.",
        "classification": "single",
        "tasks": [
            {
                "task": "Trigger file download via active browser session.",
                "tool_groups": ["browser"],
            }
        ],
    },
    {
        "id": 55,
        "query": "Check if the dev server on port 5000 is still active.",
        "classification": "single",
        "tasks": [
            {
                "task": "Verify sandbox server status on port 5000.",
                "tool_groups": ["sandbox"],
            }
        ],
    },
    {
        "id": 56,
        "query": "What is a 15% tip on a $120 bill?",
        "classification": "single",
        "tasks": [
            {
                "task": "Calculate 15% tip on $120.",
                "tool_groups": [],
            }
        ],
    },
    # -------------------------------------------------------------------------
    # MULTI-TASK QUERIES (57 - 100)
    # -------------------------------------------------------------------------
    {
        "id": 57,
        "query": "Find the Cisco interview email and reply to it saying I am available tomorrow.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Find the Cisco interview email.",
                "tool_groups": ["gmail"],
            },
            {
                "task": "Reply to the email saying I am available tomorrow.",
                "tool_groups": ["gmail"],
            },
        ],
    },
    {
        "id": 58,
        "query": "Create a portfolio app and start the server.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Create the portfolio application codebase.",
                "tool_groups": ["coding"],
            },
            {
                "task": "Start the development server for the portfolio app.",
                "tool_groups": ["sandbox"],
            },
        ],
    },
    {
        "id": 59,
        "query": "Search my Gmail for the invoice and save the attachment.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Search Gmail for the invoice email.",
                "tool_groups": ["gmail"],
            },
            {
                "task": "Download and save the invoice attachment.",
                "tool_groups": ["gmail"],
            },
        ],
    },
    {
        "id": 60,
        "query": "Check my calendar and email me the available times.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Check calendar for free available times.",
                "tool_groups": ["calendar"],
            },
            {
                "task": "Send an email containing the available times.",
                "tool_groups": ["gmail"],
            },
        ],
    },
    {
        "id": 61,
        "query": "Find the bug, fix it, and run the tests.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Find the bug in the codebase.",
                "tool_groups": ["coding"],
            },
            {
                "task": "Fix the identified bug in code.",
                "tool_groups": ["coding"],
            },
            {
                "task": "Run the test suite to verify the fix.",
                "tool_groups": ["coding"],
            },
        ],
    },
    {
        "id": 62,
        "query": "Create the website, start the server, and give me the preview URL.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Create the website source code.",
                "tool_groups": ["coding"],
            },
            {
                "task": "Start the preview server.",
                "tool_groups": ["sandbox"],
            },
            {
                "task": "Obtain and return the preview URL.",
                "tool_groups": ["sandbox"],
            },
        ],
    },
    {
        "id": 63,
        "query": "Check my memory for our project roadmap, search the web for competitors, and summarize the differences.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Retrieve project roadmap details from memory.",
                "tool_groups": ["memory"],
            },
            {
                "task": "Search the web for competitor products and features.",
                "tool_groups": ["web"],
            },
            {
                "task": "Summarize the differences between our roadmap and competitors.",
                "tool_groups": [],
            },
        ],
    },
    {
        "id": 64,
        "query": "Search Gmail for the Zoom link, check if I am free at that time, and accept the meeting.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Search Gmail for the email containing the Zoom link.",
                "tool_groups": ["gmail"],
            },
            {
                "task": "Check calendar availability at the meeting time.",
                "tool_groups": ["calendar"],
            },
            {
                "task": "Accept the meeting invitation on calendar.",
                "tool_groups": ["calendar"],
            },
        ],
    },
    {
        "id": 65,
        "query": "Open the project dashboard in the browser, log in with saved credentials, and take a screenshot.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Navigate browser to project dashboard page.",
                "tool_groups": ["browser"],
            },
            {
                "task": "Perform login interaction on the dashboard page.",
                "tool_groups": ["browser"],
            },
            {
                "task": "Capture screenshot of logged-in dashboard.",
                "tool_groups": ["browser"],
            },
        ],
    },
    {
        "id": 66,
        "query": "Look up the latest Next.js 14 release notes on the web and email a summary to team@example.com.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Search web for Next.js 14 release notes.",
                "tool_groups": ["web"],
            },
            {
                "task": "Send summary email to team@example.com.",
                "tool_groups": ["gmail"],
            },
        ],
    },
    {
        "id": 67,
        "query": "Check my calendar for tomorrow's standup, grab the agenda from memory, and email it to attendees.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Check calendar for tomorrow's standup meeting details.",
                "tool_groups": ["calendar"],
            },
            {
                "task": "Retrieve standup agenda from memory.",
                "tool_groups": ["memory"],
            },
            {
                "task": "Email standup agenda to meeting attendees.",
                "tool_groups": ["gmail"],
            },
        ],
    },
    {
        "id": 68,
        "query": "Find the broken endpoint in app/api, write a fix, run unit tests, and start the sandbox server to verify.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Locate broken endpoint code in app/api.",
                "tool_groups": ["coding"],
            },
            {
                "task": "Apply fix to broken endpoint code.",
                "tool_groups": ["coding"],
            },
            {
                "task": "Execute unit tests for app/api.",
                "tool_groups": ["coding"],
            },
            {
                "task": "Start sandbox development server to verify endpoint.",
                "tool_groups": ["sandbox"],
            },
        ],
    },
    {
        "id": 69,
        "query": "Search Gmail for flight receipt, add the flight schedule to calendar, and post a confirmation on the web portal.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Search Gmail for flight receipt email.",
                "tool_groups": ["gmail"],
            },
            {
                "task": "Add flight schedule to calendar.",
                "tool_groups": ["calendar"],
            },
            {
                "task": "Navigate web portal and submit flight confirmation.",
                "tool_groups": ["browser"],
            },
        ],
    },
    {
        "id": 70,
        "query": "Look up my user preference for code style in memory and format the script app/tests/rough.py.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Recall code style preference from memory.",
                "tool_groups": ["memory"],
            },
            {
                "task": "Format code in app/tests/rough.py according to preferences.",
                "tool_groups": ["coding"],
            },
        ],
    },
    {
        "id": 71,
        "query": "Find the latest report email, extract the PDF attachment, read the code changes inside, and create a PR branch.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Find latest report email in Gmail.",
                "tool_groups": ["gmail"],
            },
            {
                "task": "Download PDF attachment from email.",
                "tool_groups": ["gmail"],
            },
            {
                "task": "Read code changes described inside PDF.",
                "tool_groups": ["coding"],
            },
            {
                "task": "Create new Git PR branch in workspace.",
                "tool_groups": ["coding"],
            },
        ],
    },
    {
        "id": 72,
        "query": "Check if the dev server on port 8000 is running, stop it if active, and restart it with reload flag.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Check status of sandbox server on port 8000.",
                "tool_groups": ["sandbox"],
            },
            {
                "task": "Stop active sandbox server on port 8000.",
                "tool_groups": ["sandbox"],
            },
            {
                "task": "Start sandbox server with reload flag.",
                "tool_groups": ["sandbox"],
            },
        ],
    },
    {
        "id": 73,
        "query": "Search the web for Python 3.12 release notes and save a summary into workspace file docs/release_notes.md.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Search web for Python 3.12 release notes.",
                "tool_groups": ["web"],
            },
            {
                "task": "Create workspace file docs/release_notes.md with summary.",
                "tool_groups": ["coding"],
            },
        ],
    },
    {
        "id": 74,
        "query": "Search Gmail for meeting invite from David, check my calendar for conflicts, and reply with my availability.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Search Gmail for meeting invite from David.",
                "tool_groups": ["gmail"],
            },
            {
                "task": "Check calendar for conflicts at proposed time.",
                "tool_groups": ["calendar"],
            },
            {
                "task": "Reply to David's email with availability.",
                "tool_groups": ["gmail"],
            },
        ],
    },
    {
        "id": 75,
        "query": "Open https://news.ycombinator.com, find the top story about AI, and search our memory for past mentions of that topic.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Navigate to news.ycombinator.com and extract top AI story.",
                "tool_groups": ["browser"],
            },
            {
                "task": "Search memory for past notes on top AI story topic.",
                "tool_groups": ["memory"],
            },
        ],
    },
    {
        "id": 76,
        "query": "Read the failing test log, locate the error line in app/main.py, update the code, and rerun pytest.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Read failing test log output.",
                "tool_groups": ["coding"],
            },
            {
                "task": "Locate error line in app/main.py.",
                "tool_groups": ["coding"],
            },
            {
                "task": "Update code in app/main.py to resolve error.",
                "tool_groups": ["coding"],
            },
            {
                "task": "Rerun pytest test suite.",
                "tool_groups": ["coding"],
            },
        ],
    },
    {
        "id": 77,
        "query": "Check my memory for project deadline, create a calendar event for it, and email the team a reminder.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Retrieve project deadline from memory.",
                "tool_groups": ["memory"],
            },
            {
                "task": "Create calendar event for project deadline.",
                "tool_groups": ["calendar"],
            },
            {
                "task": "Send team reminder email via Gmail.",
                "tool_groups": ["gmail"],
            },
        ],
    },
    {
        "id": 78,
        "query": "Search the web for weather in San Francisco and draft a travel recommendation email.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Search web for San Francisco weather.",
                "tool_groups": ["web"],
            },
            {
                "task": "Draft travel recommendation email response.",
                "tool_groups": [],
            },
        ],
    },
    {
        "id": 79,
        "query": "Navigate browser to staging URL, click start server, check sandbox status, and send me the preview link.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Navigate browser to staging URL and click start server button.",
                "tool_groups": ["browser"],
            },
            {
                "task": "Inspect sandbox server status.",
                "tool_groups": ["sandbox"],
            },
            {
                "task": "Obtain and return preview link.",
                "tool_groups": ["sandbox"],
            },
        ],
    },
    {
        "id": 80,
        "query": "Find the contract email in Gmail, check past memory for client budget, and draft a response.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Find contract email in Gmail.",
                "tool_groups": ["gmail"],
            },
            {
                "task": "Recall client budget details from memory.",
                "tool_groups": ["memory"],
            },
            {
                "task": "Draft contract response message.",
                "tool_groups": [],
            },
        ],
    },
    {
        "id": 81,
        "query": "Search web for PyTorch 2.0 migration guide, update requirements.txt, and run tests.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Search web for PyTorch 2.0 migration guide.",
                "tool_groups": ["web"],
            },
            {
                "task": "Update requirements.txt file in workspace.",
                "tool_groups": ["coding"],
            },
            {
                "task": "Run unit test suite.",
                "tool_groups": ["coding"],
            },
        ],
    },
    {
        "id": 82,
        "query": "Check calendar for free slots on Tuesday, schedule meeting with Mark, and email Mark the invitation.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Check calendar for free slots on Tuesday.",
                "tool_groups": ["calendar"],
            },
            {
                "task": "Create calendar meeting with Mark.",
                "tool_groups": ["calendar"],
            },
            {
                "task": "Send email invitation to Mark via Gmail.",
                "tool_groups": ["gmail"],
            },
        ],
    },
    {
        "id": 83,
        "query": "Open GitHub repository page, download latest release zip, extract it into workspace, and start dev server.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Navigate to GitHub repository page in browser.",
                "tool_groups": ["browser"],
            },
            {
                "task": "Download release zip file.",
                "tool_groups": ["browser"],
            },
            {
                "task": "Extract zip file contents into workspace.",
                "tool_groups": ["coding"],
            },
            {
                "task": "Start development server in sandbox.",
                "tool_groups": ["sandbox"],
            },
        ],
    },
    {
        "id": 84,
        "query": "Search Gmail for tax documents, download attachments, and save them in docs/taxes.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Search Gmail for tax document emails.",
                "tool_groups": ["gmail"],
            },
            {
                "task": "Download tax attachment files.",
                "tool_groups": ["gmail"],
            },
            {
                "task": "Save tax attachment files into workspace docs/taxes directory.",
                "tool_groups": ["coding"],
            },
        ],
    },
    {
        "id": 85,
        "query": "Look up user preferences in memory for color scheme, update index.css, and launch preview server.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Retrieve user color scheme preferences from memory.",
                "tool_groups": ["memory"],
            },
            {
                "task": "Update styles in index.css file.",
                "tool_groups": ["coding"],
            },
            {
                "task": "Launch sandbox preview server.",
                "tool_groups": ["sandbox"],
            },
        ],
    },
    {
        "id": 86,
        "query": "Find all unread emails from manager, summarize them, and schedule follow-up tasks on calendar.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Search Gmail for unread emails from manager.",
                "tool_groups": ["gmail"],
            },
            {
                "task": "Summarize unread email contents.",
                "tool_groups": [],
            },
            {
                "task": "Create follow-up task entries on calendar.",
                "tool_groups": ["calendar"],
            },
        ],
    },
    {
        "id": 87,
        "query": "Search web for current stock price of Apple, compare with memory historical price, and write analysis.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Search web for current Apple stock price.",
                "tool_groups": ["web"],
            },
            {
                "task": "Recall historical Apple stock price from memory.",
                "tool_groups": ["memory"],
            },
            {
                "task": "Write comparative analysis report.",
                "tool_groups": [],
            },
        ],
    },
    {
        "id": 88,
        "query": "Check calendar for dentist appointment, search Gmail for address, and open Google Maps in browser.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Check calendar for dentist appointment time.",
                "tool_groups": ["calendar"],
            },
            {
                "task": "Search Gmail for dentist office address.",
                "tool_groups": ["gmail"],
            },
            {
                "task": "Navigate to Google Maps in browser.",
                "tool_groups": ["browser"],
            },
        ],
    },
    {
        "id": 89,
        "query": "Run git pull in workspace, build project, and launch sandbox server.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Execute git pull command in workspace.",
                "tool_groups": ["coding"],
            },
            {
                "task": "Build project assets in workspace.",
                "tool_groups": ["coding"],
            },
            {
                "task": "Launch sandbox server.",
                "tool_groups": ["sandbox"],
            },
        ],
    },
    {
        "id": 90,
        "query": "Search Gmail for flight booking, extract confirmation code, and check flight status on web.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Search Gmail for flight booking email.",
                "tool_groups": ["gmail"],
            },
            {
                "task": "Search web for flight status using confirmation code.",
                "tool_groups": ["web"],
            },
        ],
    },
    {
        "id": 91,
        "query": "Recall user's default timezone from memory, list today's calendar events, and email daily schedule.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Retrieve user default timezone from memory.",
                "tool_groups": ["memory"],
            },
            {
                "task": "List today's calendar events.",
                "tool_groups": ["calendar"],
            },
            {
                "task": "Send email with daily schedule via Gmail.",
                "tool_groups": ["gmail"],
            },
        ],
    },
    {
        "id": 92,
        "query": "Check if server on port 3000 is running, inspect logs, and fix app/server.py if there are errors.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Inspect sandbox server status and logs on port 3000.",
                "tool_groups": ["sandbox"],
            },
            {
                "task": "Modify code in app/server.py to fix errors.",
                "tool_groups": ["coding"],
            },
        ],
    },
    {
        "id": 93,
        "query": "Open user dashboard on web, download monthly statement, save to workspace, and update budget spreadsheet code.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Navigate user dashboard and download statement in browser.",
                "tool_groups": ["browser"],
            },
            {
                "task": "Save downloaded statement into workspace file system.",
                "tool_groups": ["coding"],
            },
            {
                "task": "Update budget spreadsheet python code.",
                "tool_groups": ["coding"],
            },
        ],
    },
    {
        "id": 94,
        "query": "Find recent error trace in memory, search stackoverflow on web for solution, and apply fix in app/main.py.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Retrieve recent error traceback from memory.",
                "tool_groups": ["memory"],
            },
            {
                "task": "Search web for error fix on StackOverflow.",
                "tool_groups": ["web"],
            },
            {
                "task": "Apply code fix in app/main.py.",
                "tool_groups": ["coding"],
            },
        ],
    },
    {
        "id": 95,
        "query": "Search Gmail for newsletter, unsubscribe via browser link, and delete the email.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Search Gmail for newsletter email.",
                "tool_groups": ["gmail"],
            },
            {
                "task": "Open unsubscribe link in browser.",
                "tool_groups": ["browser"],
            },
            {
                "task": "Delete email message from Gmail inbox.",
                "tool_groups": ["gmail"],
            },
        ],
    },
    {
        "id": 96,
        "query": "Check calendar for team lunch, search web for nearby restaurants, and email suggestions to group.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Check calendar for team lunch event details.",
                "tool_groups": ["calendar"],
            },
            {
                "task": "Search web for nearby restaurant options.",
                "tool_groups": ["web"],
            },
            {
                "task": "Send restaurant suggestions email to team.",
                "tool_groups": ["gmail"],
            },
        ],
    },
    {
        "id": 97,
        "query": "Scan workspace files for TODO comments, save them in todo.txt, and create calendar deadlines for each.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Search workspace files for TODO comments.",
                "tool_groups": ["coding"],
            },
            {
                "task": "Write TODO items into workspace todo.txt file.",
                "tool_groups": ["coding"],
            },
            {
                "task": "Create calendar deadline events for each item.",
                "tool_groups": ["calendar"],
            },
        ],
    },
    {
        "id": 98,
        "query": "Search web for Tailwind CSS v4 features, update package.json, install dependencies, and start dev server.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Search web for Tailwind CSS v4 features.",
                "tool_groups": ["web"],
            },
            {
                "task": "Update package.json workspace file.",
                "tool_groups": ["coding"],
            },
            {
                "task": "Install project dependencies.",
                "tool_groups": ["coding"],
            },
            {
                "task": "Start sandbox development server.",
                "tool_groups": ["sandbox"],
            },
        ],
    },
    {
        "id": 99,
        "query": "Recall past project name from memory, search Gmail for related discussion, and summarize key decisions.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Retrieve project name from memory.",
                "tool_groups": ["memory"],
            },
            {
                "task": "Search Gmail for emails about project.",
                "tool_groups": ["gmail"],
            },
            {
                "task": "Summarize key project decisions.",
                "tool_groups": [],
            },
        ],
    },
    {
        "id": 100,
        "query": "Open AWS dashboard in browser, check active EC2 instances, and start sandbox local mirror server.",
        "classification": "multi",
        "tasks": [
            {
                "task": "Navigate AWS dashboard in browser to inspect EC2 instances.",
                "tool_groups": ["browser"],
            },
            {
                "task": "Start sandbox local mirror server.",
                "tool_groups": ["sandbox"],
            },
        ],
    },
]


def compute_required_tool_groups(tasks: list[dict]) -> list[str]:
    """Calculates the deduplicated, sorted union of required tool groups for a query.
    Note: Tasks with tool_groups = [] (direct assistant response) contribute no tool group."""
    groups = set()
    for task in tasks:
        for tg in task.get("tool_groups", []):
            if tg in ALLOWED_TOOL_GROUPS:
                groups.add(tg)
    return sorted(list(groups))


def enrich_dataset(dataset: list[dict]) -> list[dict]:
    """Automatically adds 'required_tool_groups' to every dataset query item."""
    for item in dataset:
        item["required_tool_groups"] = compute_required_tool_groups(item["tasks"])
    return dataset


def validate_dataset(dataset: list[dict]) -> tuple[bool, list[str]]:
    """Strictly validates the dataset against all prompt requirements."""
    errors = []

    # Rule 1: Exactly 100 records
    if len(dataset) != 100:
        errors.append(f"Expected exactly 100 records, got {len(dataset)}.")

    seen_ids = set()
    seen_queries = set()

    for idx, item in enumerate(dataset, 1):
        # Required keys
        required_keys = {"id", "query", "classification", "tasks", "required_tool_groups"}
        missing_keys = required_keys - set(item.keys())
        if missing_keys:
            errors.append(f"Item #{idx} (ID {item.get('id')}) missing keys: {missing_keys}")
            continue

        # Check unique ID
        item_id = item["id"]
        if item_id in seen_ids:
            errors.append(f"Duplicate ID found: {item_id}")
        seen_ids.add(item_id)

        # Check duplicate or empty queries
        query = item["query"].strip()
        if not query:
            errors.append(f"Item ID {item_id} has an empty query.")
        if query.lower() in seen_queries:
            errors.append(f"Item ID {item_id} has duplicate query: '{query}'")
        seen_queries.add(query.lower())

        # Classification validation
        classification = item["classification"]
        if classification not in ("single", "multi"):
            errors.append(f"Item ID {item_id} invalid classification: '{classification}'")

        tasks = item["tasks"]
        if not isinstance(tasks, list) or len(tasks) == 0:
            errors.append(f"Item ID {item_id} must have a non-empty list of tasks.")
            continue

        # Single must have 1 task, Multi must have >= 2 tasks
        if classification == "single" and len(tasks) != 1:
            errors.append(
                f"Item ID {item_id} classified as 'single' but has {len(tasks)} tasks."
            )
        elif classification == "multi" and len(tasks) < 2:
            errors.append(
                f"Item ID {item_id} classified as 'multi' but has {len(tasks)} tasks."
            )

        # Validate atomic tasks and tool groups
        for t_idx, task_obj in enumerate(tasks, 1):
            if not isinstance(task_obj, dict) or "task" not in task_obj or "tool_groups" not in task_obj:
                errors.append(f"Item ID {item_id} task #{t_idx} missing 'task' or 'tool_groups'.")
                continue
            
            tool_groups = task_obj["tool_groups"]
            if not isinstance(tool_groups, list):
                errors.append(f"Item ID {item_id} task #{t_idx} 'tool_groups' must be a list.")
                continue

            for tg in tool_groups:
                if tg not in ALLOWED_TOOL_GROUPS:
                    errors.append(
                        f"Item ID {item_id} task #{t_idx} contains invalid tool group: '{tg}'"
                    )

        # Validate required_tool_groups calculation matches ground truth tasks
        expected_required = compute_required_tool_groups(tasks)
        actual_required = item["required_tool_groups"]
        if actual_required != expected_required:
            errors.append(
                f"Item ID {item_id} 'required_tool_groups' mismatch! Expected {expected_required}, got {actual_required}"
            )

    return len(errors) == 0, errors


def generate_summary(dataset: list[dict]) -> dict:
    """Calculates dataset summary statistics for both Task Decomposition and Tool Routing."""
    total_queries = len(dataset)
    single_count = sum(1 for item in dataset if item["classification"] == "single")
    multi_count = sum(1 for item in dataset if item["classification"] == "multi")

    total_tasks = sum(len(item["tasks"]) for item in dataset)
    average_tasks = round(total_tasks / total_queries, 2) if total_queries > 0 else 0
    max_tasks = max((len(item["tasks"]) for item in dataset), default=0)

    # Tool group frequency in routing (strictly from required_tool_groups)
    tool_group_routing_freq = {tg: 0 for tg in sorted(ALLOWED_TOOL_GROUPS)}
    for item in dataset:
        for tg in item["required_tool_groups"]:
            tool_group_routing_freq[tg] += 1

    # Routing group count metrics
    no_tool_group_queries = sum(1 for item in dataset if len(item["required_tool_groups"]) == 0)
    single_tool_group_queries = sum(1 for item in dataset if len(item["required_tool_groups"]) == 1)
    multi_tool_group_queries = sum(1 for item in dataset if len(item["required_tool_groups"]) >= 2)
    max_tool_groups = max(len(item["required_tool_groups"]) for item in dataset)
    avg_tool_groups = round(sum(len(item["required_tool_groups"]) for item in dataset) / total_queries, 2)

    # Task Decomposition vs Tool Routing Matrix
    matrix = {
        "single_task_no_tool": sum(1 for item in dataset if item["classification"] == "single" and len(item["required_tool_groups"]) == 0),
        "single_task_single_tool_group": sum(1 for item in dataset if item["classification"] == "single" and len(item["required_tool_groups"]) == 1),
        "multi_task_single_tool_group": sum(1 for item in dataset if item["classification"] == "multi" and len(item["required_tool_groups"]) == 1),
        "multi_task_multi_tool_group": sum(1 for item in dataset if item["classification"] == "multi" and len(item["required_tool_groups"]) >= 2),
    }

    token_saving_multi_queries = matrix["multi_task_single_tool_group"]
    token_saving_percentage = round((token_saving_multi_queries / multi_count) * 100, 1) if multi_count > 0 else 0

    # Clean representative examples
    single_examples = [
        {
            "id": item["id"],
            "query": item["query"],
            "classification": item["classification"],
            "tasks": [t["task"] for t in item["tasks"]],
            "required_tool_groups": item["required_tool_groups"],
        }
        for item in dataset if item["classification"] == "single"
    ][:5]

    multi_single_group_examples = [
        {
            "id": item["id"],
            "query": item["query"],
            "classification": item["classification"],
            "task_count": len(item["tasks"]),
            "tasks": item["tasks"],
            "required_tool_groups": item["required_tool_groups"],
        }
        for item in dataset if item["classification"] == "multi" and len(item["required_tool_groups"]) == 1
    ][:5]

    multi_multi_group_examples = [
        {
            "id": item["id"],
            "query": item["query"],
            "classification": item["classification"],
            "task_count": len(item["tasks"]),
            "tasks": item["tasks"],
            "required_tool_groups": item["required_tool_groups"],
        }
        for item in dataset if item["classification"] == "multi" and len(item["required_tool_groups"]) >= 2
    ][:5]

    return {
        "total_queries": total_queries,
        "task_decomposition": {
            "single_task_count": single_count,
            "multi_task_count": multi_count,
            "average_tasks_per_query": average_tasks,
            "max_tasks_in_query": max_tasks,
        },
        "tool_routing": {
            "no_tool_group_count": no_tool_group_queries,
            "single_tool_group_count": single_tool_group_queries,
            "multi_tool_group_count": multi_tool_group_queries,
            "average_tool_groups_per_query": avg_tool_groups,
            "max_tool_groups_in_query": max_tool_groups,
            "tool_group_routing_frequency": tool_group_routing_freq,
        },
        "decomposition_vs_routing_matrix": matrix,
        "token_optimization_insight": {
            "multi_task_single_group_queries": token_saving_multi_queries,
            "percentage_multi_tasks_saving_tool_tokens": f"{token_saving_percentage}%",
            "description": "Multi-action user requests that consolidate down to a single tool group, saving token context by avoiding loading unnecessary tool schemas."
        },
        "examples": {
            "single_task": single_examples,
            "multi_task_single_tool_group": multi_single_group_examples,
            "multi_task_multi_tool_group": multi_multi_group_examples,
        }
    }


def main():
    print("=" * 70)
    print("🧪 OPENCLAW TASK-DECOMPOSITION & TOOL-ROUTING BENCHMARK GENERATOR")
    print("=" * 70)

    # Enrich dataset with required_tool_groups
    enrich_dataset(DATASET)

    # 1. Validate Dataset
    is_valid, errors = validate_dataset(DATASET)
    if not is_valid:
        print("❌ Dataset Validation Failed with the following errors:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    
    print("✅ Dataset passed all validation checks strictly!")

    # 2. Output task_decomposition_test.json
    output_dataset_path = Path("task_decomposition_test.json")
    with open(output_dataset_path, "w", encoding="utf-8") as f:
        json.dump(DATASET, f, indent=2, ensure_ascii=False)
    print(f"📄 Saved full dataset to: {output_dataset_path.resolve()}")

    # 3. Calculate and Output task_decomposition_summary.json
    summary = generate_summary(DATASET)
    output_summary_path = Path("task_decomposition_summary.json")
    with open(output_summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"📊 Saved evaluation summary to: {output_summary_path.resolve()}")

    # 4. Print Terminal Summary
    print("\n" + "─" * 70)
    print("📈 TERMINAL EVALUATION SUMMARY")
    print("─" * 70)
    td = summary["task_decomposition"]
    tr = summary["tool_routing"]
    matrix = summary["decomposition_vs_routing_matrix"]
    
    print("📌 1. Task Decomposition Breakdown:")
    print(f"  • Total Queries         : {summary['total_queries']}")
    print(f"  • Single-Task Queries   : {td['single_task_count']} ({td['single_task_count']/summary['total_queries']*100:.1f}%)")
    print(f"  • Multi-Task Queries    : {td['multi_task_count']} ({td['multi_task_count']/summary['total_queries']*100:.1f}%)")
    print(f"  • Average Tasks / Query : {td['average_tasks_per_query']}")
    print(f"  • Max Tasks in Query    : {td['max_tasks_in_query']}")

    print("\n📌 2. Tool Routing Breakdown (Ground Truth Required Groups):")
    print(f"  • No Tool Group (Direct): {tr['no_tool_group_count']} queries")
    print(f"  • Single Tool Group     : {tr['single_tool_group_count']} queries")
    print(f"  • Multi Tool Groups     : {tr['multi_tool_group_count']} queries")
    print(f"  • Avg Groups / Query    : {tr['average_tool_groups_per_query']}")
    print(f"  • Max Groups in Query   : {tr['max_tool_groups_in_query']}")

    print("\n📌 3. Decomposition vs Routing Matrix:")
    print(f"  • Single Task  | 0 Tool Groups   : {matrix['single_task_no_tool']}")
    print(f"  • Single Task  | 1 Tool Group    : {matrix['single_task_single_tool_group']}")
    print(f"  • Multi Task   | 1 Tool Group    : {matrix['multi_task_single_tool_group']} ⚡ (Token-saving consolidation!)")
    print(f"  • Multi Task   | 2+ Tool Groups  : {matrix['multi_task_multi_tool_group']} 🔀 (True multi-capability routing)")

    print(f"\n⚡ Token Optimization Insight: {summary['token_optimization_insight']['percentage_multi_tasks_saving_tool_tokens']} of multi-action queries require ONLY 1 tool group!")

    print("\n🛠️ Tool Group Frequency in Routing:")
    for group, count in tr["tool_group_routing_frequency"].items():
        print(f"  - {group:12s} : {count} queries")
    print("=" * 70)


if __name__ == "__main__":
    main()

