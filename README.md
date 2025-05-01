# basic_cursor_rag

A simple CLI-based AI coding assistant. It processes natural language commands to generate projects with real code, execute shell commands, and write files. The assistant leverages the Gemini API (via an OpenAI-compatible wrapper) and integrates Langfuse for tracing.

## Features

- Convert natural language queries into code actions.
- Execute shell commands (`run_command`) and write files (`write_file`).
- Auto-detects OS and project root for command context.
- Tracing and observability with Langfuse.
