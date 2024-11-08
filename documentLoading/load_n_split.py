import os
from pathlib import Path
from langchain.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def create_vector_db():
    # Get the absolute path of the current script
    current_dir = Path(__file__).parent.absolute()
    documents_dir = current_dir.parent / "documents"
    vector_db_path = current_dir.parent / "vector_db"
    
    # List of PDF files to process
    pdf_files = [
        "CognitiveTherapyTechniques.pdf",
        "DavidBurnsFeelingGood.pdf",
        "patienthealth.pdf",
        "RecoveryOrientedCognitiveTherapy.pdf"
    ]
    
    all_pages = []
    
    try:
        # Process each PDF file
        for pdf_file in pdf_files:
            pdf_path = documents_dir / pdf_file
            
            # Verify PDF file exists
            if not pdf_path.exists():
                print(f"Warning: PDF file not found at: {pdf_path}")
                continue
            
            print(f"Loading PDF from: {pdf_path}")
            
            # Create loader and process file
            loader = PyPDFLoader(str(pdf_path))
            pages = loader.load_and_split()
            
            if pages:
                print(f"Successfully loaded {len(pages)} pages from {pdf_file}")
                all_pages.extend(pages)
            else:
                print(f"Warning: No pages extracted from {pdf_file}")
        
        if not all_pages:
            raise ValueError("No pages were extracted from any PDF files")
            
        print(f"Total pages loaded: {len(all_pages)}")
        
        # Create embedding function
        embedding_func = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Create vector store directory if it doesn't exist
        vector_db_path.mkdir(parents=True, exist_ok=True)
        
        print(f"Creating vector store at: {vector_db_path}")
        
        # Create vector store
        vectordb = Chroma.from_documents(
            documents=all_pages,
            embedding=embedding_func,
            persist_directory=str(vector_db_path),
            collection_name="cognitive_therapy_docs"  # Updated collection name
        )
        
        print("Vector store created and persisted successfully")
        
        return vectordb
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        vectordb = create_vector_db()
        print("Database creation completed successfully")
    except Exception as e:
        print(f"Failed to create database: {str(e)}")