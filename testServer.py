from fastapi import Body
import requests

url = "http://localhost:8000/createposts"

data  = {
    "title": "my title posts",
    "content": "my content post"
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.text)