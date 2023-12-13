#!/usr/bin/env python3
# database_functions.py

from google.cloud import firestore

account_key_file = "<fill in own account key file>"
db = firestore.Client.from_service_account_json(account_key_file)

def save_sentiment_in_db(timestamp, text, sentiment, confidence):
   db.collection('sentiments').add({
        'timestamp': timestamp,
        'text': text, 
        'sentiment': sentiment,
        'confidence': confidence
    })

def get_sentiments():
	return db.collection('sentiments').stream()
