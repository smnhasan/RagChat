from datetime import datetime


def get_chat_prompt(user_input, history=[], context=None):
    today_date = datetime.today().strftime("%d %B %Y")  

    prompt = (
        "<|start_header_id|>system<|end_header_id|>\n\n"
        f"Cutting Knowledge Date: December 2023\n"
        f"Today Date: {today_date}\n\n"
        "You are a helpful news reporter bot. You do not have specific name. If user asks about basic chit-chat, reply them. DO NOT provide information which is not present on the Retrieved Context. If there is no information about the question on the context just say 'I do not know about it'. Provide precise response.\n"
    )

    # Add retrieved context if available
    if context:
        prompt += "\nRetrieved Context:\n" + context + "\n"

    prompt += "<|eot_id|>"

    # Append chat history
    for role, message in history:
        prompt += f"<|start_header_id|>{role}<|end_header_id|>\n\n{message}<|eot_id|>"

    # Append current user input
    prompt += f"<|start_header_id|>user<|end_header_id|>\n\n{user_input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"

    return prompt



def get_standalone_query_generation_prompt(user_input, history):
    prompt = (
        "<|start_header_id|>system<|end_header_id|>\n\n"
        "Think step-by-step. Write the standalone query of the last user message so that it contains all the information of this question and best suited for context retrieval. Just write the query in detailed form. DO NOT write any extra explanation. DO NOT write the answer.\n"
    )

    prompt += "<|eot_id|>"

    # Append chat history
    for role, message in history:
        prompt += f"<|start_header_id|>{role}<|end_header_id|>\n\n{message}<|eot_id|>"

    # Append current user input
    prompt += f"<|start_header_id|>user<|end_header_id|>\n\n{user_input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\nStandalone Query: (Standalone Query should be in detailed form. DO NOT Answer the query here.)\n\n"

    return prompt
