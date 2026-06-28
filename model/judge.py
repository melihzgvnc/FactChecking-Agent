from langchain_ollama import ChatOllama
from model.schema import ClaimCheck

judge_model = ChatOllama(
    model='qwen3-dpo-q5-gguf',
    base_url="http://localhost:11434",
    reasoning=False,
    temperature=0
)
judge_model = judge_model.with_structured_output(ClaimCheck)