import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from model.schema import SubClaim

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY')

decomposer_model = ChatOpenAI(model='gpt-4o-mini', temperature=0)
decomposer_model = decomposer_model.with_structured_output(SubClaim)