from langchain_openai import ChatOpenAI
# from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings



def get_openai_llm(model_name: str, temperature: float = 0.0):
    return ChatOpenAI(model=model_name, temperature=temperature)

# def get_google_llm(model_name: str, temperature: float = 0.0):
#     return ChatGoogleGenerativeAI(model_name=model_name, temperature=temperature)


