#!/usr/bin/env python3
# sentiment_functions.py

import random

def analyze_sentiment(text: str) -> tuple:
    # Replace this by your favorite ML algo
    sentiments = ['positive', 'negative', 'neutral']
    random_sentiment = random.choice(sentiments)
    random_confidence = random.uniform(0.5, 1.0)
    return random_sentiment, random_confidence