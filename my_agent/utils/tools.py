from langchain_community.tools.tavily_search import TavilySearchResults
import os

tavily_api_key='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'
tools = [TavilySearchResults(max_results=1,tavily_api_key=tavily_api_key)]