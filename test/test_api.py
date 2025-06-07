import requests

payload = {
    "question": "What tools are used in data analysis?",
    "image": None
}

res = requests.post("http://localhost:8000/api/", json=payload)
print(res.json())
