from .models.llm import LLM 
from prompts import get_chat_prompt


class Pipeline:
    def __init__(self):        
        self.llm = LLM
        
        
    def generate(self, query):
        """
        Generate a response based on the provided query using the LLM.

        Args:
            query (str): The input query to generate a response for.

        Returns:
            str: The generated response.
        """
        
        prompt = get_chat_prompt(query)
        llm_response = self.llm.generate([prompt])
        text = llm_response.flatten()

        if not text or not text[0].generations:
            return "I'm sorry, I couldn't generate a response. Please try again."

        generated_text = text[0].generations[0][0].text
        return generated_text.replace('"', "")

        return self.llm.generate(res)
        