from extract import extract
from transform import sentiment_analysis
from load import load_to_postgresql
from wordclouds import generate_wordclouds

def ml_pipeline():
    data = extract()
    data = sentiment_analysis(data)
    generate_wordclouds(data)
    load_to_postgresql(data)