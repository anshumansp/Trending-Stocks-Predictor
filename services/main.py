from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
import os
import logging
from dotenv import load_dotenv
from anthropic import Anthropic, APIError, APIConnectionError, APITimeoutError
from typing import Dict, Optional
import tempfile
import traceback

# Configure logging with more detail
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for more detail
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Stock Recommendation System API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Anthropic client
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    logger.error("ANTHROPIC_API_KEY environment variable not set")
    raise ValueError("ANTHROPIC_API_KEY environment variable not set")

logger.info(f"Initializing Anthropic client with API key: {api_key[:4]}...")
anthropic = Anthropic(api_key=api_key)

# Pydantic models
class ChatRequest(BaseModel):
    message: str

    @field_validator('message')
    @classmethod
    def message_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('message cannot be empty')
        return v

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

class ErrorResponse(BaseModel):
    detail: str
    error_type: str
    status: str = "error"

class DocumentQARequest(BaseModel):
    question: str
    document_index: int = 0  # Index of the document to query

@app.get("/")
def root():
    return {"message": "Stock Recommendation System API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> Dict:
    try:
        logger.info(f"Processing chat request with message length: {len(request.message)}")
        logger.debug(f"Request message: {request.message}")
        
        logger.debug("Creating Anthropic API request...")
        client = Anthropic()
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[{"role": "user", "content": request.message}]
        )
        
        logger.info("Successfully received response from Anthropic API")
        logger.debug(f"Response content: {message}")
        
        # Extract the message content from the response
        response_text = message.content[0].text
        return ChatResponse(
            response=response_text,
            status="success"
        )
    
    except APIConnectionError as e:
        logger.error(f"Connection error with Anthropic API: {str(e)}")
        logger.debug(f"Connection error details: {traceback.format_exc()}")
        raise HTTPException(
            status_code=503,
            detail={
                "detail": "Unable to connect to AI service. Please try again later.",
                "error_type": "connection_error",
                "status": "error"
            }
        )
    except APITimeoutError as e:
        logger.error(f"Timeout error with Anthropic API: {str(e)}")
        logger.debug(f"Timeout error details: {traceback.format_exc()}")
        raise HTTPException(
            status_code=504,
            detail={
                "detail": "Request timed out. Please try again.",
                "error_type": "timeout_error",
                "status": "error"
            }
        )
    except APIError as e:
        logger.error(f"Anthropic API error: {str(e)}")
        logger.debug(f"API error details: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail={
                "detail": f"AI service error: {str(e)}",
                "error_type": "api_error",
                "status": "error"
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        logger.debug(f"Error details: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail={
                "detail": f"An unexpected error occurred: {str(e)}",
                "error_type": "internal_error",
                "status": "error"
            }
        )

# Store for processed documents
processed_documents = []

@app.post("/upload")
def upload_file(
    file: UploadFile = File(...)
) -> Dict:
    try:
        logger.info("Processing file upload")
        
        # Create a temporary file
        temp_file_path = ""
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name
            content = temp_file.read()
            temp_file.write(content)

        # Process the document
        with open(temp_file_path, "r") as temp_file:
            document = temp_file.read()
        
        # Store processed documents
        processed_documents.append(document)
        
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        
        logger.info("File uploaded successfully")
        return {
            "message": "Document processed successfully",
            "chunks": 1,
            "document_index": len(processed_documents) - 1
        }
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        logger.error(f"Error in file upload endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/qa", response_model=ChatResponse)
def qa_endpoint(request: DocumentQARequest, client_id: str = "default"):
    if not processed_documents:
        raise HTTPException(
            status_code=400,
            detail="No documents have been processed yet. Please upload a document first."
        )
    
    try:
        logger.info(f"Processing QA request with question: {request.question}")
        
        # Get the document content
        if request.document_index >= len(processed_documents):
            raise HTTPException(
                status_code=400,
                detail=f"Document index {request.document_index} is out of range. Max index is {len(processed_documents) - 1}"
            )
        
        document = processed_documents[request.document_index]
        
        # Create a prompt that includes both the question and document content
        prompt = f"""Here is a document content:
{document}

Question: {request.question}

Please answer the question based on the document content above."""
        
        # Get answer using the conversation chain
        message = anthropic.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        logger.info("Successfully received response from Anthropic API")
        logger.debug(f"Response content: {message.content}")
        
        return ChatResponse(
            response=message.content
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in QA endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
