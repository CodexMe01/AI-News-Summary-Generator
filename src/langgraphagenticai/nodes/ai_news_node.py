from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
import os
import logging
from requests.exceptions import SSLError

logger = logging.getLogger(__name__)


class AiNewsNode:
    def __init__(self, llm):
        """Initialize the AINewsNode with Tavily client and an LLM instance."""
        try:
            self.tavily = TavilyClient()
        except Exception:
            logger.exception("Failed to initialize TavilyClient")
            self.tavily = None

        self.llm = llm
        self.state = {}

    def _extract_frequency(self, state: dict) -> str:
        messages = state.get("messages") or []
        if not messages:
            return "daily"

        last = messages[-1]
        text = ""
        try:
            if isinstance(last, dict):
                text = last.get("content") or last.get("message") or str(last)
            elif hasattr(last, "content"):
                text = getattr(last, "content")
            else:
                text = str(last)
        except Exception:
            text = str(last)

        token = text.strip().lower().split()[0] if text else "daily"
        if token not in ("daily", "weekly", "monthly", "year"):
            token = "daily"
        return token

    def fetch_news(self, state: dict) -> dict:
        frequency = self._extract_frequency(state)
        self.state["frequency"] = frequency

        time_range_map = {"daily": "d", "weekly": "w", "monthly": "m", "year": "y"}
        days_map = {"daily": 1, "weekly": 7, "monthly": 30, "year": 366}

        if not self.tavily:
            state["news_data"] = []
            state["error"] = "Tavily client not initialized"
            self.state["news_data"] = []
            self.state["error"] = state["error"]
            return state

        try:
            response = self.tavily.search(
                query="All Breaking News",
                topic="news",
                time_range=time_range_map[frequency],
                include_answer="advanced",
                max_result=1,
                days=days_map[frequency],
            )
            results = response.get("results", []) if isinstance(response, dict) else []

        except SSLError as e:
            logger.exception("Tavily SSL error while fetching news")
            state["news_data"] = []
            state["error"] = f"Tavily SSL error: {e}"
            self.state["news_data"] = []
            self.state["error"] = state["error"]
            return state

        except Exception as e:
            logger.exception("Unexpected error while fetching news from Tavily")
            state["news_data"] = []
            state["error"] = str(e)
            self.state["news_data"] = []
            self.state["error"] = state["error"]
            return state

        state["news_data"] = results
        self.state["news_data"] = results
        return state

    def summerize_news(self, state: dict) -> dict:
        # kept the name `summerize_news` to match graph registration
        news_items = self.state.get("news_data", [])

        # Use a plain string prompt template to avoid depending on ChatPromptTemplate API
        prompt_template = (
            "Summarize All Breaking news articles into markdown format. For each item include:\n"
            "- Date in **YYYY-MM-DD** format (IST)\n"
            "- A concise 10 words Heading\n"
            "- A concise 60 words summary\n"
            "- Sort news by time (latest first)\n"
            "- Source URL as a link\n\n"
            "Article:\n{articles}"
        )

        articles_lines = []
        for item in news_items:
            content = item.get("content", "") if isinstance(item, dict) else str(item)
            url = item.get("url", "") if isinstance(item, dict) else ""
            date = item.get("published_date", "") if isinstance(item, dict) else ""
            articles_lines.append(f"Content: {content}\nURL: {url}\nDate: {date}")

        articles_str = "\n\n".join(articles_lines)

        try:
            llm_input = prompt_template.format(articles=articles_str)
            if hasattr(self.llm, "invoke"):
                response = self.llm.invoke(llm_input)
            elif hasattr(self.llm, "chat"):
                response = self.llm.chat(llm_input)
            else:
                response = self.llm(llm_input)

            summary_text = getattr(response, "content", None) or (response if isinstance(response, str) else str(response))
        except Exception as e:
            logger.exception("LLM summarization failed")
            summary_text = ""
            state["error"] = f"LLM summarization error: {e}"

        state["summary"] = summary_text
        self.state["summary"] = summary_text
        return state

    def save_results(self, state: dict) -> dict:
        frequency = self.state.get("frequency", "daily")
        summary = self.state.get("summary", "")
        out_dir = os.path.join(os.getcwd(), "AINews")
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"{frequency}_summary.md")
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"*{frequency.capitalize()} AI News Summary\n\n")
                f.write(summary or "")
            self.state["filename"] = filename
            state["filename"] = filename
        except Exception:
            logger.exception("Failed to write AI News summary file")
            state["error"] = "Failed to save results to disk"

        return state
        
