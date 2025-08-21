from .models.llm import LLM
from .prompts import get_chat_prompt, get_standalone_query_generation_prompt
from .retriever import Retriever

class Pipeline:
    def __init__(self):
        self.llm = LLM()
        self.retriever = Retriever()
        self.history = []

    def run(self, query):
        # Process the query using the rag service
                
        if self.history:
            prompt = get_standalone_query_generation_prompt(query, history=self.history)
            standalone_query = self.llm.generate_response(prompt)
            print(f"Standalone Query: {standalone_query}")
        else:
            standalone_query = query
        
        
        context = self.retriever.retrieve(standalone_query)        
        print(f"Retrieved context: {context}")
        
        prompt = get_chat_prompt(query, history=self.history, context=context)     
        response = self.llm.generate_response(prompt)
        self.history.append(("user", query))
        self.history.append(("assistant", response))
        
        return response
    
    
    