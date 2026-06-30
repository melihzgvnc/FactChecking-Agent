from langchain_ollama import ChatOllama
from model.schema import ClaimCheck
from pydantic import ValidationError
from langchain_core.exceptions import OutputParserException
from functools import lru_cache

@lru_cache(maxsize=1)
def get_judge_model():
    judge_model = ChatOllama(
        model='qwen3-dpo-q5-gguf',
        base_url="http://localhost:11434",
        reasoning=False,
        temperature=0
    )
    return judge_model.with_structured_output(ClaimCheck).with_retry(
        retry_if_exception_type = (ValidationError, OutputParserException),
        stop_after_attempt = 3
    )