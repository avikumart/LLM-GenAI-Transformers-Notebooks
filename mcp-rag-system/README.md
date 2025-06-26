# mcp-rag-system
# MCP-Powered Agentic RAG System Setup Guide

This comprehensive guide will help you set up a complete MCP-powered Agentic RAG system using Firecrawl, Agno, and Milvus with a Streamlit interface.

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │────│   Agno Agent    │────│  MCP Protocol   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                │                        │
                       ┌─────────────────┐    ┌─────────────────┐
                       │ Milvus Vector   │    │ Firecrawl Web   │
                       │    Database     │    │    Scraper      │
                       └─────────────────┘    └─────────────────┘
```

## 🔧 Prerequisites

- **Python 3.8+**
- **Docker & Docker Compose**
- **Node.js & npm** (for Firecrawl MCP server)
- **Git**

## 📋 Step-by-Step Setup

### 1. Clone and Setup Project Structure

```bash
# Create project directory
mkdir mcp-rag-system
cd mcp-rag-system

# Create file structure
mkdir -p {mcp-servers,logs,data,config}

# Download the files provided in the artifacts
# - main.py (Streamlit application)
# - mcp_milvus_server.py (Custom MCP server)
# - requirements.txt
# - docker-compose.yml
# - .env.example
# - setup.sh
```

### 2. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies for Firecrawl MCP server
npm install -g @mendable/firecrawl-mcp-server
```

### 3. Setup Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your API keys
nano .env
```

Required API keys:
- **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Firecrawl API Key**: Get from [Firecrawl Dashboard](https://firecrawl.dev)

### 4. Start Milvus Vector Database

```bash
# Start Milvus using Docker Compose
docker-compose up -d

# Wait for services to be ready (30-60 seconds)
# Check status
docker-compose ps
```

Access Milvus Admin UI at: http://localhost:9001 (minioadmin/minioadmin)

### 5. Test MCP Servers

#### Test Milvus MCP Server:
```bash
# Run the custom Milvus MCP server
python mcp_milvus_server.py
```

#### Test Firecrawl MCP Server:
```bash
# Test Firecrawl MCP server
FIRECRAWL_API_KEY=your_key npx @mendable/firecrawl-mcp-server
```

### 6. Configure Cursor IDE (Optional)

For Cursor IDE MCP integration:

1. Go to **Settings → MCP**
2. Add new global MCP server with this configuration:

```json
{
  "firecrawl": {
    "command": "npx",
    "args": ["@mendable/firecrawl-mcp-server"],
    "env": {
      "FIRECRAWL_API_KEY": "your_firecrawl_api_key"
    }
  },
  "milvus-rag": {
    "command": "python",
    "args": ["mcp_milvus_server.py"],
    "cwd": "/path/to/your/project",
    "env": {
      "MILVUS_HOST": "localhost",
      "MILVUS_PORT": "19530"
    }
  }
}
```

### 7. Run the Application

```bash
# Start the Streamlit application
streamlit run main.py
```

The application will be available at: http://localhost:8501

## 🎯 Usage Instructions

### Basic Usage Flow:

1. **Configure API Keys**: Enter your OpenAI and Firecrawl API keys in the sidebar
2. **Add Documents**: Use the Documents tab to:
   - Scrape web pages using URLs
   - Upload text files directly
3. **Chat with Agent**: Use the Chat tab to:
   - Ask questions about your documents
   - Request web searches for current information
   - Get intelligent responses combining both sources

### Key Features:

- **Intelligent Routing**: Agent automatically decides whether to search web or local documents
- **Vector Search**: Semantic search through your document collection
- **Web Scraping**: Real-time web content extraction via Firecrawl
- **Source Citations**: All responses include proper source attribution
- **Interactive UI**: Clean, user-friendly Streamlit interface

## 🔍 Component Details

### Agno Agent Configuration
- **Model**: GPT-4 (configurable)
- **Tools**: MCP tools for Firecrawl and Milvus
- **Instructions**: Intelligent decision-making for information retrieval
- **Storage**: Optional PostgreSQL for conversation history

### Milvus Vector Database
- **Embedding Model**: all-MiniLM-L6-v2 (384 dimensions)
- **Index Type**: IVF_FLAT with COSINE similarity
- **Schema**: Content, title, URL, embeddings, metadata, timestamps

### MCP Integration
- **Firecrawl Server**: Web scraping and content extraction
- **Custom Milvus Server**: Vector database operations
- **Protocol**: Standard MCP for tool communication

## 🐛 Troubleshooting

### Common Issues:

1. **Milvus Connection Failed**
   ```bash
   # Check if Milvus is running
   docker-compose ps
   # Restart if needed
   docker-compose restart milvus
   ```

2. **API Key Errors**
   - Verify keys are correctly set in .env file
   - Check API key permissions and quotas

3. **MCP Server Not Responding**
   ```bash
   # Test MCP servers individually
   python mcp_milvus_server.py
   # Check Firecrawl server
   npx @mendable/firecrawl-mcp-server --help
   ```

4. **Embedding Model Download Issues**
   ```bash
   # Pre-download the model
   python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
   ```

### Performance Optimization:

1. **Milvus Performance**:
   - Increase nlist parameter for larger datasets
   - Use GPU-enabled Milvus for better performance
   - Adjust index parameters based on data size

2. **Memory Usage**:
   - Limit embedding batch size for large documents
   - Use streaming for large file uploads
   - Monitor Docker container resource usage

## 📊 Monitoring and Maintenance

### Health Checks:
```bash
# Check Milvus health
curl http://localhost:9091/healthz

# Check collection status
python -c "
from pymilvus import Collection
coll = Collection('rag_documents')
print(f'Documents: {coll.num_entities}')
"
```

### Backup Strategy:
- Export Milvus data regularly
- Backup environment configuration
- Version control your document corpus

## 🚀 Advanced Features

### Custom Embedding Models:
```python
# Replace in MilvusVectorDB class
self.embedding_model = SentenceTransformer('your-custom-model')
```

### Additional MCP Tools:
- Add more MCP servers for different data sources
- Create custom tools for specific use cases
- Integrate with other AI services

### Scaling Considerations:
- Use Milvus cluster for large-scale deployment
- Implement caching for frequently accessed documents
- Add load balancing for high-traffic scenarios

## 📚 Additional Resources

- [Agno Documentation](https://github.com/agno-agi/agno)
- [Firecrawl API Docs](https://docs.firecrawl.dev)
- [Milvus Documentation](https://milvus.io/docs)
- [MCP Specification](https://spec.modelcontextprotocol.io/)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request with detailed description

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Need help?** Check the troubleshooting section or open an issue in the project repository.
