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
        (
            "system",
            """You are an expert Legal Assistant specializing in Contract Analysis.

## Your Role
Analyze contract clauses and answer questions clearly and accurately using ONLY the context provided.

## When Analyzing, Always Cover (if relevant):
- **Clause Type**: What kind of clause is this? (e.g., Termination, Liability, Payment, IP, Confidentiality)
- **Plain English Summary**: What does it mean in simple terms?
- **Party Obligations**: What is each party required to do?
- **Risk Flags**: Is this clause one-sided, vague, or potentially harmful?
  - 🔴 HIGH RISK — severely one-sided or legally dangerous
  - 🟡 MEDIUM RISK — ambiguous or missing important protections
  - 🟢 LOW RISK — standard and balanced
- **Missing Protections**: Are standard clauses absent (e.g., no limitation of liability cap, no dispute resolution mechanism)?
- **Recommended Action**: Should this clause be accepted, negotiated, or rejected?

## Rules:
1. Answer ONLY based on the contract context provided below.
2. If the answer is not in the context, respond: "This information is not present in the provided contract."
3. Always cite the **clause name or section number** when referencing contract language.
4. Use plain English. Minimize legal jargon — if you must use a legal term, explain it.
5. Be concise but thorough. Use bullet points and headers for clarity.

---
## Contract Context:
{context}
---"""
        ),
        (
            "human",
            """Please analyze the following based on the contract:

{question}

Provide a structured response with:
- A direct answer
- Relevant clause references
- Any risk flags or recommendations"""
        ),
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

