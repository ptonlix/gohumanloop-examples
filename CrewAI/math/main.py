import os
from crewai import Agent, Crew, Task
from crewai.tools import tool

from gohumanloop.adapters import HumanloopAdapter
from gohumanloop import DefaultHumanLoopManager, EmailProvider
from dotenv import load_dotenv

load_dotenv()
# 从环境变量获取邮箱配置
smtp_server = os.environ.get("SMTP_SERVER", "smtp.example.com")
smtp_port = int(os.environ.get("SMTP_PORT", "587"))
imap_server = os.environ.get("IMAP_SERVER", "imap.example.com")
imap_port = int(os.environ.get("IMAP_PORT", "993"))
recipient_email = os.environ.get("TEST_RECIPIENT_EMAIL", "your_email@example.com")

# 创建 EmailProvider 实例
provider = EmailProvider(
    name="EmailHumanLoop",
    smtp_server=smtp_server,
    smtp_port=smtp_port,
    imap_server=imap_server,
    imap_port=imap_port,
    check_interval=30,  # 每30秒检查一次邮件
    language="en",  # 支持中文模板切换
)

# Create HumanLoopManager instance
manager = DefaultHumanLoopManager(
    initial_providers=[provider],
)

hl = HumanloopAdapter(manager=manager)

PROMPT = """multiply 2 and 5, then add 32 to the result"""


@tool
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@tool
@hl.require_approval(metadata={"recipient_email": recipient_email},)
def multiply(a: int, b: int, approval_result=None) -> int:
    """multiply two numbers"""
    print(f"approval_result: {approval_result}")
    return a * b


general_agent = Agent(
    role="Math Professor",
    goal="""Provide the solution to the students that are asking
    mathematical questions and give them the answer.""",
    backstory="""You are an excellent math professor that likes to solve math questions
    in a way that everyone can understand your solution""",
    allow_delegation=False,
    tools=[add, multiply],
    verbose=True,
)

task = Task(
    description=PROMPT,
    agent=general_agent,
    expected_output="A numerical answer.",
)

crew = Crew(agents=[general_agent], tasks=[task], verbose=True)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n\n---------- RESULT ----------\n\n")
    print(result)