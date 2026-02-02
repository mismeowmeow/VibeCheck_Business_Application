from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import DATABASE_URL
from app.models import Base, Business

# Create engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency function to get database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database by creating all tables and populating with sample businesses if empty.
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    
    # Check if businesses already exist and populate if empty
    db = SessionLocal()
    try:
        existing_businesses = db.query(Business).first()
        
        if not existing_businesses:
            print("Database is empty. Populating with sample businesses...")
            
            # Sample businesses data
            sample_businesses = [
                Business(
                    name="Veempire Hotels",
                    category="Hotel",
                    location="123 Main St, New York, NY 10001",
                    aggregated_vibe_score=0.0,
                    total_reviews=0
                ),
                Business(
                    name="The Krusty Krab",
                    category="Restaurant",
                    location="456 Oak Avenue, Los Angeles, CA 90001",
                    aggregated_vibe_score=0.0,
                    total_reviews=0
                ),
                Business(
                    name="Bob's Auto Repair",
                    category="Auto Repair",
                    location="789 Elm Street, Chicago, IL 60601",
                    aggregated_vibe_score=0.0,
                    total_reviews=0
                ),
                Business(
                    name="Sunrise Yoga Studio",
                    category="Fitness",
                    location="321 Wellness Blvd, Austin, TX 78701",
                    aggregated_vibe_score=0.0,
                    total_reviews=0
                ),
                Business(
                    name="Tech Haven Electronics",
                    category="Electronics Store",
                    location="654 Innovation Drive, Seattle, WA 98101",
                    aggregated_vibe_score=0.0,
                    total_reviews=0
                ),
                Business(
                    name="Bella's Boutique",
                    category="Fashion Retail",
                    location="987 Style Lane, Miami, FL 33101",
                    aggregated_vibe_score=0.0,
                    total_reviews=0
                ),
                Business(
                    name="Downtown Pet Grooming",
                    category="Pet Services",
                    location="147 Park Place, Denver, CO 80201",
                    aggregated_vibe_score=0.0,
                    total_reviews=0
                ),
                Business(
                    name="Alice's Wonderland Bakery",
                    category="Bakery",
                    location="258 Sweet Avenue, Boston, MA 02101",
                    aggregated_vibe_score=0.0,
                    total_reviews=0
                ),
                Business(
                    name="Kami-tachi tea shop",
                    category="Cafe",
                    location="369 Razor Road, Atlanta, GA 30301",
                    aggregated_vibe_score=0.0,
                    total_reviews=0
                ),
                Business(
                    name="Vee's Paradise",
                    category="Bookstore",
                    location="741 Library Lane, Portland, OR 97201",
                    aggregated_vibe_score=0.0,
                    total_reviews=0
                ),
                Business(
                    name="Fresh Market Grocery",
                    category="Grocery Store",
                    location="852 Farm Street, Nashville, TN 37201",
                    aggregated_vibe_score=0.0,
                    total_reviews=0
                ),
                Business(
                    name="Ocean Breeze Onlinemart",
                    category="Online Store",
                    location="963 Relaxation Way, San Diego, CA 92101",
                    aggregated_vibe_score=0.0,
                    total_reviews=0
                ),
            ]
            
            db.add_all(sample_businesses)
            db.commit()
            print(f"✓ Successfully populated database with {len(sample_businesses)} businesses!")
        else:
            print("Database already contains businesses. Skipping population.")
            
    except Exception as e:
        print(f"Error during database initialization: {str(e)}")
        db.rollback()
    finally:
        db.close()