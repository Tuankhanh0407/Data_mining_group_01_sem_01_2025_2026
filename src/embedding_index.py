# Import necessary libraries
import faiss
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
from typing import Dict, List

class EmbeddingIndex:
    """ 
    Wrapper around SentenceTransformer embeddings and FAISS index for RAG.

    Attributes:
    - model_name (str): Name of the sentence transformer model.
    - index (faiss.IndexFlatIP): FAISS index using inner product similarity.
    - embeddings (np.ndarray): Dense vectors for all chunks.
    - meta (List[Dict]): Metadata per chunk (topic, intent, audience, text). 
    """

    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2") -> None:
        self.model_name = model_name
        self.index = None
        self.embeddings = None
        self.meta: List[Dict] = []

    def build(self, dataset_path: Path) -> None:
        """ 
        Build FAISS index from dataset.
        @param dataset_path (Path): Path to dataset JSONL file. 
        """
        model = SentenceTransformer(self.model_name)
        texts: List[str] = []
        meta: List[Dict] = []
        with dataset_path.open("r", encoding = "utf-8") as f:
            for line in f:
                obj = json.loads(line)
                for ch in obj.get("chunks", []):
                    texts.append(ch)
                    meta.append({
                        "topic": obj.get("topic", ""),
                        "intent": obj.get("intent", ""),
                        "audience": obj.get("audience", ""),
                        "chunk": ch
                    })
        if not texts:
            raise ValueError("No chunks available to create embeddings.")
        emb = model.encode(texts, convert_to_numpy = True, normalize_embeddings = True)
        dim = emb.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(emb)
        self.index = index
        self.embeddings = emb
        self.meta = meta

    def search(self, query: str, top_k: int = 8) -> List[Dict]:
        """ 
        Search FAISS index for relevant chunks.
        @param query (str): Query text for retrieval.
        @param top_k (int): Number of top results to fetch.
        @return (List[Dict]): Retrieved chunks with scores and metadata. 
        """
        if self.index is None:
            raise RuntimeError("Index not built.")
        model = SentenceTransformer(self.model_name)
        q_emb = model.encode([query], convert_to_numpy = True, normalize_embeddings = True)
        scores, idxs = self.index.search(q_emb, top_k)
        results: List[Dict] = []
        for rank, i in enumerate(idxs[0]):
            if (i < 0):
                continue
            item = dict(self.meta[i])
            item["score"] = float(scores[0][rank])
            results.append(item)
        return results