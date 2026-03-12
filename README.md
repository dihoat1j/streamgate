# StreamGate

StreamGate is a high-performance, real-time LLM proxy designed to provide a unified interface for multiple AI providers (OpenAI, Anthropic, Azure) with built-in load balancing, streaming support, and automatic fallback routing.

## Features

*   **Real-time Streaming**: Full support for Server-Sent Events (SSE) to stream LLM responses.
*   **Load Balancing**: Distribute traffic across multiple API keys or providers using Round Robin or Latency-aware strategies.
*   **Automatic Failover**: If a provider returns a 5xx error or hits rate limits, StreamGate automatically reroutes the request to a healthy backup.
*   **Unified API**: OpenAI-compatible endpoint structure.
*   **Health Monitoring**: Continuous tracking of provider latency and availability.

## Architecture

StreamGate sits between your application and the LLM providers. It intercepts requests, selects the best available provider based on health and priority, and pipes the stream back to the client with minimal overhead.

[Client] -> [StreamGate Proxy] -> [Load Balancer] -> [Provider A / B / C]

## Installation

```bash
pip install -e .
```

## Usage

1. Configure your providers in `config.yaml`:

```yaml
providers:
  - name: openai-primary
    type: openai
    api_key: ${OPENAI_API_KEY}
    weight: 10
  - name: azure-backup
    type: azure
    api_key: ${AZURE_API_KEY}
    endpoint: https://my-resource.openai.azure.com/
```

2. Start the gateway:

```bash
uvicorn streamgate.main:create_app --host 0.0.0.0 --port 8000
```

3. Send a request:

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": true
  }'
```

## Development

Run tests using pytest:
```bash
pytest tests/
```

## License

MIT
