import os
from pymilvus import connections, utility, Collection, CollectionSchema, FieldSchema, DataType
from sentence_transformers import SentenceTransformer
from mcp.server.fastmcp import FastMCP
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
COLLECTION_NAME = "rag_documents"
EMBEDDING_DIM = 384
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'
METRIC_TYPE = "COSINE"
INDEX_TYPE = "IVF_FLAT"

mcp = FastMCP("milvus-rag")

class MilvusVectorDB:
    def __init__(self):
        self.host = os.getenv("MILVUS_HOST", "localhost")
        self.port = os.getenv("MILVUS_PORT", "19530")
        self.embedding_model = None
        self._connect()
        self._get_collection()

    def _connect(self):
        try:
            logger.info(f"Connecting to Milvus at {self.host}:{self.port}")
            connections.connect("default", host=self.host, port=self.port)
            logger.info("Successfully connected to Milvus.")
        except Exception as e:
            logger.error(f"Failed to connect to Milvus: {e}")
            raise

    def _load_embedding_model(self):
        if self.embedding_model is None:
            logger.info(f"Loading embedding model: {EMBEDDING_MODEL_NAME}")
            self.embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
            logger.info("Embedding model loaded.")

    def _get_collection(self):
        if not utility.has_collection(COLLECTION_NAME):
            logger.info(f"Collection '{COLLECTION_NAME}' does not exist. Creating it.")
            fields = [
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
                FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=512),
                FieldSchema(name="url", dtype=DataType.VARCHAR, max_length=2048),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM),
                FieldSchema(name="timestamp", dtype=DataType.INT64)
            ]
            schema = CollectionSchema(fields, "RAG documents collection")
            self.collection = Collection(COLLECTION_NAME, schema)
            self._create_index()
            logger.info(f"Collection '{COLLECTION_NAME}' created and index built.")
        else:
            logger.info(f"Collection '{COLLECTION_NAME}' already exists.")
            self.collection = Collection(COLLECTION_NAME)
        self.collection.load()

    def _create_index(self):
        index_params = {
            "metric_type": METRIC_TYPE,
            "index_type": INDEX_TYPE,
            "params": {"nlist": 128},
        }
        self.collection.create_index(field_name="embedding", index_params=index_params)
        logger.info("Index created for 'embedding' field.")

    def add_documents(self, documents: list[dict]) -> list[int]:
        self._load_embedding_model()
        
        contents = [doc['content'] for doc in documents]
        embeddings = self.embedding_model.encode(contents)

        entities = []
        for i, doc in enumerate(documents):
            entities.append({
                "content": doc.get('content', ''),
                "title": doc.get('title', ''),
                "url": doc.get('url', ''),
                "embedding": embeddings[i],
                "timestamp": doc.get('timestamp', 0)
            })

        logger.info(f"Inserting {len(entities)} documents.")
        mr = self.collection.insert(entities)
        self.collection.flush()
        logger.info(f"Successfully inserted {len(mr.primary_keys)} documents.")
        return mr.primary_keys

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        self._load_embedding_model()
        
        query_embedding = self.embedding_model.encode([query])[0]
        
        search_params = {
            "metric_type": METRIC_TYPE,
            "params": {"nprobe": 10},
        }
        
        logger.info(f"Searching for query: '{query}'")
        results = self.collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            output_fields=["content", "title", "url", "timestamp"]
        )
        
        output = []
        for hit in results[0]:
            output.append({
                "id": hit.id,
                "score": hit.distance,
                "content": hit.entity.get('content'),
                "title": hit.entity.get('title'),
                "url": hit.entity.get('url'),
                "timestamp": hit.entity.get('timestamp'),
            })
        logger.info(f"Found {len(output)} results for query.")
        return output

try:
    milvus_db = MilvusVectorDB()

    @mcp.tool()
    def add_documents(documents: list[dict]) -> dict:
        """
        Adds documents to the Milvus vector database.
        Each document should be a dictionary with 'content', 'title', 'url', and 'timestamp'.
        """
        try:
            ids = milvus_db.add_documents(documents)
            return {"status": "success", "inserted_ids": ids}
        except Exception as e:
            logger.error(f"Error in add_documents tool: {e}")
            return {"status": "error", "message": str(e)}

    @mcp.tool()
    def search(query: str, top_k: int = 5) -> dict:
        """
        Searches for similar documents in the Milvus vector database.
        """
        try:
            results = milvus_db.search(query, top_k)
            return {"status": "success", "results": results}
        except Exception as e:
            logger.error(f"Error in search tool: {e}")
            return {"status": "error", "message": str(e)}

except Exception as e:
    logger.error(f"Failed to initialize MilvusVectorDB and MCP tools: {e}")
    # Define dummy functions if initialization fails
    @mcp.tool()
    def add_documents(documents: list[dict]) -> dict:
        return {"status": "error", "message": "Milvus connection failed during startup."}
    
    @mcp.tool()
    def search(query: str, top_k: int = 5) -> dict:
        return {"status": "error", "message": "Milvus connection failed during startup."}


if __name__ == "__main__":
    logger.info("Starting MCP server for Milvus RAG.")
    mcp.run()
