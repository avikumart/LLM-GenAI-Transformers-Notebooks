import requests
import json
import os

url = "https://api.cortex.cerebrium.ai/v4/p-b38f562d/llama-deploy/predict"

payload = json.dumps({"prompt": "What is the value of gravity?"})

headers = {
  'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJwcm9qZWN0SWQiOiJwLWIzOGY1NjJkIiwiaWF0IjoxNzQ2NzAzNzAxLCJleHAiOjIwNjIyNzk3MDF9.bakKJlyTtwq_KR997Uh8vnO7NjkPJCJDtqTML4Q21i-rA9zZpuIbAYla5ikgkNcwQo8pHSbF8plcvkNspeqXAnMnwpzMhr7ZKSYvQ9PmIngmlFajCg4us9Ug1DBzDK-2Y0tazncsNnCoAX6HeWSt3p8V9lGFiUCoBZhJw2sb5f97IgJH-bHrWtMCYdb07C9ZecSZKTYIrmkijOLhkWInXIllyn8jjkwH1pnn6eOdsNMcjGmQxqBXn9GO69fe6cKFhsJjvy0wFHWt-X8lYPC9PGCnosUk_2qUEScZ-HUhK6YrzPAzpF7nr5Iv8qboUE-bKHwLMBKRT5dXQDmdJejJZw',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)