from deepagents import create_deep_agent

from infrastructure.llm_router import get_groq_llm
from tools.heritage_search import heritage_search_tool


llm = get_groq_llm()

agent = create_deep_agent(
    model=llm,
    tools=[heritage_search_tool],
    system_prompt="""
You are a Goa heritage research agent.

When the user asks about a Goa heritage place,
use the heritage_search_tool first.

After receiving the tool result, answer the user.
Do not invent information.
""",
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Tell me about the Basilica of Bom Jesus in Goa.",
            }
        ]
    }
)

print(result)