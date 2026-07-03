from transformers import pipeline


class EmailClassifier:
    """
    Email Classifier using Hugging Face Zero-Shot Classification pipeline.
    Uses a lightweight distilled model for fast and efficient inference.
    """
    def __init__(self, model_name: str = "typeform/distilbert-base-uncased-mnli"):
        self.model_name = model_name
        self._pipeline = None

    @property
    def pipeline(self):
        # Lazy load the pipeline so it is only initialized on first use
        if self._pipeline is None:
            self._pipeline = pipeline(
                "zero-shot-classification",
                model=self.model_name
            )
        return self._pipeline

    def classify(self, text: str) -> dict:
        """
        Classifies the email body into one of the candidate classes:
        - Job
        - Complaint
        - Sales
        - Personal

        Returns:
            dict: { "category": str, "confidence": float }
        """
        if not text or not text.strip():
            return {"category": "Personal", "confidence": 0.0}

        candidate_labels = ["Job", "Complaint", "Sales", "Personal"]
        
        # Execute zero-shot pipeline
        result = self.pipeline(text, candidate_labels)
        
        # The result outputs labels and scores sorted from highest to lowest confidence
        top_category = result["labels"][0]
        top_score = result["scores"][0]
        
        return {
            "category": top_category,
            "confidence": round(float(top_score), 4)
        }
