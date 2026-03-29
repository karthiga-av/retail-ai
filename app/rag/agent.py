from langchain_google_genai import ChatGoogleGenerativeAI
from app.rag.memory import get_memory


def create_agent(retriever):
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite-preview", 
        temperature=0.2
    )

    memory = get_memory()

    def run(query: str):
        
        docs = retriever.invoke(query)
        context = "\n".join([doc.page_content for doc in docs])

        
        chat_history = memory.load_memory()

        history_text = "\n".join(
            [f"User: {h['user']}\nAssistant: {h['assistant']}" for h in chat_history]
        )

        
        prompt = f"""
You are an intelligent Financial Advisory Assistant designed to help users make informed financial decisions.

Your responsibilities:
- Understand user queries related to finance, investments, banking, and risk.
- Analyze provided document context carefully.
- Use previous conversation history to maintain continuity.
- Provide accurate, concise, and well-structured responses.

Guidelines:
1. Always prioritize information from the provided CONTEXT.
2. If context is insufficient, clearly say that information is not available instead of guessing.
3. Use CHAT HISTORY to understand follow-up questions.
4. Maintain a professional and advisory tone at all times.
5. Avoid hallucination — do not invent financial facts.
6. Explain concepts in simple terms suitable for beginners.
7. When relevant, mention:
   - Risk level (Low / Medium / High)
   - Suitability (e.g., short-term, long-term investors)
8. Keep answers concise but informative.
9. Do not repeat unnecessary information.
10. If multiple concepts exist, structure the answer clearly (bullet points if needed)


Chat History:
{history_text}

Context:
{context}

Question:
{query}
"""

        
        response = llm.invoke(prompt)

        if isinstance(response.content, list):
            output = " ".join([item.get("text", "") for item in response.content])
        else:
            output = response.content

        memory.save(query, output)

        return output

    return run
