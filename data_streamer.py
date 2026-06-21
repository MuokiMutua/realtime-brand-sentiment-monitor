import pandas as pd
import random
import time
from datetime import datetime
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize the NLP Sentiment Engine
analyzer = SentimentIntensityAnalyzer()

TARGET_BANKS = ["GlobalBank", "NeoFi", "TrustUnion"]

# Realistic social media templates
POSITIVE_TEMPLATES = [
    "Just got my loan approved by {bank}! So fast. 🚀",
    "Loving the new app update from {bank}. Very smooth.",
    "Great customer service at {bank} today. Resolved my issue in 5 mins!",
    "Wow, {bank} waived my late fee. Thank you! 🙏",
    "Switched to {bank} and the UI is just lightyears ahead."
]

NEGATIVE_TEMPLATES = [
    "The {bank} app is down AGAIN. I can't access my money! 😡",
    "Hidden fees on my account. Leaving {bank} today. Unacceptable.",
    "Been on hold for 40 minutes with {bank} support. Useless.",
    "Why did {bank} block my card while I'm traveling?! Worst bank ever.",
    "Transfer failed but the money left my account. Fix this {bank}!"
]

NEUTRAL_TEMPLATES = [
    "Does anyone know what time the {bank} branch opens?",
    "Just received my new debit card from {bank} in the mail.",
    "Applying for a mortgage at {bank} tomorrow.",
    "Is the {bank} ATM network currently working?",
    "Reviewing the new interest rates posted by {bank}."
]

FILE_NAME = "live_mentions.csv"

def initialize_stream():
    """Creates the file with headers if it doesn't exist."""
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(columns=["Timestamp", "Bank", "Mention_Text", "Compound_Score", "Sentiment_Label"])
        df.to_csv(FILE_NAME, index=False)
        print(f"[✓] Created live database: {FILE_NAME}")

def generate_mention():
    """Simulates a single social media post."""
    bank = random.choice(TARGET_BANKS)
    
    # Weight the probability (mostly neutral, some positive, occasional negative spikes)
    sentiment_category = random.choices(
        [POSITIVE_TEMPLATES, NEGATIVE_TEMPLATES, NEUTRAL_TEMPLATES], 
        weights=[0.3, 0.2, 0.5], 
        k=1
    )[0]
    
    text = random.choice(sentiment_category).format(bank=bank)
    
    # Analyze the text using VADER NLP
    # Compound score is a normalized metric between -1 (extreme negative) and +1 (extreme positive)
    sentiment_dict = analyzer.polarity_scores(text)
    score = sentiment_dict['compound']
    
    # Categorize the score
    if score >= 0.05:
        label = "Positive"
    elif score <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
        
    return {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Bank": bank,
        "Mention_Text": text,
        "Compound_Score": score,
        "Sentiment_Label": label
    }

def start_firehose():
    initialize_stream()
    print(" Starting Social Media Firehose... (Press Ctrl+C to stop)")
    print("-" * 60)
    
    try:
        while True:
            # Generate 1 to 3 new mentions every cycle
            num_mentions = random.randint(1, 3)
            new_data = [generate_mention() for _ in range(num_mentions)]
            
            # Convert to dataframe and append to our CSV without writing headers again
            df = pd.DataFrame(new_data)
            df.to_csv(FILE_NAME, mode='a', header=False, index=False)
            
            # Print to terminal so we can watch it work
            for data in new_data:
                color = "🟢" if data['Sentiment_Label'] == 'Positive' else "🔴" if data['Sentiment_Label'] == 'Negative' else "⚪"
                print(f"{color} [{data['Timestamp']}] {data['Bank']}: {data['Compound_Score']:.2f} -> {data['Mention_Text']}")
            
            # Pause for 2-5 seconds before the next batch of tweets
            time.sleep(random.uniform(2.0, 5.0))
            
    except KeyboardInterrupt:
        print("\n Firehose stopped by user.")

if __name__ == "__main__":
    start_firehose()