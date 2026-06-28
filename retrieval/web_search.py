"""Retrieval logic for web documents"""

from langchain_tavily import TavilySearch

from dotenv import load_dotenv
import os

load_dotenv()
os.environ['TAVILY_API_KEY'] = os.environ.get('TAVILY_API_KEY')

web_search = TavilySearch(max_results=1, include_images=False)
