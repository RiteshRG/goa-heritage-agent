from langchain.tools import tool

from infrastructure.llm_router import get_groq_llm


@tool
def get_heritage_info(place: str) -> str:
    """Get basic heritage information about a Goa place."""
    return f"Heritage information for {place}."


llm = get_groq_llm()

llm_with_tools = llm.bind_tools(
    [get_heritage_info]
)

response = llm_with_tools.invoke(
    """
What is the Mahadeva Temple at Tambdi Surla, and what makes it historically significant?"""
)

print("CONTENT:")
print(response.content)

print("\nTOOL CALLS:")
print(response.tool_calls)