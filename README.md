# Document AST Parser & Compiler Skill for Autonomous Agents

[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-blue.svg)](https://modelcontextprotocol.io)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-brightgreen.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero External Dependencies](https://img.shields.io/badge/dependencies-zero-success.svg)](requirements.txt)

Enterprise Document Abstract Syntax Tree (AST) engine enabling autonomous agents to parse unstructured markdown documents into structured AST nodes and serialize nodes back into standard formatting.

## Core Capabilities
- **Hierarchical Node Extraction**: Accurately recognizes headings (H1-H6), nested lists, markdown tables, and code blocks.
- **Bi-directional Compilation**: Deconstructs raw markdown to AST and serializes modified AST back to clean canonical text.
- **Zero Third-Party Dependencies**: Pure Python standard library implementation.

## MCP Server Integration
Run standard stdio MCP server:
```bash
python mcp_server.py
```

### Available MCP Tools
- `parse_markdown_ast`: Parse markdown string into structured AST node list.
- `compile_ast_markdown`: Serialize AST node array back into formatted markdown.
