from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs
import requests
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class Analisa_berita:
    def __init__(self):
        pass

    def scraping_berita(self):
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'
        headers = {'User-Agent': user_agent,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

        alamat = "https://nasional.kompas.com/read/2020/10/16/10154691/mahasiswa-demonstrasi-di-istana-jakarta-jokowi-kerja-di-istana-bogor"
        req = Request(alamat, headers=headers)
        html = urlopen(req)

        data = bs(html, 'html.parser')
        box = data.find("div",{"class":"read__content"})

        hidelabel = box.findAll('strong')
        for delete in hidelabel:
            delete.decompose()

        items = box.findAll('p')
        hasil = [item.get_text() for item in items]

        return hasil

    def preprocessing(self, hasil):
        hasil = [item.lower() for item in hasil]
        hasil = [' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", item).split()) for item in hasil]

        paragraf = ' '.join(hasil)
        stop_words = set(stopwords.words('indonesian'))
        word_tokens = word_tokenize(paragraf) 
        final_data = ' '.join([w for w in word_tokens if not w in stop_words])

        return final_data

    def visualisasi(self, final_data):
        wordcloud = WordCloud(width=1600, height=800, max_font_size=200, background_color="white").generate(final_data)
        plt.figure(figsize=(12,10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()

app = Analisa_berita()
data = app.scraping_berita()
clean_data = app.preprocessing(data)
app.visualisasi(clean_data)