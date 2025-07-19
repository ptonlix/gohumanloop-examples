# /// script
# requires-python = ">=3.10"
# dependencies = [
# "gohumanloop>=0.0.12",
# "fastmcp>=2.6.0"]
# ///
from fastmcp import FastMCP
from gohumanloop import DefaultHumanLoopManager, HumanloopAdapter, APIProvider,  get_secret_from_env
import os

#设置环境变量
os.environ["GOHUMANLOOP_API_KEY"] = "46cf87c5-9d08-4027-b72a-f0a91f27298a"

# 创建 GoHumanLoopManager 实例
manager = DefaultHumanLoopManager(
    APIProvider(
        name="ApiProvider",
        api_base_url="http://127.0.0.1:9800/api", # 换成自己飞书应用的URL
        api_key=get_secret_from_env("GOHUMANLOOP_API_KEY"),
        default_platform="feishu"
    )
)
# 创建 LangGraphAdapter 实例
adapter = HumanloopAdapter(
    manager=manager,
    default_timeout=600,  # 默认超时时间为10分钟
)
mcp = FastMCP("Weather")

@mcp.tool()
@adapter.require_info()
async def get_weather(location: str, info_result:dict={}) -> str:

    current_date = info_result["response"]

    """Get weather for location."""
    return f"It's always sunny in {location} on {current_date}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
