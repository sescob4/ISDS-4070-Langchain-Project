import os
import sys
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
import argparse
import docx

# Load environment variables from .env file
load_dotenv()


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Ask questions about documents.")
    parser.add_argument(
        "--files", nargs="+", required=True, help="List of files (PDF, TXT, DOCX) to process."
    )
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables.")
        sys.exit(1)

    # Extract and combine text from all provided files
    all_text = ""
    for file_name in args.files:
        text = extract_data(file_name)
        if text:
            all_text += text
        else:
            print(f"No text extracted from {file_name}.")

    if not all_text.strip():
        print("No text extracted from the provided files.")
        sys.exit(1)

    # Split the text into chunks
    docs = split_text(all_text)
    print(f"Number of chunks generated: {len(docs)}")

    # Vectorize and store the text chunks
    docstorage = vectorize_and_store(docs, api_key)

    # Interactive question-answering loop
    print("\nYou can now ask questions about the documents.")
    print("Type 'exit' to quit.")
    while True:
        question = input("\nEnter your question: ")
        if question.lower() == "exit":
            print("Goodbye!")
            break
        response = answer_question(question, api_key, docstorage)
        print(f"Answer: {response}")


def extract_data(file_name):
    """Extract text data from different file types."""
    try:
        # For PDF files
        if file_name.endswith('.pdf'):
            loader = PyPDFLoader(file_name)
            data = loader.load()
            return "".join(doc['text'] if 'text' in doc else str(doc) for doc in data)

        # For TXT files
        elif file_name.endswith('.txt'):
            with open(file_name, 'r', encoding='utf-8') as f:
                return f.read()

        # For DOCX files
        elif file_name.endswith('.docx'):
            doc = docx.Document(file_name)
            return "\n".join([para.text for para in doc.paragraphs])

        else:
            raise ValueError(f"Unsupported file format: {file_name}")

    except Exception as e:
        print(f"Error extracting data from {file_name}: {e}")
        return ""


def split_text(text):
    """Split the text into manageable chunks."""
    ct_splitter = CharacterTextSplitter(
        separator=".",
        chunk_size=1500,
        chunk_overlap=300
    )
    docs = ct_splitter.split_text(text)
    return docs


def vectorize_and_store(docs, api_key):
    """Create embeddings and store them in a FAISS vector database."""
    try:
        embedding_function = OpenAIEmbeddings(openai_api_key=api_key)
        docstorage = FAISS.from_texts(docs, embedding_function)
        return docstorage
    except Exception as e:
        print(f"Error vectorizing and storing data: {e}")
        sys.exit(1)


def answer_question(question, api_key, docstorage):
    """Answer the user's question using the vectorized data."""
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=api_key)
    retriever = docstorage.as_retriever(search_type="similarity", search_kwargs={"k": 5})  # Retrieve top 5 chunks
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever
    )
    try:
        response = qa.invoke({"query": question})
        return response["result"]
    except Exception as e:
        print(f"Error during question answering: {e}")
        return "An error occurred while processing your question."


if __name__ == "__main__":
    main()
