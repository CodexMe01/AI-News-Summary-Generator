import sys
import os
# Ensure project root is on sys.path for imports when running from scripts/
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.langgraphagenticai.nodes.ai_news_node import AiNewsNode

class MockResponse:
    def __init__(self, content):
        self.content = content

class MockLLM:
    def invoke(self, prompt):
        # return an object with a `content` attribute like real LLM wrappers
        return MockResponse("# Sample Summary\n\n- 2025-10-13\n- This is a mocked summary for testing. (source)")

class FakeTavily:
    def search(self, **kwargs):
        return {"results": [
            {"content": "AI breakthrough in sample test.", "url": "https://example.com/article1", "published_date": "2025-10-13"},
            {"content": "Another AI story.", "url": "https://example.com/article2", "published_date": "2025-10-12"}
        ]}


def run_test():
    llm = MockLLM()
    node = AiNewsNode(llm)
    # inject fake tavily client so fetch_news returns data
    node.tavily = FakeTavily()

    state = {"messages": ["weekly"]}
    state = node.fetch_news(state)
    print("After fetch_news: news count=", len(state.get("news_data", [])))
    state = node.summerize_news(state)
    print("After summerize_news: summary exists=", bool(state.get("summary")))
    state = node.save_results(state)
    print("Saved filename=", state.get("filename"))

    # Print file contents
    if "filename" in state:
        with open(state["filename"], "r", encoding="utf-8") as f:
            print("--- FILE CONTENT START ---")
            print(f.read())
            print("--- FILE CONTENT END ---")

if __name__ == '__main__':
    run_test()
