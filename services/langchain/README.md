# LangChain Documentation for AWS Orchestrator

## Introduction
LangChain is a powerful framework designed to help developers build applications powered by language models. In our AWS Orchestrator project, we use LangChain to integrate Claude 3 models and create intelligent interactions with AWS services.

## Why LangChain?
- **Memory Management**: Built-in conversation memory to maintain context
- **Document Processing**: Easy handling of various document formats
- **Structured Output**: Clean formatting of AI responses
- **Chain of Thought**: Complex reasoning through sequential steps
- **AWS Integration**: Seamless connection with AWS services

## Components We Use

### 1. Chat Models
We use `ChatAnthropic` from LangChain to interact with Claude 3 models:
```python
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(
    model="claude-3-sonnet-20240229",  # or "claude-3-haiku-20240307" for faster responses
    temperature=0.7,
    max_tokens=1024,
    timeout=None,
    max_retries=2
)
```

#### Available Claude 3 Models
- **Claude 3 Opus**: Most capable model, best for complex tasks
- **Claude 3 Sonnet**: Balanced performance and speed
- **Claude 3 Haiku**: Fastest model, ideal for simple tasks

#### Model Features
- Tool calling capabilities
- Structured output support
- Image input support
- Token-level streaming
- Native async support
- Token usage tracking

### 2. Memory
We implement conversation memory to maintain context:
```python
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory()
```

### 3. Document Processing
For handling documents and AWS service responses:
```python
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
```

### 4. Vector Store
For semantic search and document retrieval:
```python
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
```

## Getting Started

1. **Environment Setup**
   - Install required packages:
     ```bash
     pip install langchain>=0.0.240 anthropic>=0.18.1
     ```
   - Set up your Anthropic API key in `.env`:
     ```
     ANTHROPIC_API_KEY=your_key_here
     ```

2. **Basic Usage**
   ```python
   from langchain.chains import ConversationChain
   
   conversation = ConversationChain(
       llm=llm,
       memory=ConversationBufferMemory()
   )
   
   response = conversation.predict(input="Hello!")
   ```

## Features

### 1. Conversational Memory
- Maintains context across multiple interactions
- Stores previous conversations for reference
- Enables more natural and contextual responses

### 2. Document Processing
- Splits documents into manageable chunks
- Creates embeddings for semantic search
- Enables question-answering over documents

### 3. AWS Service Integration
- Processes AWS service responses
- Formats AWS CLI outputs
- Provides natural language interface to AWS

## Best Practices

1. **Model Selection**
   - Use Claude 3 Haiku for quick, simple responses
   - Use Claude 3 Sonnet for balanced performance
   - Use Claude 3 Opus for complex reasoning tasks

2. **Memory Management**
   - Clear memory when starting new conversations
   - Use appropriate memory types for your use case
   - Monitor memory usage in long conversations

3. **Error Handling**
   - Implement proper try-catch blocks
   - Handle API rate limits gracefully
   - Provide meaningful error messages

4. **Security**
   - Never expose API keys in code
   - Use environment variables
   - Implement proper authentication

## Anthropic Integration Details

### Authentication
```python
import os
from langchain_anthropic import ChatAnthropic

# Set your API key
os.environ["ANTHROPIC_API_KEY"] = "your-api-key"

# Initialize the model
llm = ChatAnthropic()
```

### Message Formatting
```python
# Single message
response = llm.invoke("Tell me a joke")

# Multiple messages
messages = [
    ("system", "You are a helpful assistant"),
    ("human", "What's the weather like?"),
]
response = llm.invoke(messages)
```

### Using Tools
```python
from pydantic import BaseModel, Field

class GetWeather(BaseModel):
    """Get current weather in a location"""
    location: str = Field(..., description="City and state")

# Bind tools to the model
llm_with_tools = llm.bind_tools([GetWeather])

# Tool will be automatically invoked when needed
response = llm_with_tools.invoke("What's the weather in New York?")
```

### Streaming Responses
```python
for chunk in llm.stream("Tell me a story"):
    print(chunk.content, end="", flush=True)
```

### Async Support
```python
async def get_response():
    async for chunk in llm.astream("Tell me a story"):
        print(chunk.content, end="", flush=True)
```

## Troubleshooting

### Common Issues

1. **API Key Issues**
   - Ensure ANTHROPIC_API_KEY is set
   - Check API key validity
   - Verify environment variable loading

2. **Memory Issues**
   - Clear memory if context becomes too large
   - Monitor token usage
   - Use streaming for large responses

3. **Performance Issues**
   - Implement proper caching
   - Use appropriate chunk sizes
   - Monitor and optimize embeddings

## Additional Resources

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction.html)
- [Anthropic Claude Documentation](https://docs.anthropic.com/claude/docs)
- [AWS SDK Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## Support

For issues or questions:
1. Check the troubleshooting guide above
2. Review error messages carefully
3. Consult the official documentation
4. Reach out to the development team
