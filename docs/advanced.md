# Optional integrations

Start with the default HTTP profile. Add optional `browser` and `parser` Compose profiles only when needed; read compose.yaml and deployment.md for their independent keys, networks and memory constraints. The bundled signed browser worker is included; the standalone HoundBrowser session API uses a separate protocol.

For S3 set the documented HOUNDCRAWLER_STORAGE URI and use your own workload identity/credentials. For Gemini/OpenAI-compatible/Vertex extraction configure an explicit supported model, your own key or ADC identity, and current operator-supplied pricing with provenance. Never assume a model exists because a label appears in an example. No model, search or cloud credentials ship with this repository.

Run `houndcrawler mcp` with HOUNDCRAWLER_ENDPOINT and HOUNDCRAWLER_API_KEY to expose tools over stdio. It calls REST and returns untrusted source data. It has no internal shell/database/CDP privileges. Optional profiles have their own qualification workflows and are not part of default HTTP test claims.
