from langgraph.graph import StateGraph
from src.langgraphagenticai.state.state import State
from langgraph.graph import START,END

from src.langgraphagenticai.tools.search_tool import get_tools,create_tool_node
from langgraph.prebuilt import tools_condition,ToolNode

from src.langgraphagenticai.nodes.ai_news_node import AiNewsNode

class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(State)

    
    def ai_news_builder_graph(self):
        ai_news_node = AiNewsNode(self.llm)

        # nodes
        # Register actual callables from the AiNewsNode instance
        self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news)
        # Support both spellings: `summerize_news` (existing) and `summarize_news` (common)
        if hasattr(ai_news_node, "summerize_news"):
            summary_fn = ai_news_node.summerize_news
        elif hasattr(ai_news_node, "summarize_news"):
            summary_fn = ai_news_node.summarize_news
        else:
            # register a wrapper that raises a clear error during execution
            def summary_fn(state):
                raise AttributeError("AiNewsNode missing 'summerize_news'/'summarize_news' method")

        self.graph_builder.add_node("summerize_news", summary_fn)
        self.graph_builder.add_node("save_results", ai_news_node.save_results)

        # edges
        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summerize_news")
        self.graph_builder.add_edge("summerize_news", "save_results")
        self.graph_builder.add_edge("save_results", END)
        

    
    def setup_graph(self, usecase: dict):
        """
        Sets up the graph for the selected use case.
        """
        
        if usecase == "AI News":
            self.ai_news_builder_graph()

        return self.graph_builder.compile()
