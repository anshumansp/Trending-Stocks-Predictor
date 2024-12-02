import requests
import json

BASE_URL = "http://localhost:8000"

def test_chat():
    """
    Test the chat endpoint which uses Claude via LangChain's ConversationChain.
    This maintains context across multiple messages.
    """
    print("\n=== Testing Chat Endpoint with Claude ===")
    url = f"{BASE_URL}/chat"
    
    # Test multiple messages to demonstrate context retention
    messages = [
        "Can you explain AWS Lambda in simple terms?",
        "What are some common use cases for the service you just described?",
        "What are the main limitations or constraints I should be aware of?"
    ]
    
    for message in messages:
        payload = {"message": message}
        print(f"\nSending message: {message}")
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print(f"Response: {response.json()['response']}")
        else:
            print(f"Error: {response.status_code}, {response.text}")

def test_document_processing():
    """
    Test the document processing endpoint which demonstrates:
    1. Document loading
    2. Text splitting
    3. HuggingFace embedding creation
    4. Vector storage
    """
    print("\n=== Testing Document Processing Endpoint ===")
    url = f"{BASE_URL}/process-document"
    
    # Create a sample document about AWS
    with open("sample_doc.txt", "w") as f:
        f.write("""
AWS CloudFormation provides a common language to model and provision AWS and third-party 
application resources in your cloud environment. CloudFormation allows you to use programming 
languages or a simple text file to model and provision, in an automated and secure manner, 
all the resources needed for your applications across all regions and accounts.

Key benefits include:
1. Infrastructure as Code
2. Automated deployments
3. Dependency management
4. Rollback on failure
5. Version control capability
        """)
    
    # Send the document for processing
    with open("sample_doc.txt", "rb") as f:
        files = {"file": ("sample_doc.txt", f)}
        response = requests.post(url, files=files)
        
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.status_code}, {response.text}")

def test_qa():
    """
    Test the QA endpoint which uses Claude via LangChain's QA chain to:
    1. Process specific questions about given contexts
    2. Generate relevant and accurate answers
    """
    print("\n=== Testing QA Endpoint with Claude ===")
    url = f"{BASE_URL}/qa"
    
    # Test context and questions about AWS
    context = """
    Amazon ECS (Elastic Container Service) is a fully managed container orchestration service 
    that helps you easily deploy, manage, and scale containerized applications. It deeply 
    integrates with the rest of the AWS platform to provide a secure and easy-to-use 
    solution for running container workloads in the cloud and now on your infrastructure 
    with ECS Anywhere.

    ECS features include Fargate for serverless compute for containers, deep integration 
    with AWS IAM for security, AWS VPC for networking, and AWS CloudWatch for monitoring.
    """
    
    questions = [
        "What is Amazon ECS and what does it do?",
        "What are the key features of ECS?",
        "How does ECS integrate with other AWS services?"
    ]
    
    for question in questions:
        payload = {
            "question": question,
            "context": context
        }
        print(f"\nAsking: {question}")
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print(f"Response: {response.json()['response']}")
        else:
            print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    print("Starting endpoint tests with Claude...")
    
    try:
        # Test basic connectivity
        requests.get(f"{BASE_URL}/health")
        
        # Run tests
        test_chat()
        test_document_processing()
        test_qa()
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
