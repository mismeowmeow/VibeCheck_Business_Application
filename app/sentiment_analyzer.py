"""
Sentiment Analysis Module
Created by Data Science Team

This module uses Hugging Face's transformers library to perform 
sentiment analysis on text using a pre-trained DistilBERT model.
"""

from transformers import pipeline


class SentimentAnalyzer:
    """
    A class to perform sentiment analysis on text(s) using the Hugging Face transformers library.

    The class initializes a sentiment-analysis pipeline upon instantiation, which downloads
    a default pre-trained model (typically `distilbert-base-uncased-finetuned-sst-2-english`)
    if one is not specified or already cached.
    """

    def __init__(self):
        """
        Initializes the SentimentAnalyzer by setting up the sentiment analysis pipeline.
        The pipeline automatically loads a suitable model for sentiment analysis.
        """
        print("Initializing Sentiment Analysis pipeline...")
        # This will automatically download a default model for sentiment analysis
        # (e.g., distilbert-base-uncased-finetuned-sst-2-english) if not already present.
        self.classifier = pipeline("sentiment-analysis")
        print("Sentiment Analysis pipeline initialized.")

    def analyze_sentiment(self, texts):
        """
        Analyzes the sentiment of one or more given texts.

        Args:
            texts (str or list[str]): A single string or a list of strings
                                     to be analyzed for sentiment.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary contains
                        the 'label' (e.g., 'POSITIVE', 'NEGATIVE') and 'score'
                        for the sentiment of the corresponding input text.

        Example:
            >>> analyzer = SentimentAnalyzer()
            >>> analyzer.analyze_sentiment("I love this product!")
            [{'label': 'POSITIVE', 'score': 0.999...}]

            >>> analyzer.analyze_sentiment([
            ...     "This is a fantastic day!",
            ...     "I am quite disappointed with the service."
            ... ])
            [{'label': 'POSITIVE', 'score': 0.999...}, {'label': 'NEGATIVE', 'score': 0.999...}]
        """
        if isinstance(texts, str):
            # If a single string is provided, wrap it in a list for consistent processing
            return self.classifier(texts)
        elif isinstance(texts, list):
            # If a list of strings is provided, process all of them
            return self.classifier(texts)
        else:
            raise TypeError("Input 'texts' must be a string or a list of strings.")


# Global instance - initialized once when module is imported
_sentiment_analyzer = None


def get_sentiment_analyzer():
    """
    Returns a singleton instance of SentimentAnalyzer.
    This ensures the model is only loaded once.
    """
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        _sentiment_analyzer = SentimentAnalyzer()
    return _sentiment_analyzer
