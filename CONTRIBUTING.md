# Contributing to ResQ-Edge Agent

This is an experimental AI assistant. Contributions must preserve human control and safety boundaries.

## Safety requirements

- Do not add autonomous flight, navigation, payload, or actuation behavior without a separate safety review and explicit project scope.
- Model output must never be treated as authoritative emergency guidance.
- Use simulated or authorized test telemetry; do not commit sensitive mission logs or personal data.
- Preserve a human verification step for all operational recommendations.

## Development expectations

- Add request timeouts and clear handling for Ollama unavailable/model missing responses.
- Validate prompt and telemetry sizes and structure.
- Restrict CORS and add authentication before network exposure.
- Keep model names and service URLs configurable through server-side settings.
- Add tests for malformed requests, model errors, and telemetry edge cases.
- Keep the Agent Skill description synchronized with tools that are actually implemented.

## Pull requests

Include the safety impact, test data source, commands run, failure cases considered, and known limitations. Do not describe a feature as field-ready without controlled validation and approval.
