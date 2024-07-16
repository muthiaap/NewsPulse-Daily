import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
from airflow.decorators import task

@task(task_id = 'Transformation')
def sentiment_analysis(df, text_column='news'):
    # Load the tokenizer and model
    tokenizer_sentiment = AutoTokenizer.from_pretrained("saved_model")
    model_sentiment = AutoModelForSequenceClassification.from_pretrained("saved_model")

    # using normal distribution to weighted scoring
    def get_chunk_weights(num_chunks):
        center = num_chunks / 2
        sigma = num_chunks / 4
        weights = [np.exp(-0.5 * ((i - center) / sigma) ** 2) for i in range(num_chunks)]
        weights = np.array(weights)
        return weights / weights.sum()

    def tokenize_and_chunk(text, tokenizer, chunk_size=512):
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        input_ids = inputs['input_ids'][0]
        chunks = [input_ids[i:i+chunk_size] for i in range(0, len(input_ids), chunk_size)]
        return chunks

    def analyze_sentiment(text, tokenizer, model):
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
        labels = ["positive", "neutral", "negative"]
        predicted_sentiment = labels[predicted_class]
        return predicted_sentiment

    # sentiment result
    sentiments = []
    for text in df[text_column]:
        if isinstance(text, str):
            chunks = tokenize_and_chunk(text, tokenizer_sentiment)
            chunk_weights = get_chunk_weights(len(chunks))
            chunk_sentiments = []

            for chunk in chunks:
                chunk_text = tokenizer_sentiment.decode(chunk, skip_special_tokens=True)
                sentiment = analyze_sentiment(chunk_text, tokenizer_sentiment, model_sentiment)
                chunk_sentiments.append(sentiment)

            # Weighted scoring for sentiment
            sentiment_scores = {"positive": 1, "neutral": 0, "negative": -1}
            weighted_score = sum(chunk_weights[i] * sentiment_scores[sent] for i, sent in enumerate(chunk_sentiments))
            if weighted_score > 0.5:
                aggregated_sentiment = "positive"
            elif weighted_score < -0.5:
                aggregated_sentiment = "negative"
            else:
                aggregated_sentiment = "neutral"

            sentiments.append(aggregated_sentiment)
        else:
            sentiments.append("neutral")  # Handle non-string entries

    # create dataframe
    df['sentiment'] = sentiments
    return df