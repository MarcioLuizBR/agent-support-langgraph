import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("A chave de API do OpenAI não foi encontrada. Por favor, defina a variável de ambiente OPENAI_API_KEY.")

llm = ChatOpenAI(
    model="gpt-4o-mini", 
    temperature=0, 
    api_key=api_key
    )

def main():
    resposta = llm.invoke("Explique em uma frase o que é um agente de IA.")
    print("\nResposta do modelo:\n")
    print(resposta.content)


if __name__ == "__main__":
    main()