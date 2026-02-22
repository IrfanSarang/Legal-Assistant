import requests


class DeepSeekLLM:

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:1234/v1/responses",
        model: str = "deepseek-r1-distill-qwen-7b"
    ):
        self.base_url = base_url
        self.model = model

    def generate(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.0):

        payload = {
            "model": self.model,
            "input": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        try:
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status()
            data = response.json()

            if "output" in data:
                return data["output"][0]["content"][0]["text"].strip()

            return "Unexpected response format."

        except Exception as e:
            return f"Error calling LLM: {str(e)}"