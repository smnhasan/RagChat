

def get_chat_prompt(text: str) -> str:
    """Get prompt template for llm"""
    prompt_template = f"""<|start_header_id|>user<|end_header_id|>

{text}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>\n"""
    return prompt_template