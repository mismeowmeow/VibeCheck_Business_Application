"""
Model Download Script
Run this script BEFORE starting the server to download the sentiment analysis model.

Usage:
    python download_model.py
"""

print("=" * 70)
print("VibeCheck Business - Model Download Script")
print("=" * 70)
print()
print("This will download the DistilBERT sentiment analysis model (~268MB)")
print("Please ensure you have a stable internet connection.")
print("This may take 5-10 minutes depending on your internet speed.")
print()

import sys

try:
    from transformers import pipeline
    
    print("Starting download...")
    print()
    
    # This will download the model
    classifier = pipeline("sentiment-analysis")
    
    print()
    print("✓ Model downloaded successfully!")
    print()
    
    # Test the model
    print("Testing the model...")
    result = classifier("This is a great product!")
    print(f"Test result: {result}")
    print()
    
    print("=" * 70)
    print("✓ Setup complete! You can now run: uvicorn app.main:app --reload")
    print("=" * 70)
    
except Exception as e:
    print()
    print("✗ Error occurred during download:")
    print(f"  {str(e)}")
    print()
    print("Troubleshooting:")
    print("1. Check your internet connection")
    print("2. Try running again: python download_model.py")
    print("3. If error persists, delete cache folder:")
    print("   C:\\Users\\dell\\.cache\\huggingface\\")
    print()
    sys.exit(1)
