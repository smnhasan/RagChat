import requests

# Make sure the query parameter is sent in the URL
url = "http://127.0.0.1:8000/api/chat/stream"
params = {"query": "Hello streaming world"}  # must match 'query'

with requests.get(url, params=params, stream=True) as response:
    for line in response.iter_lines():
        if line:
            decoded = line.decode("utf-8")
            if decoded == "data: [DONE]":
                print("\nStreaming complete!")
                break
            print(decoded.replace("data: ", ""), end="", flush=True)

