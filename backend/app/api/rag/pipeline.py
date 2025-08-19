from .models.llm import LlamaModel, ModelConfig, get_chat_messages


class Pipeline:
    def __init__(self):
        
        config = ModelConfig()
        self.llm = LlamaModel(config)
        
        
    def generate(self, query):
        """
        Generate a response based on the provided query using the LLM.

        Args:
            query (str): The input query to generate a response for.

        Returns:
            str: The generated response.
        """
        messages = get_chat_messages(query)
        res = self.llm.generate_with_chat_template(messages)

        return self.llm.generate(res)
        