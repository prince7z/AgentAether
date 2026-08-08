import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from app.agent.router import route_tools_for_query, decompose_query_to_tasks, TOOL_GROUP_MAP

TEST_QUERIES = [
    "hello",
    "tell me a joke",
    "how are you?",
    "thank you!",
    "make a portfolio start the server and send the preview link",
    "Search my Gmail for the invoice and save the attachment.",
    "Check my calendar and email me the available times.",
    "Find the bug, fix it, and run the tests.",
    "Look up Next.js release notes on the web and email team@example.com",
    "Open Google in browser and search for news",
    "What is the capital of France?"
]

print("=" * 80)
print("🧪 TESTING DYNAMIC TOOL ROUTER INTEGRATION WITH BGE RERANKER")
print("=" * 80)

for q in TEST_QUERIES:
    tasks = decompose_query_to_tasks(q)
    routed_tools, groups = route_tools_for_query(q)
    
    print(f"\nUser Query : '{q}'")
    print(f"Decomposed : {tasks}")
    print(f"Groups     : {groups}")
    print(f"Tools Bound: {len(routed_tools)} / 27 total tools")
    tool_names = [getattr(t, "name", str(t)) for t in routed_tools]
    print(f"Tool Names : {tool_names[:6]}{'...' if len(tool_names) > 6 else ''}")
    print("-" * 75)

print("\n✅ Router integration test script completed.")
