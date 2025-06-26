import random
import pandas as pd

# use openrouter api to get multiple model responses
def get_openrouter_responses(prompt, model="gpt-4", num_responses=3):
    url = f"https://api.openrouter.com/v1/models/{model}/generate"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    responses = []
    for _ in range(num_responses):
        response = requests.post(url, headers=headers, json={"prompt": prompt})
        if response.status_code == 200:
            responses.append(response.json())
        else:
            print(f"Error: {response.status_code}")
    return responses
