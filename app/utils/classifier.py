from typing import Dict, List

from huggingface_hub import InferenceClient

from app.config import settings


# =========================================================
# Descriptive labels improve zero-shot classification
# =========================================================
CANDIDATE_LABELS: List[str] = [
    "job application, recruitment, interview, hiring or career opportunity",
    "customer complaint, dissatisfaction, problem or negative feedback",
    "sales inquiry, product offer, pricing or business proposal",
    "personal message, general communication, reminder, invitation or announcement",
]


# Convert descriptive Hugging Face labels back to app categories
LABEL_MAPPING: Dict[str, str] = {
    CANDIDATE_LABELS[0]: "Job",
    CANDIDATE_LABELS[1]: "Complaint",
    CANDIDATE_LABELS[2]: "Sales",
    CANDIDATE_LABELS[3]: "Personal",
}


class EmailClassifier:
    """
    Remote zero-shot email classifier using Hugging Face Inference Providers.

    The model runs remotely, so PyTorch and Transformers are not loaded
    inside the FastAPI application. This keeps memory usage low for
    deployment on limited-resource hosting platforms.
    """

    def __init__(
        self,
        model_name: str = "facebook/bart-large-mnli",
    ) -> None:
        """
        Initialize the Hugging Face Inference Client.
        """

        self.model_name = model_name

        self.client = InferenceClient(
            token=settings.HF_TOKEN
        )

    def classify(self, text: str) -> Dict[str, float | str]:
        """
        Classify an email into one of four categories:

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

        # Handle empty input
        if not text or not text.strip():
            return {
                "category": "Personal",
                "confidence": 0.0,
            }

        try:
            # Call Hugging Face remote inference
            result = self.client.zero_shot_classification(
                text=text.strip(),
                candidate_labels=CANDIDATE_LABELS,
                model=self.model_name,
                multi_label=False,
            )

            # Highest-scoring classification
            top_result = result[0]

            # Convert descriptive label to application category
            category = LABEL_MAPPING.get(
                top_result.label,
                "Personal"
            )

            return {
                "category": category,
                "confidence": round(
                    float(top_result.score),
                    4
                ),
            }

        except Exception as e:
            print(
                f"[Hugging Face Classifier Error] "
                f"{type(e).__name__}: {e}"
            )

            # Safe fallback
            return {
                "category": "Personal",
                "confidence": 0.0,
            }