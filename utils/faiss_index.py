import faiss
import numpy as np
import os
import json

class FaissIndex:
    def __init__(self, dim=384):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)
        self.ids = []

    def add(self, vectors, ids):
        self.index.add(vectors)
        self.ids.extend(ids)

    def search(self, qvec, k=5):
        q = qvec.reshape(1, -1).astype("float32")
        D, I = self.index.search(q, k)
        scores = D[0].tolist()
        ids = [self.ids[i] if i < len(self.ids) else None for i in I[0].tolist()]
        return {"scores": scores, "ids": ids}

    def is_ready(self):
        return self.index.ntotal > 0

    def reset(self):
        self.index.reset()
        self.ids = []

    def save(self, index_path):
        faiss.write_index(self.index, index_path)
        with open(index_path + ".meta", "w") as f:
            json.dump(self.ids, f)

    def load(self, index_path):
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
            try:
                with open(index_path + ".meta", "r") as f:
                    self.ids = json.load(f)
            except:
                self.ids = []
