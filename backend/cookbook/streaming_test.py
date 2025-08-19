# test_sse_stream.py
import requests

def stream_chat(query: str):
    # Use the public domain via Nginx
    url = "https://chatbot.staging.nascenia.com/api/chat/stream"
    params = {"query": query}

    with requests.get(url, params=params, stream=True) as response:
        if response.status_code != 200:
            print(f"Failed to connect: {response.status_code}")
            return

        print("Streaming response:")
        for line in response.iter_lines():
            if line:
                decoded = line.decode("utf-8")
                if decoded.strip() == "data: [DONE]":
                    print("\nStreaming complete!")
                    break
                # Remove "data: " prefix and print tokens
                print(decoded.replace("data: ", ""), end="", flush=True)

if __name__ == "__main__":
    query_text = input("Enter your query: ")
    stream_chat(query_text)
