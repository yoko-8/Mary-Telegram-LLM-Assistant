# Edit your hyperDB file by copy-pasting this file over your hyperDB script
# This should be under: External Libraries > Python > site-packages > hypderdb > hypderdb.py

import gzip
import pickle

import numpy as np

from hyperdb.galaxy_brain_math_shit import (
    dot_product,
    adams_similarity,
    cosine_similarity,
    derridaean_similarity,
    euclidean_metric,
    hyper_SVM_ranking_algorithm_sort,
)
from fast_sentence_transformers import FastSentenceTransformer as SentenceTransformer

MAX_BATCH_SIZE = 2048
EMBEDDING_MODEL = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device='cpu')

def get_embedding(documents, key=None, model="text-embedding-ada-002"):
    if isinstance(documents, list):
        if isinstance(documents[0], dict):
            texts = []
            if isinstance(key, str):
                if "." in key:
                    key_chain = key.split(".")
                else:
                    key_chain = [key]
                for doc in documents:
                    for key in key_chain:
                        doc = doc[key]
                    texts.append(doc.replace("\n", " "))
            elif key is None:
                for doc in documents:
                    text = ", ".join([f"{key}: {value}" for key, value in doc.items()])
                    texts.append(text)
        elif isinstance(documents[0], str):
            texts = documents

    embeddings = EMBEDDING_MODEL.encode(texts)
    return embeddings


class HyperDB:
    def __init__(
        self,
        documents=None,
        vectors=None,
        key=None,
        embedding_function=None,
        similarity_metric="cosine",
    ):
        documents = documents or []
        self.documents = []
        self.vectors = None
        self.embedding_function = embedding_function or (
            lambda docs: get_embedding(docs, key=key)
        )
        if vectors is not None:
            self.vectors = vectors
            self.documents = documents
        else:
            self.add_documents(documents)

        if similarity_metric.__contains__("dot"):
            self.similarity_metric = dot_product
        elif similarity_metric.__contains__("cosine"):
            self.similarity_metric = cosine_similarity
        elif similarity_metric.__contains__("euclidean"):
            self.similarity_metric = euclidean_metric
        elif similarity_metric.__contains__("derrida"):
            self.similarity_metric = derridaean_similarity
        elif similarity_metric.__contains__("adams"):
            self.similarity_metric = adams_similarity
        else:
            raise Exception(
                "Similarity metric not supported. Please use either 'dot', 'cosine', 'euclidean', 'adams', or 'derrida'."
            )

    def dict(self, vectors=False):
        if vectors:
            return [
                {"document": document, "vector": vector.tolist(), "index": index}
                for index, (document, vector) in enumerate(
                    zip(self.documents, self.vectors)
                )
            ]
        return [
            {"document": document, "index": index}
            for index, document in enumerate(self.documents)
        ]

    def add(self, documents, vectors=None):
        if not isinstance(documents, list):
            return self.add_document(documents, vectors)
        self.add_documents(documents, vectors)

    def add_document(self, document: dict, vector=None):
        vector = (
            vector if vector is not None else self.embedding_function([document])[0]
        )
        if self.vectors is None:
            self.vectors = np.empty((0, len(vector)), dtype=np.float32)
        elif len(vector) != self.vectors.shape[1]:
            raise ValueError("All vectors must have the same length.")
        self.vectors = np.vstack([self.vectors, vector]).astype(np.float32)
        self.documents.append(document)

    def remove_document(self, index):
        self.vectors = np.delete(self.vectors, index, axis=0)
        self.documents.pop(index)

    def add_documents(self, documents, vectors=None):
        if not documents:
            return
        vectors = vectors or np.array(self.embedding_function(documents)).astype(
            np.float32
        )
        for vector, document in zip(vectors, documents):
            self.add_document(document, vector)

    def save(self, storage_file):
        data = {"vectors": self.vectors, "documents": self.documents}
        if storage_file.endswith(".gz"):
            with gzip.open(storage_file, "wb") as f:
                pickle.dump(data, f)
        else:
            with open(storage_file, "wb") as f:
                pickle.dump(data, f)

    def load(self, storage_file):
        if storage_file.endswith(".gz"):
            with gzip.open(storage_file, "rb") as f:
                data = pickle.load(f)
        else:
            with open(storage_file, "rb") as f:
                data = pickle.load(f)
        self.vectors = data["vectors"].astype(np.float32)
        self.documents = data["documents"]

    # def query(self, query_text, top_k=5, return_similarities=True):
    #     query_vector = self.embedding_function([query_text])[0]
    #     ranked_results, similarities = hyper_SVM_ranking_algorithm_sort(
    #         self.vectors, query_vector, top_k=top_k, metric=self.similarity_metric
    #     )
    #     if return_similarities:
    #         return list(
    #             zip([self.documents[index] for index in ranked_results], similarities)
    #         )
    #     return [self.documents[index] for index in ranked_results]


    # def query(self, query_text, top_k=1, return_similarities=True, context_window=1):
    #     query_vector = self.embedding_function([query_text])[0]
    #     ranked_results, similarities = hyper_SVM_ranking_algorithm_sort(
    #         self.vectors, query_vector, top_k=top_k, metric=self.similarity_metric
    #     )
    #
    #     results_with_context = []
    #
    #     for i in range(len(ranked_results)):
    #         index = ranked_results[i]
    #         before_index = max(0, index - context_window)
    #         after_index = min(len(self.documents) - 1, index + context_window)
    #
    #         context_documents = [self.documents[i] for i in range(before_index, after_index + 1)]
    #         result_with_context = {
    #             "document": self.documents[index],
    #             "context": context_documents,
    #             # "similarity": similarities[i]
    #         }
    #         results_with_context.append(result_with_context)
    #
    #     if return_similarities:
    #         return results_with_context
    #     return [result['document'] for result in results_with_context]


    def query(self, query_text, top_k=1, return_similarities=True, context_window=1):
        query_vector = self.embedding_function([query_text])[0]
        ranked_results, similarities = hyper_SVM_ranking_algorithm_sort(
            self.vectors, query_vector, top_k=top_k, metric=self.similarity_metric
        )

        index = ranked_results[0]
        before_index = max(0, index - context_window)
        after_index = min(len(self.documents) - 1, index + context_window)
        context_documents = [self.documents[i] for i in range(before_index, after_index + 1)]
        return context_documents