"""
Database Population Script for VibeCheck Business
Run this script to populate the database with sample businesses.

Usage:
    python populate_db.py
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Business


def populate_database():
    """
    Populate the database with sample businesses.
    """
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create database session
    db: Session = SessionLocal()
    
    try:
        # Check if businesses already exist
        existing_count = db.query(Business).count()
        
        if existing_count > 0:
            print(f"Database already contains {existing_count} businesses.")
            user_input = input("Do you want to add more businesses anyway? (yes/no): ")
            if user_input.lower() not in ['yes', 'y']:
                print("Operation cancelled.")
                return
        
        # Sample businesses data
        sample_businesses = [
            {
                "name": "Veempire Hotels",
                "category": "Hotel chain",
                "location": "123 Main St, New York, NY 10001",
            },
            {
                "name": "The Krusty Krab",
                "category": "Restaurant",
                "location": "456 Oak Avenue, Los Angeles, CA 90001",
            },
            {
                "name": "Bob's Auto Repair",
                "category": "Auto Repair",
                "location": "789 Elm Street, Chicago, IL 60601",
            },
            {
                "name": "Sunrise Yoga Studio",
                "category": "Fitness",
                "location": "321 Wellness Blvd, Austin, TX 78701",
            },
            {
                "name": "Tech Haven Electronics",
                "category": "Electronics Store",
                "location": "654 Innovation Drive, Seattle, WA 98101",
            },
            {
                "name": "Bella's Boutique",
                "category": "Fashion Retail",
                "location": "987 Style Lane, Miami, FL 33101",
            },
            {
                "name": "Downtown Pet Grooming",
                "category": "Pet Services",
                "location": "147 Park Place, Denver, CO 80201",
            },
            {
                "name": "Alice's Wonderland Bakery",
                "category": "Bakery",
                "location": "258 Sweet Avenue, Boston, MA 02101",
            },
            {
                "name": "Kami-tachi tea shop",
                "category": "Cafe",
                "location": "369 Razor Road, Atlanta, GA 30301",
            },
            {
                "name": "Vee's Paradise",
                "category": "Bookstore",
                "location": "741 Library Lane, Portland, OR 97201",
            },
            {
                "name": "Fresh Market Grocery",
                "category": "Grocery Store",
                "location": "852 Farm Street, Nashville, TN 37201",
            },
            {
                "name": "Ocean Breeze onlinemart",
                "category": "Online Store",
                "location": "963 Relaxation Way, San Diego, CA 92101",
            },
        ]
        
        # Create business instances
        businesses_to_add = []
        for business_data in sample_businesses:
            business = Business(
                name=business_data["name"],
                category=business_data["category"],
                location=business_data["location"],
                aggregated_vibe_score=0.0,
                total_reviews=0
            )
            businesses_to_add.append(business)
        
        # Add all businesses to database
        db.add_all(businesses_to_add)
        db.commit()
        
        print(f"\n✓ Successfully added {len(businesses_to_add)} businesses to the database!")
        print("\nSample businesses added:")
        for idx, business in enumerate(businesses_to_add, 1):
            print(f"{idx}. {business.name} ({business.category})")
        
    except Exception as e:
        print(f"\n✗ Error occurred: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("VibeCheck Business - Database Population Script")
    print("=" * 60)
    print()
    populate_database()
    print()
    print("=" * 60)
