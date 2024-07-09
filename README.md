# NewsPulse-Daily
Batch Sentiment Analysis and Visualization Pipeline

## Project Overview
This project aims to create a dashboard that displays the sentiment analysis of daily news articles. The project involves scraping news data, performing sentiment analysis, and visualizing the results on a dashboard. The entire workflow is orchestrated using Apache Airflow and Docker.

## Project Workflow
1. Data Scraping: Scrape news articles from various sources.
2. Data Processing: Clean and preprocess the scraped data.
3. Sentiment Analysis: Perform sentiment analysis on the preprocessed news data.
4. Data Storage: Store the sentiment analysis results in a database.
5. Dashboard Visualization: Visualize the sentiment analysis results on a dashboard.
6. Automation: Automate the entire workflow using Apache Airflow.

## Technologies Used
Python: For data scraping, processing, and sentiment analysis.
Apache Airflow: To orchestrate and automate the workflow.
Docker: To containerize the application and ensure consistent environments.
PostgreSQL/MySQL: For storing the sentiment analysis results.
Dash/Plotly: For creating the interactive dashboard.

## Setup Instructions
### Prerequisites
1. Docker and Docker Compose installed
2. Python 3.7+ installed

### Step-by-Step Guide
1. Clone the repository
2. Install the requirements.txt
3. Download model from HuggingFace
4. Change the path of the model
5. Build Docker Containers
6. Initialize Airflow
7. Access Airflow
8. Run the DAGs

### How It Works
1. Scrape News Data: The scraper.py script scrapes news articles from specified sources and saves them in the data/raw/ directory.
2. Data Processing: The data_processing.py script cleans and preprocesses the scraped data.
3. Sentiment Analysis: The sentiment_analysis.py script performs sentiment analysis on the preprocessed data using a sentiment analysis model.
4. Store Results: The sentiment analysis results are stored in a PostgreSQL/MySQL database using the database.py script.
5. Visualize Data: The app.py and layout.py scripts in the dashboard/ directory create an interactive dashboard to visualize the sentiment analysis results.
