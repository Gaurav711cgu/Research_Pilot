"""
Semantic search & source ranking using Nova Multimodal Embeddings + FAISS.
ResearchPilot — Amazon Nova AI Hackathon 2026
"""
import numpy as np
from typing import List, Tuple
from tools.bedrock_client import BedrockClient


class EmbeddingSearch:
    """
    Semantic similarity engine using Amazon Nova Embeddings.
    Ranks research sources by relevance to the user's query.
    Uses FAISS for fast nearest-neighbor search.
    """

    def __init__(self):
        self.bedrock = BedrockClient()
        self.index = None
        self.stored_texts: List[str] = []
        self.stored_metadata: List[dict] = []
        self.dimension: int = 1536  # Nova Embedding dimension

    def add_sources(self, sources: List[dict]) -> None:
        """
        Embed and index a list of research sources.
        Each source: {"text": str, "url": str, "title": str, ...}
        """
        try:
            import faiss
        except ImportError:
            # Fallback: simple cosine similarity without FAISS
            self._add_sources_simple(sources)
            return

        vectors = []
        for source in sources:
            text = f"{source.get('title', '')} {source.get('text', '')}"
            embedding = self.bedrock.embed_text(text)
            vectors.append(embedding)
            self.stored_texts.append(text)
            self.stored_metadata.append(source)

        if not vectors:
            return

        matrix = np.array(vectors, dtype=np.float32)
        self.dimension = matrix.shape[1]

        # Build FAISS index (inner product = cosine similarity for normalized vectors)
        faiss.normalize_L2(matrix)
        self.index = faiss.IndexFlatIP(self.dimension)
        self.index.add(matrix)

    def _add_sources_simple(self, sources: List[dict]) -> None:
        """Fallback without FAISS — stores embeddings in memory."""
        self.vectors = []
        for source in sources:
            text = f"{source.get('title', '')} {source.get('text', '')}"
            embedding = self.bedrock.embed_text(text)
            self.vectors.append(np.array(embedding, dtype=np.float32))
            self.stored_texts.append(text)
            self.stored_metadata.append(source)

    def search(self, query: str, top_k: int = 5) -> List[Tuple[dict, float]]:
        """
        Find the most relevant sources for a query.
        Returns list of (source_metadata, similarity_score) tuples.
        """
        query_embedding = np.array(
            self.bedrock.embed_text(query), dtype=np.float32
        ).reshape(1, -1)

        if self.index is not None:
            import faiss
            faiss.normalize_L2(query_embedding)
            scores, indices = self.index.search(query_embedding, min(top_k, len(self.stored_metadata)))
            results = [
                (self.stored_metadata[idx], float(scores[0][i]))
                for i, idx in enumerate(indices[0])
                if idx >= 0
            ]
        else:
            # Simple cosine similarity fallback
            results = self._cosine_search(query_embedding, top_k)

        return results

    def _cosine_search(self, query_vec: np.ndarray, top_k: int) -> List[Tuple[dict, float]]:
        """Cosine similarity search without FAISS."""
        if not hasattr(self, "vectors") or not self.vectors:
            return []

        q = query_vec.flatten()
        q_norm = np.linalg.norm(q)

        scores = []
        for i, vec in enumerate(self.vectors):
            v_norm = np.linalg.norm(vec)
            if q_norm > 0 and v_norm > 0:
                sim = float(np.dot(q, vec) / (q_norm * v_norm))
            else:
                sim = 0.0
            scores.append((self.stored_metadata[i], sim))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def rerank(self, query: str, sources: List[dict]) -> List[dict]:
        """
        Rerank a list of sources by semantic relevance.
        Returns sources sorted by relevance score (highest first).
        """
        self.add_sources(sources)
        ranked = self.search(query, top_k=len(sources))
        return [meta for meta, score in ranked if score > 0.3]
