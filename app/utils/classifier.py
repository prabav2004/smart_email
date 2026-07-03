from typing import Dict, List
from transformers import pipeline

# Categories used for zero-shot classification
CANDIDATE_LABELS: List[str] = [
    "Job",
    "Complaint",
    "Sales",
    "Personal"
]


class EmailClassifier:
    """
    Email Classifier using Hugging Face Zero-Shot Classification.

    The Hugging Face model is loaded once when the application starts
    and reused for every incoming request.
    """

    def __init__(
        self,
        model_name: str = "typeform/distilbert-base-uncased-mnli"
    ) -> None:

        self.pipeline = pipeline(
            task="zero-shot-classification",
            model=model_name
        )

    def classify(self, text: str) -> Dict[str, float | str]:
        """
        Classify an email into one of the supported categories.

        Categories:
        - Job
        - Complaint
        - Sales
        - Personal

        Returns:
        {
            "category": str,
            "confidence": float
        }
        """

        if not text or not text.strip():
            return {
                "category": "Personal",
                "confidence": 0.0
            }

        try:
            result = self.pipeline(
                text,
                candidate_labels=CANDIDATE_LABELS,
                multi_label=False
            )

            return {
                "category": result["labels"][0],
                "confidence": round(float(result["scores"][0]), 4)
            }

        except Exception as e:
            print(f"[Classifier Error] {e}")

            return {
                "category": "Personal",
                "confidence": 0.0
            }