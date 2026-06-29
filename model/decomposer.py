import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from model.schema import SubClaim
import openai

load_dotenv()

decomposer_model = ChatOpenAI(model='gpt-4o-mini', temperature=0)
decomposer_model = decomposer_model.with_structured_output(SubClaim).with_retry(
    retry_if_exception_type = (openai.APITimeoutError, openai.APIConnectionError,
    openai.RateLimitError, openai.InternalServerError),
    stop_after_attempt = 3
)