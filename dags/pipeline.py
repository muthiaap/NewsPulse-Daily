from extract import extract
from transform import sentiment_analysis
from load import load_to_postgresql

def ml_pipeline():
    data = extract()
    data = sentiment_analysis(data)
    load_to_postgresql(data)