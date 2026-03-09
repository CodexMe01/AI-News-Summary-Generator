import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
from src.langgraphagenticai.nodes.ai_news_node import AiNewsNode
import json


class DisplayResultStreamlit:
    def __init__(self,usecase,graph,user_message):
        self.usecase= usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase= self.usecase
        graph = self.graph
        user_message = self.user_message
        print(user_message)
        
        if usecase=="AI News":
             # Prepare state and invoke the graph
            frequency = self.user_message
            with st.spinner("Fetching and summarizing news..."):
                # Graph expects `messages` per the project's State TypedDict
                result = graph.invoke({"messages": [frequency]})
                try:
                    # READ MARKDOWN FILE
                    AI_NEWS_PATH = f"./AINews/{frequency.lower()}_summary.md"
                    with open(AI_NEWS_PATH, "r") as file:
                        markdown_content = file.read()
                        

                    # Display the markdown content is streamlit
                    st. markdown(markdown_content, unsafe_allow_html = True)
                except FileNotFoundError:
                    st.error(f"News not Generated or File Not found: {AI_NEWS_PATH}")
                except Exception as e:
                    st.error(f"An error occured: {str(e)}")