from infrastructure.llm_router import get_groq_llm


def test_groq_llm_initializes():
    llm = get_groq_llm()

    assert llm is not None