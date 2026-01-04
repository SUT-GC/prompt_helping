# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

JSON Prompt Converter - A tool that converts natural language prompts into structured JSON prompting format using Doubao (豆包) API. It consists of a Python proxy server and a frontend HTML page.

## Architecture

- **server.py**: Python HTTP proxy server (zero dependencies, uses only stdlib). Handles CORS and forwards requests to Doubao API (`https://ark.cn-beijing.volces.com/api/v3`). Proxies `/v1/*` endpoints.
- **index.html**: Single-page frontend application with embedded CSS and JavaScript. Provides UI for input/output, API key management, and template selection for different output types (image, video, infographic, content, data extraction, code generation).

## Commands

### Start the server
```bash
python server.py
```

### Start on custom port
```bash
PORT=8080 python server.py
```

The server runs on port 3000 by default. Health check endpoint: `/health`

## Key Implementation Details

- The proxy server is intentionally dependency-free, using only Python 3.7+ standard library
- API keys are stored in browser localStorage and passed via `Authorization: Bearer <key>` header through the proxy
- The frontend uses OpenAI-compatible API format with `doubao-seed-1-8-251215` model
- System prompt in `index.html` defines JSON schema templates for each output type
