from openai import OpenAI


class LLM:
    def __init__(
        self,
        model: str,
        api_key: str,
        base_url: str,
        temp: float = 0.7,
        max_new_tokens: int = 512,
    ):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.temp = temp
        self.max_new_tokens = max_new_tokens

    def prompt_builder(self, user_prompt: str):
        return f"""
                {user_prompt}
                """

    def generate_response(self, messages: list, context: str = ""):
        """Streams a response from the model.
        Args:
            messages (list): Conversation history.
            context (str): Retrieved context to ground the answer.
        Yields:
            str: Chunks of the generated response.
        """
        messages = list(messages)  # avoid mutating the caller's list
        if context:
            messages.insert(
                0,
                {
                    "role": "system",
                    "content": "use only the following information to answer the question:\n "
                    + context,
                },
            )

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_new_tokens,
            temperature=self.temp,
            top_p=0.95,
            stream=True,
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
