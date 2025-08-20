from .models.llm import LLM
from .prompts import get_chat_prompt
from .retriever import Retriever

class Pipeline:
    def __init__(self):
        self.llm = LLM()
        self.retriever = Retriever()

    def run(self, query):
        # Process the query using the rag service
        
        docs = self.retriever.retrieve(query)        
        print(f"Retrieved documents: {docs}")
        
        prompt = get_chat_prompt(query)
        llm_response = self.llm.generate([prompt])
        text = llm_response.flatten()

        if not text or not text[0].generations:
            return "I'm sorry, I couldn't generate a response. Please try again."

        generated_text = text[0].generations[0][0].text
        return generated_text.replace('"', "")        

        return response