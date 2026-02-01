from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db, init_db
from app.models import User, Business, Review
from app.schemas import (
    UserCreate, UserLogin, UserResponse, LoginResponse,
    BusinessResponse, ReviewCreate, ReviewResponse, MessageResponse
)
from app.auth import hash_password, verify_password
from app.utils import analyze_review_sentiment, update_business_vibe_score

# Initialize FastAPI app
app = FastAPI(title="VibeCheck Business API", version="1.0.0")


# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to VibeCheck Business API"}


# User Registration
@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if username exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_pwd = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


# User Login
@app.post("/login", response_model=LoginResponse)
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    # Find user
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Verify password
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    return {
        "message": "Login successful",
        "user": user
    }


# Get all businesses
@app.get("/businesses", response_model=List[BusinessResponse])
def list_all_businesses(db: Session = Depends(get_db)):
    businesses = db.query(Business).all()
    return businesses


# Get specific business
@app.get("/businesses/{business_id}", response_model=BusinessResponse)
def get_business(business_id: int, db: Session = Depends(get_db)):
    business = db.query(Business).filter(Business.id == business_id).first()
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    return business


# Post a review
@app.post("/businesses/{business_id}/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    business_id: int,
    review_data: ReviewCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    # Verify business exists
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Analyze sentiment using DS Service
    sentiment_result = analyze_review_sentiment(review_data.content)
    
    # Create review
    new_review = Review(
        user_id=user_id,
        business_id=business_id,
        content=review_data.content,
        vibe_score=sentiment_result.get("vibe_score"),
        sentiment=sentiment_result.get("sentiment"),
        keywords=sentiment_result.get("keywords")
    )
    
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    
    # Update business vibe score
    update_business_vibe_score(business_id, db)
    
    return new_review


# Get reviews for a business
@app.get("/businesses/{business_id}/reviews", response_model=List[ReviewResponse])
def get_business_reviews(business_id: int, db: Session = Depends(get_db)):
    # Verify business exists
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    reviews = db.query(Review).filter(Review.business_id == business_id).all()
    return reviews
