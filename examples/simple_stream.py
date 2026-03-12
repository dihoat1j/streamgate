import asyncio
from streamgate.providers.openai import OpenAIProvider

async def main():
    # Example of direct provider usage
    provider = OpenAIProvider(
        name="test-provider",
        api_key="your-key-here",
        base_url="https://api.openai.com/v1"
    )
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Tell me a joke"}],
        "stream": True
    }
    
    print("Streaming response:")
    async for chunk in provider.stream_chat(payload):
        print(chunk, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
