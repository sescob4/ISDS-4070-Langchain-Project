# ISDS-4070-Langchain-Project

This project is a Python-based Question and Answer (Q&A) system that processes various document types (`PDF`, `TXT`, `DOCX`) and uses the OpenAI API to answer questions based on the content of those documents. The project employs LangChain for chunking text, creating embeddings, and performing retrieval-based question answering.

---

## Features

- **Supported Formats**: Processes `PDF`, `TXT`, and `DOCX` files.
- **Chunking**: Splits document content into smaller chunks for better context.
- **Vector Store**: Uses FAISS for efficient storage and retrieval of embeddings.
- **OpenAI Integration**: Utilizes `gpt-3.5-turbo` for answering questions interactively.
- **Interactive Q&A**: Allows users to interactively ask questions about the documents.

---

## Requirements

To run this project, ensure you have the following installed:

- Python 3.8+
- Required Python libraries (see `requirements.txt`)

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up OpenAI API Key**
   - Create a `.env` file in the project root.
   - Add your OpenAI API key:
     ```env
     OPENAI_API_KEY=your_openai_api_key
     ```

---

## Usage

### Run the Script

To process documents and ask questions:

```bash
python langchain_project.py --files <file1> <file2> ...
```

Replace `<file1>`, `<file2>` with the paths to your documents.

### Example

```bash
python langchain_project.py --files "example.pdf" "notes.txt" "assignment.docx"
```

### Interactive Q&A

Once the script processes the documents, you can ask questions interactively:

```plaintext
Enter your question: Who is the professor for Ethics?
Answer: Dr. John Doe

Enter your question: exit
Goodbye!
```

---

## How It Works

1. **Extract Text**: The script extracts text from the provided files.
2. **Chunk Text**: Splits the text into chunks of 1,500 characters with 300 characters of overlap.
3. **Vectorize Chunks**: Converts the text chunks into embeddings using OpenAI’s embedding model.
4. **Store in FAISS**: Saves embeddings in a FAISS vector store for efficient retrieval.
5. **Answer Questions**: Answers questions by retrieving relevant chunks and querying the OpenAI GPT model.

---

## Supported File Formats

- **PDF**: Extracted using `PyPDFLoader`.
- **TXT**: Read directly as plain text.
- **DOCX**: Processed with `python-docx`.

---

## Troubleshooting

### Common Errors

1. **Missing OpenAI API Key**:
   Ensure your `.env` file is correctly set up with your API key.

2. **Missing Dependencies**:
   Run `pip install -r requirements.txt` to install all required libraries.

3. **Unsupported File Format**:
   Make sure the files are in `PDF`, `TXT`, or `DOCX` format.

---


