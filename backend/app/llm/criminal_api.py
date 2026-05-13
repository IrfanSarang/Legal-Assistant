import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough


load_dotenv()

def generate_response(question, retriever):

    model = init_chat_model(
        model="gemini-2.5-flash-lite",
        model_provider="google-genai",
        api_key=os.getenv("GOOGLE_API_KEY")
    )

    prompt = ChatPromptTemplate.from_messages([
        ('system',
         'You are an Expert Legal Assistant for Criminal Cases. '
         'Answer using only the context provided below. '
         'If the answer is not in the context, say you do not know.\n\n'
         'Context:\n{context}'),
        ('human', '{question}'),
    ])

    parser = StrOutputParser()

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | model
        | parser
    )

    return chain.invoke(question)

