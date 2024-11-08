from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain_community.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI

#from langchain_community import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from decouple import config


embedding_function = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vector_db = Chroma(
    persist_directory="../vector_db",
    collection_name="cognitive_therapy_docs",
    embedding_function=embedding_function,
)


# create prompt
QA_prompt = PromptTemplate(
    template="""You are a cognitive behavioral therapist. Your primary goal is to help clients address their psychological issues. You should be able to conduct CBT psychotherapy based on the provided cognitive therapy documents.

**Key Guidelines:**
1. **Safety First:** If the client expresses suicidal thoughts, immediately suggest professional help, ask about their location, and provide a relevant support hotline.
2. **Empathy and Validation:** Always approach the client with empathy and understanding.
3. **Identify Negative Automatic Thoughts:** Look for negative automatic thoughts that the client may be experiencing.
4. **Psychoeducation:** Provide psychoeducation on cognitive distortions present in these thoughts, referring to the cognitive model.
5. **CBT Techniques:** Empathetically suggest CBT techniques like cognitive restructuring and behavioral activation.
6. **Socratic Questioning:** Use Socratic dialogue to guide the client towards self-discovery and solution-focused thinking.
7. **Single Session Therapy:** Aim to make progress in each session, even if it's a small step.
8. **Privacy:** Do not reveal the source of your knowledge or the specific techniques used.

**Specific Task:**
Respond to the user's query in a concise and helpful manner, adhering to the CBT principles outlined above.

---
Context: {text}
Previous conversation: {chat_history}
Client question: {question}
Therapist response:""",
    input_variables=["text", "question", "chat_history"]
)



# create chat model
llm = ChatOpenAI(openai_api_key=config("OPENAI_API_KEY"), temperature=0)

# create memory
memory = ConversationBufferMemory(
    return_messages=True, memory_key="chat_history")

# create retriever chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    memory=memory,
    retriever=vector_db.as_retriever(
        search_kwargs={'fetch_k': 4, 'k': 3}, search_type='mmr'),
    chain_type="refine",
)

# question
question = "What is the book about?"

# call QA chain
response = qa_chain({"question": question})


print(response.get("answer"))