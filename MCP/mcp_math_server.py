# /// script
# requires-python = ">=3.10"
# dependencies = [
# "gohumanloop>=0.0.12",
# "fastmcp>=2.6.0"]
# ///
from fastmcp import FastMCP, Client
from gohumanloop import DefaultHumanLoopManager, HumanloopAdapter, TerminalProvider

# 设置环境变量

# 创建 GoHumanLoopManager 实例
manager = DefaultHumanLoopManager(
    TerminalProvider(name="TerminalProvider")
)
# 创建 LangGraphAdapter 实例
adapter = HumanloopAdapter(
    manager=manager,
    default_timeout=600,  # 默认超时时间为10分钟
)

mcp = FastMCP(name="CalculatorServer")

@mcp.tool()
@adapter.require_approval()
async def add(a: int, b: int,) -> int:
    """Adds two integer numbers together."""
    return a + b

@mcp.tool()
@adapter.require_approval()
async def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b


@mcp.tool(exclude_args=["huamninfo"])
@adapter.require_info(ret_key="huamninfo")
async def feedback(add_result: int, huamninfo: dict={}) -> str:
    """Gets feedback from human response.
    Args:
        add_result: The result from previous addition operation
    Returns:
        The human response string
    """

    print(f"Get Human Response: {huamninfo}")
    info = huamninfo["response"]

    return info


if __name__ == "__main__":
    # This runs the server, defaulting to STDIO transport
    mcp.run(transport="streamable-http", port=3000)

    # client = Client(mcp)

    # async def call_tool(name: str):
    #     async with client:
    #         print(await client.list_tools())
    #         result = await client.call_tool("add", {"a": 1, "b": 2})
    #         print(result)
    #         result = await client.call_tool("feedback", {"add_result": result[0].text})

    # asyncio.run(call_tool("Ford"))