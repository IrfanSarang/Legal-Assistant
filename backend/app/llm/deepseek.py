import requests

DEESEEK_URL = "http://127.0.0.1:1234/v1/responses"  # LM Studio local endpoint

def send_to_deepseek(prompt: str) -> str:
    """
    Send the prompt to DeepSeek LLM in chat format and get an answer.
    """
    payload = {
        "model": "deepseek-r1-distill-qwen-7b",
        "input": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 512
    }

    try:
        response = requests.post(DEESEEK_URL, json=payload)
        response.raise_for_status()
        data = response.json()

        # LM Studio returns 'output' as a list of messages
        if "output" in data and isinstance(data["output"], list):
            for item in data["output"]:
                if item.get("type") == "message" and "content" in item:
                    return item["content"]
            return "No text output in LLM response."
        else:
            return f"Unexpected response format: {data}"

    except requests.exceptions.HTTPError as e:
        return f"HTTP Error from LLM: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error calling LLM: {str(e)}"
