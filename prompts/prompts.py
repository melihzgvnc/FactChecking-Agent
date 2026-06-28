"""Prompts for LLMs"""

DECOMPOSER_PROMPT = """
You are a helpful assistant. 
You are given a raw claim and your task is to extract sub-claims from that.

Here is the claim:
<claim>{raw_claim}</claim>

Extract sub-claims from it and return them as a list.
"""

JUDGE_PROMPT = """Check the claim against the evidence passage and decide if it is supported, refuted or insufficient evidence.
IMPORTANT: You are not expected to answer a question but review a claim against a context.
IMPORTANT: You return the grounding sentence that supports your verdict. Return None if it is insufficient evidence.
IMPORTANT: Return a confidence score reflecting how strongly the passage supports your verdict.

<claim>{sub_claim}</claim>

<evidence_passage>{evidence}</evidence_passage>
"""