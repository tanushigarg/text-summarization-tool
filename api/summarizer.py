import boto3
from langchain_community.chat_models import BedrockChat
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate

# Configure HuggingFace Embeddings
def configure_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Configure FAISS retriever from input text
def configure_retriever(context):
    SPLIT_THRESHOLD = 5000
    embedding_model = configure_embeddings()

    if len(context) <= SPLIT_THRESHOLD:
        documents = [Document(page_content=context, metadata={"source": "html_input"})]
    else:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200,
            separators=["\n", ">", "<"]
        )
        chunks = text_splitter.split_text(context)
        documents = [Document(page_content=chunk, metadata={"source": "html_input"}) for chunk in chunks]


    try:
        vector_db = FAISS.from_documents(documents, embedding_model)

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e  # Optional: or return a JSON error from Flask

    return vector_db.as_retriever()

# Configure Claude 3.5 via Bedrock
def configure_llm():
    return BedrockChat(
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        client=boto3.client("bedrock-runtime", region_name="us-east-1")
    )

# QA chain setup
def configure_qa_chain(retriever, llm):
    prompt = PromptTemplate.from_template(
        "You are a helpful assistant. Summarize the following content accurately: \n\n{context}"
    )
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )