import pandas as pd
from airflow.decorators import task
from wordcloud import WordCloud, STOPWORDS

@task(task_id='wordcloud_task')
def generate_wordclouds(df):
    WORDCLOUD_SAVE_PATH = "C:\\Users\\Muthia\\Downloads\\cw1.png"
    words_to_remove = ["bni", "dan", 'dengan', 'di', 'itu', 'yang', 'pada', 'juga', 'dalam', 'dari', 'untuk', 'ke', 'ini']
    
    def remove_words(text, words_to_remove):
        for word in words_to_remove:
            text = text.replace(word, '')
        return text
    
    df['news'] = df['news'].dropna().apply(lambda x: remove_words(x, words_to_remove))

    text = ' '.join(df['news'].dropna())

    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=STOPWORDS).generate(text)

    wordcloud.to_file(WORDCLOUD_SAVE_PATH)
    print(f"Word cloud image saved to {WORDCLOUD_SAVE_PATH}")

    return WORDCLOUD_SAVE_PATH