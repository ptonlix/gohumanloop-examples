# /// script
# requires-python = ">=3.10"
# dependencies = [
# "gohumanloop>=0.0.12",
# "langchain_mcp_adapters>=0.1.9",
# "langgraph>=0.5.3",
# "langchain>=0.3.26",
# "langchain-openai>=0.3.28"]
# ///
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

client = MultiServerMCPClient(
    {
        "math": {
            "url": "http://localhost:3000/mcp/",
            "transport": "streamable_http",
        },
        "weather": {
            # Make sure you start your weather server on port 8000
            "url": "http://localhost:8000/mcp/",
            "transport": "streamable_http",
        }
    }
)

async def main():
    tools = await client.get_tools()
    agent = create_react_agent("openai:deepseek-chat", tools)
    math_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
    print(f"Question: what's (3 + 5) x 12? \nMath Response: {math_response['messages'][-1].content}\n")
    weather_response = await agent.ainvoke({"messages": "what is the weather in nyc?"})
    print(f"Question: what is the weather in nyc?\nWeather Response: {weather_response['messages'][-1].content}\n")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())