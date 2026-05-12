import chromadb
from core.config import settings

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path=settings.CHROMA_DB_DIR)

# Get or create a collection for clothing embeddings
clothing_collection = chroma_client.get_or_create_collection(
    name="clothing_items",
    metadata={"hnsw:space": "cosine"} # Use cosine similarity
)

def get_vector_db():
    return clothing_collection
