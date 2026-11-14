# ResQ-Edge Agent

An offline-first AI co-pilot and agent-skill prototype for emergency-response drone workflows.

## Model

- **Model family:** Gemma 2 9B through [Ollama](https://ollama.com)
- **Model terms:** [Google Gemma Terms](https://ai.google.dev/gemma/terms)

The model runs locally. Hardware requirements depend on the model quantization and runtime configuration.

## Prerequisites

- Python
- [Ollama](https://ollama.com)
- The configured Gemma model available locally

## Run locally

Start the model in one terminal:

```bash
ollama run gemma2:9b
```

In a second terminal, from the repository root, start the agent API:

```bash
python agent/server.py
```

Install the project's declared Python dependencies if the server reports missing packages. Check the source and configuration for any additional environment variables or setup steps.

## Responsible use

This is a prototype to support emergency-response workflows. It must not replace trained incident commanders, pilots, emergency services, or established operating procedures. Verify generated recommendations before acting on them.

## License

See [LICENSE](LICENSE) for the software license. The model is governed separately by Google's Gemma terms.
