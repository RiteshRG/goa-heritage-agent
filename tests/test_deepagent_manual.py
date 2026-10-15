from deepagents import create_deep_agent
from langchain.tools import tool

from infrastructure.llm_router import get_groq_llm


@tool
def get_heritage_info(place: str) -> str:
    """Get basic heritage information about a Goa place."""
    return f"Heritage information for {place}."


llm = get_groq_llm()

agent = create_deep_agent(
    model=llm,
    tools=[get_heritage_info],
    system_prompt="""
You are a simple heritage research agent.

When the user asks about a heritage place,
use the get_heritage_info tool before answering.
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