from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingModel:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()

    def embed(self, text):
        if not text:
            return np.zeros(self.dim, dtype="float32")
        vec = self.model.encode([text], show_progress_bar=False)[0]
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec /= norm
        return vec.astype("float32")
