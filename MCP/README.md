# GoHumanLoop Example with MCP

> MCP stands for Model Context Protocol

This example shows how to use the GoHumanLoop package to create a MCP agent that augments human control.

## Example List

- MCP Server Example

  - [Math Server](MCP/mcp_mcp_server.py)
  - [Weather Server](MCP/mcp_weather_server.py)

- MCP Client Example
  - [LangChain Client](MCP/mcp_langchain_client.py)

## Start

1. Install uv

Go to installation guide: https://github.com/astral-sh/uv

2. Run MCP Server

```bash
uv run mcp_math_server.py
uv run mcp_weather_server.py  # Optional
```

> `mcp_weather_server` depends on the Feishu server. You can refer to the [gohumanloop-feishu](https://github.com/ptonlix/gohumanloop-feishu) project to set up the Feishu server

3. Run MCP Client

```bash
uv run mcp_langchain_client.py
```

4. Check math server where approval are received

5. Input 'approve' or 'reject' to respond to the request

6. [Optional] Check weather server (Feishu) where approval are received

7. Wait for `langchain_client` to return results

## License

This project is released under the MIT License.
