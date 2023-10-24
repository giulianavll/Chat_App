import requests

API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-alpha"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
# messages = [
#     {
#         "role": "system",
#         "content": "You are a friendly chatbot who always responds in the style of a pirate",
#     },
#     {"role": "user", "content": "How many helicopters can a human eat in one sitting?"},
# ]
messages={"inputs":[{
        "role": "system",
        "content": "You are a friendly chatbot who always responds in the style of a pirate",
    },
    {"role": "user", "content": "How many helicopters can a human eat in one sitting?"},]}
output = query(
	messages
)
print(output)