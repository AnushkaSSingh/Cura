import os
from typing import List, Dict


class KnowledgeBase:
    """
    Lightweight knowledge-base search for the Cura prototype.

    This version uses simple keyword matching instead of a
    vector database, making it easy to run during a hackathon.
    """

    def __init__(self):
        self.base_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "knowledge_base",
        )

    def _load_file(self, filename: str) -> str:
        path = os.path.join(self.base_path, filename)

        try:
            with open(path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return ""

    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> List[Dict[str, str]]:
        """
        Search the knowledge base using simple keyword matching.
        """

        documents = [
            "company_policies.md",
            "product_docs.md",
            "faq.md",
        ]

        query_words = set(
            query.lower().split()
        )

        results = []

        for filename in documents:
            content = self._load_file(filename)

            if not content:
                continue

            content_words = set(
                content.lower().split()
            )

            score = len(
                query_words.intersection(content_words)
            )

            if score > 0:
                results.append(
                    {
                        "source": filename,
                        "content": content,
                        "score": score,
                    }
                )

        results.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return results[:top_k]