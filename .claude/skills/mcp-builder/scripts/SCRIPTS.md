# Scripts Documentation

This directory contains executable scripts for the **mcp-builder** skill.

## Scripts Overview

| Script | Purpose | Status |
|--------|---------|--------|
| `connections.py` | Manage MCP server connections | Production |
| `evaluation.py` | Evaluate MCP tool implementations | Production |

---

## connections.py

**Purpose:** Manages MCP (Model Context Protocol) server connections, including registration, testing, and configuration.

### Usage

```bash
python3 connections.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Server config or connection URL |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Capabilities

- Register new MCP servers
- Test server connectivity
- List available tools
- Validate server schemas
- Generate connection configs

---

## evaluation.py

**Purpose:** Evaluates MCP tool implementations for correctness, performance, and best practices compliance.

### Usage

```bash
python3 evaluation.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | MCP server or tool config |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Evaluation Criteria

- Tool schema validation
- Response format correctness
- Error handling
- Performance benchmarks
- Security best practices

### Dependencies

All scripts require Python 3.8+ (stdlib only)
