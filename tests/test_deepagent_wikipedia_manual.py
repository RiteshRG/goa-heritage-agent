from deepagents import create_deep_agent

from infrastructure.llm_router import get_groq_llm
from tools.heritage_search import heritage_search_tool
from tools.wikipedia_tool import wikipedia_tool


llm = get_groq_llm()

agent = create_deep_agent(
    model=llm,
    tools=[
        heritage_search_tool,
        wikipedia_tool,
    ],
    system_prompt="""
You are a Goa heritage research agent.

Research rules:

1. First use heritage_search_tool.
2. Evaluate its result.
3. If the result contains enough information to answer,
   answer the user.
4. If the result is insufficient, use wikipedia_tool.
5. After using Wikipedia, answer the user.
6. Do not invent historical or cultural information.

Do not call tools unnecessarily.
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
