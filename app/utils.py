from sqlalchemy.orm import Session
from app.models import Business, Review
from app.sentiment_analyzer import get_sentiment_analyzer
import re


def extract_keywords(text: str, max_keywords: int = 5) -> str:
    """
    Extract important keywords from review text.
    Simple implementation using word frequency and filtering.
    
    Args:
        text: The review text
        max_keywords: Maximum number of keywords to extract
        
    Returns:
        Comma-separated string of keywords
    """
    # Convert to lowercase and remove special characters
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    
    # Common words to ignore (stop words)
    stop_words = {
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
        'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
        'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
        'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
        'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
        'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
        'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
        'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
        'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
        'once', 'very', 'can', 'will', 'just', 'should', 'now'
    }
    
    # Split into words and filter
    words = [word for word in text.split() if word not in stop_words and len(word) > 3]
    
    # Count word frequency
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency and get top keywords
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    keywords = [word for word, freq in sorted_words[:max_keywords]]
    
    return ", ".join(keywords) if keywords else "general feedback"


def analyze_review_sentiment(review_text: str) -> dict:
    """
    Analyze review sentiment using DS team's sentiment analyzer.
    Transforms the output to match VibeCheck requirements.
    
    Args:
        review_text: The review content to analyze
        
    Returns:
        Dictionary containing:
        - vibe_score (float): Score from 0-100
        - sentiment (str): "POSITIVE" or "NEGATIVE"
        - keywords (str): Comma-separated keywords
    """
    try:
        # Get sentiment analyzer instance
        analyzer = get_sentiment_analyzer()
        
        # Analyze the review
        result = analyzer.analyze_sentiment(review_text)[0]
        
        label = result['label']  # "POSITIVE" or "NEGATIVE"
        confidence = result['score']  # 0.0 to 1.0
        
        # Transform confidence score to vibe score (0-100)
        if label == "POSITIVE":
            vibe_score = confidence * 100
        else:  # NEGATIVE
            vibe_score = (1 - confidence) * 100
        
        # Extract keywords from the review
        keywords = extract_keywords(review_text)
        
        return {
            "vibe_score": round(vibe_score, 2),
            "sentiment": label,
            "keywords": keywords
        }
    
    except Exception as e:
        print(f"Error in sentiment analysis: {str(e)}")
        # Return neutral values if analysis fails
        return {
            "vibe_score": 50.0,
            "sentiment": "NEUTRAL",
            "keywords": "error in analysis"
        }


def calculate_vibe_score(business_id: int, db: Session) -> float:
    """
    Calculate the aggregated Vibe Score for a business based on all its reviews.
    
    Args:
        business_id: ID of the business
        db: Database session
        
    Returns:
        Average vibe score (0-100)
    """
    reviews = db.query(Review).filter(Review.business_id == business_id).all()
    
    if not reviews:
        return 0.0
    
    # Filter reviews that have vibe scores
    valid_scores = [review.vibe_score for review in reviews if review.vibe_score is not None]
    
    if not valid_scores:
        return 0.0
    
    # Calculate average
    avg_score = sum(valid_scores) / len(valid_scores)
    return round(avg_score, 2)


def update_business_vibe_score(business_id: int, db: Session):
    """
    Update the aggregated Vibe Score and total review count for a business.
    
    Args:
        business_id: ID of the business
        db: Database session
    """
    business = db.query(Business).filter(Business.id == business_id).first()
    
    if business:
        business.aggregated_vibe_score = calculate_vibe_score(business_id, db)
        business.total_reviews = db.query(Review).filter(Review.business_id == business_id).count()
        db.commit()
