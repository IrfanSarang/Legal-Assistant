import requests


class DeepSeekLLM:

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:1234/v1/responses",
        model: str = "deepseek-r1-distill-qwen-7b"  # Ideally switch to instruct model
    ):
        self.base_url = base_url
        self.model = model

    def generate(
        self,
        prompt: str,
        max_tokens: int = 200,
        temperature: float = 0.1,
        top_p: float = 0.8
    ) -> str:

        payload = {
            "model": self.model,
            "input": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p
        }

        try:
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status()
            data = response.json()

            # 🔹 Robust parsing for LM Studio response format
            if "output" in data and isinstance(data["output"], list):
                for item in data["output"]:
                    if item.get("type") == "message":
                        content = item.get("content", [])
                        if isinstance(content, list):
                            return "".join(
                                part.get("text", "") for part in content
                            ).strip()

            return "Unexpected response format."

        except requests.exceptions.RequestException as e:
            return f"LLM Request Error: {str(e)}"

        except Exception as e:
            return f"LLM Processing Error: {str(e)}"