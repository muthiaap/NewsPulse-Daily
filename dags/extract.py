import requests
import re
from bs4 import BeautifulSoup as BS
import newspaper
import tempfile
import os
from newspaper import Article, Config
import preprocessor as p
import pandas as pd
import urllib.parse
import logging
from datetime import date
from datetime import timedelta
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from airflow.decorators import task

@task(task_id = 'Extraction')
def extract():
    # giving list of sites that gonna be taken
    list_of_sites = [
        ('eco-business.com', 'en'),
        ('thejakartapost.com', 'en'),
        ('tempo.co', 'id'),
        ('greenpeace.org', 'id'),
        ('enternusantara.org', 'id'),
        ('mongabay.co.id', 'id'),
        ('ecoton.or.id', 'id'),
        ('betahita.id', 'id'),
        ('cnnindonesia.com', 'id'),
        ('cnbcindonesia.com', 'id'),
        ('detik.com', 'id'),
        ('republika.id', 'id'),
        ('kontan.co.id', 'id'),
        ('tambang.co.id', 'id'),
        ('topbusiness.id', 'id'),
        ('viva.co.id', 'id'),
        ('investortrust.id', 'id'),
        ('investor.id', 'id'),
        ('indopos.co.id', 'id'),
        ('katadata.co.id', 'id'),
        ('beritasatu.com', 'id'),
        ('kompasiana.com', 'id'),
        ('wartaekonomi.co.id', 'id'),
        ('sinergipos.com', 'id'),
        ('antaranews.com', 'id'),
        ('kompas.id', 'id'),
        ('republika.co.id', 'id'),
        # ('infobanknews.com', 'id'),
        ('bisnis.com', 'id'),
        ('medcom.id', 'id'),
        ('rakyatjelata.com', 'id'),
        ('baznas.go.id', 'id'),
        ('jakartaglobe.id', 'id'),
        # ('emitennews.com', 'id'),
        ('sudutpandang.id', 'id'),
        ('majalahlintas.com', 'id'),
        ('bisnisnews.id', 'id'),
    ]

    # the website and header
    GOOGLE = 'https://www.google.com/search'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}

    # Initialize logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Starting news extraction process')

    links = []
    MAX_ARTICLES = 20

    yesterday = date.today() - timedelta(days=1)

    def get_query(site, company) -> str:
        date_str = yesterday.strftime('%Y-%m-%d')
        return f"site:{site} after:{date_str} {company}"

    company = 'BBNI'

    # Set up retry strategy
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    for site in list_of_sites:
        query = get_query(site[0], company)

        params = {
            'q': query,
            'num': 10 
        }

        response = http.get(GOOGLE, params=params, headers=headers)
        response.raise_for_status()
        soup = BS(response.text, 'lxml')
        links += soup.find_all("a")[16:]

        if len(links) >= MAX_ARTICLES:
            links = links[:MAX_ARTICLES]
            break
    
    # collecting the URL
    url_collection = []

    for link in links:
        str_link = str(link)
        if str_link.find('/url?q=') == -1 or 'accounts.google.com' in str_link or 'support.google.com' in str_link:
            continue
        # doing parse 
        url = str_link[str_link.find('/url?q='):str_link.find('>')]
        url_parsed = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)['q'][0]
        url_collection.append(url_parsed)
    
    newspaper.settings.TOP_DIRECTORY = tempfile.gettempdir()

    # User agent and configuration for newspaper
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 60

    p.set_options(p.OPT.MENTION, p.OPT.EMOJI, p.OPT.HASHTAG, p.OPT.RESERVED, p.OPT.SMILEY, p.OPT.URL)

    # Text cleaner function
    def cleaner(text):
        text = re.sub("@[A-Za-z0-9]+", "", text)  # Remove @ sign
        text = text.replace("#", "").replace("_", "")  # Remove hashtag sign but keep the text
        text = p.clean(text)  # Clean text from any mention, emoji, hashtag, reserved words, smiley, and url
        text = text.strip().replace("\n", "")
        return text

    # take the text from all the sites
    news_text = []

    for url in url_collection:
        if "http" not in url:
            continue
        lang = "id"
        if "eco-business.com" in url or "thejakartapost.com" in url:
            lang = "en"
        try:
            article = Article(url, language=lang, config=config)
            article.download()
            article.parse()
            article_clean = cleaner(article.text)
            news_text.append(article_clean)
            logging.info(f'Successfully extracted article from {url}')
        except newspaper.ArticleException as e:
            logging.error(f'Error processing article from {url}: {e}')
        except Exception as e:
            logging.error(f'Unexpected error processing article from {url}: {e}')

    # create dataframe
    df = pd.DataFrame({'news': news_text})
    logging.info('News extraction process completed')
    
    return df