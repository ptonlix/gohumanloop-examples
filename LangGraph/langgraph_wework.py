# /// script
# requires-python = ">=3.10"
# dependencies = [
# "gohumanloop>=0.0.11",
# "langgraph>=0.4.7",
# "langchain-openai>=0.3.12"]
# ///

"""
LangGraph 与 WeWork企业微信 简单集成示例

这是一个最小化示例，展示如何在 LangGraph 中使用 LangGraphAdapter和 APIProvider与企业微信进行人机交互。
将你的 AI Agent 链接到企业微信审批流程中。

配置：
- API 地址: https://your-api-endpoint/api
- API KEY: 通过API接口获取

前置条件：需要根据GoHumanLoop-WeWork配置好企业微信审批应用和服务
详情见：https://github.com/ptonlix/gohumanloop-wework
"""

import os
import time
from typing import TypedDict, List, Dict
from dotenv import load_dotenv

# 导入 LangGraph 相关库
from langgraph.graph import StateGraph, END

# 导入 GoHumanLoop 相关库
from gohumanloop.adapters.langgraph_adapter import HumanloopAdapter
from gohumanloop.core.interface import HumanLoopStatus
from gohumanloop import DefaultHumanLoopManager, APIProvider
from gohumanloop.utils import get_secret_from_env

import logging

logging.basicConfig(level=logging.INFO)

# 设置环境变量
os.environ["GOHUMANLOOP_API_KEY"] = "b1c080cd-b9f6-4a9e-8180-b6162f29a741"


# 定义简单状态类型
class SimpleState(TypedDict):
    messages: List[Dict[str, str]]


# 创建 GoHumanLoopManager 实例
manager = DefaultHumanLoopManager(
    APIProvider(
        name="ApiProvider", 
        api_base_url="https://dread.run/api", # 换成自己企业微信的URL
        api_key=get_secret_from_env("GOHUMANLOOP_API_KEY"),
        default_platform="wework"
    )
)
# 创建 LangGraphAdapter 实例
adapter = HumanloopAdapter(
    manager=manager,
    default_timeout=300,  # 默认超时时间为5分钟
)

# 定义需要获取人工信息的节点
@adapter.require_info(
    task_id="simple-information-test",
    additional="这是一个简单的获取信息的示例。",
)
def get_information_node(state: SimpleState, info_result={}) -> SimpleState:
    """获取信息的节点"""
    print("获取人工信息...")
    print(f"info_result: {info_result}")

    
    state["messages"].append({
        "role": "system",
        "content": f"已获取信息: {info_result.get('response')}"
    })
    
    return state


# 定义需要人工审批的节点
@adapter.require_approval(
    task_id="simple-approval-test",
    additional="这是一个简单的审批示例。",
    execute_on_reject=True,
)
def human_approval_node(state: SimpleState, approval_result=None) -> SimpleState:
    """需要人工审批的节点"""
    print("人工审批完成中...")

    print(f"approval_result: {approval_result}")
    # 处理审批结果
    if approval_result:
        status = approval_result.get("status")
        response = approval_result.get("response", {})

        if status == HumanLoopStatus.APPROVED:
            state["messages"].append(
                {
                    "role": "human",
                    "content": f"审批已通过！理由: {response}",
                }
            )
        elif status == HumanLoopStatus.REJECTED:
            state["messages"].append(
                {
                    "role": "human",
                    "content": f"审批被拒绝。理由: {response}",
                }
            )

    return state


def final_node(state: SimpleState) -> SimpleState:
    """最终节点"""
    state["messages"].append({"role": "system", "content": "工作流程已完成！"})
    return state


# 构建工作流图
def build_simple_graph():
    """构建简单工作流图"""
    graph = StateGraph(SimpleState)

    # 添加节点
    graph.add_node("get_info", get_information_node)
    graph.add_node("human_approval", human_approval_node)
    graph.add_node("final", final_node)

    # 设置边
    graph.add_edge("get_info", "human_approval")
    graph.add_edge("human_approval", "final")
    graph.add_edge("final", END)

    # 设置入口
    graph.set_entry_point("get_info")

    return graph.compile()


# 运行工作流
def run_simple_workflow():
    """运行简单工作流"""
    with adapter:
        # 构建工作流图
        workflow = build_simple_graph()

        # 初始化状态
        initial_state = SimpleState(
            messages=[{"role": "system", "content": "开始简单工作流..."}],
        )

        # 运行工作流
        for output in workflow.stream(initial_state, stream_mode="values"):
            print(f"状态: {output}")

            # 等待一下，便于观察
            time.sleep(1)


# 主函数
if __name__ == "__main__":
    # 加载环境变量
    load_dotenv()

    # 运行工作流
    run_simple_workflow()

