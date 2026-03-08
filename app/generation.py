"""
Generation module — sends the retrieved context + user query to an LLM
and returns the final answer.
Uses LangChain's ChatOpenAI for LLM interaction.
"""

from typing import List, Dict
from langchain_openai import ChatOpenAI
from config import *
from openai import AzureOpenAI
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()



_llm = ChatOpenAI(
    model=OPENAI_MODEL,
    api_key=OPENAI_API_KEY,
    max_tokens=MAX_TOKENS,
    temperature=TEMPERATURE,
)

groq_api_key = os.getenv("GROQ_API_KEY")


llm = ChatGroq(
    model="llama-3.3-70b-versatile",  # or "llama3-70b-8k"
    api_key=groq_api_key
)

MODEL="GROQ"

SYSTEM_PROMPT = """You are a helpful assistant that answers questions based on the provided context.
Use ONLY the context below to answer. If the answer is not in the context, say "I don't have enough information to answer that."

CITATION RULES:
- Each context chunk is labeled [1], [2], etc. with its source document and page number(s).
- When you use information from a chunk, cite it inline like [1], [2], etc.
- At the end of your answer, add a "References" section listing each cited source with page numbers.
- Format: [n] source_filename, p.X

Example:
Apple's Q4 revenue was $94.9 billion [1], with Services reaching a record $25 billion [2].

References:
[1] Apple_Q24.pdf, p.3
[2] Apple_Q24.pdf, p.5"""


def build_context_block(chunks: List[Dict]) -> str:
    """Format retrieved chunks into a numbered context string with page info."""
    parts = []
    for i, c in enumerate(chunks, 1):
        source = c.get("source", "unknown")
        pages = c.get("pages", "")
        text = c.get("chunk_text", "")
        page_label = f", p.{pages}" if pages else ""
        parts.append(f"[{i}] (source: {source}{page_label})\n{text}")
    return "\n\n".join(parts)


#using azure ai/openai
def generate_answer2(query: str, chunks: List[Dict]) -> str:
    """
    Generate an answer with inline citations using LangChain ChatOpenAI.
    """
    context = build_context_block(chunks)

    # messages = [
    #     ("system", SYSTEM_PROMPT),
    #     ("human", f"Context:\n{context}\n\n---\nQuestion: {query}"),
    # ]
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\n---\nQuestion: {query}",
        }
    
    ]

    ai_msg = get_response(messages)
    answer=ai_msg.choices[0].message.content

   
    return answer


#using groq
def generate_answer(query: str, chunks: List[Dict]) -> str:
    """
    Generate an answer with inline citations using LangChain ChatOpenAI.
    """
    context = build_context_block(chunks)

    prompt = PromptTemplate(
            input_variables=["system_prompt", "context", "query"],
            template="""
        {system_prompt}

        Context:
        {context}

        ---

        Question: {query}

        Answer:
        """
        )
    chain = prompt | llm
    response = chain.invoke({
    "system_prompt": SYSTEM_PROMPT,
    "context": context,
    "query": query
})
    return response.content

def get_response(messages):
    """
    Returns a response from the OpenAI client.
    """
    client = get_openai_client()
    response = client.chat.completions.create(
        stream=False,
        messages=messages,
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=gpt4deployment
        )
    return response

    

def get_openai_client():
    """
    Returns an instance of the AzureOpenAI client.
    """
    return AzureOpenAI(
    api_version=api_version,
    azure_endpoint=AI_FOUNDRY_AI_SERVICES_URL,
    api_key=AI_FOUNDRY_KEY,
    )


def generate_answer1(query: str, chunks: List[Dict]) -> str:
    """
    Returns a response from the OpenAI client.
    """
    context = build_context_block(chunks)

    client = get_openai_client()
    response = client.chat.completions.create(
        stream=False,
        messages=query,
    max_tokens=4096,
    temperature=1.0,
    top_p=1.0,
    model=gpt4deployment
        )
    return response


if __name__ == "__main__":
    print("=== Generation Test ===")
    print(f"   Using: model {MODEL})")

    # Test with dummy context
    test_chunks = [
        {"chunk_text": "Apple reported Q4 2024 revenue of $94.9 billion, up 6% year over year.", "source": "Apple_Q24.pdf"},
        {"chunk_text": "Services revenue reached an all-time record of $25 billion.", "source": "Apple_Q24.pdf"},
    ]
    test_query = "What was Apple's revenue in Q4 2024?"

    print(f"Query: {test_query}")
    print(f"Context chunks: {len(test_chunks)}\n")

    answer = generate_answer(test_query, test_chunks)
    print(f"💬 Answer:\n{answer}")
    print("\n✅ Generation test passed !")
