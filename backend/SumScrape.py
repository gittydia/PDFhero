import scrapy
from scrapy.crawler import CrawlerProcess
from textblob import TextBlob
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from string import punctuation
from heapq import nlargest
from collections import defaultdict
import nltk


nltk.download('punkt')
nltk.download('stopwords')


class SummaryWeb(scrapy.Spider):

    name = ''

    def __init__(self, url='', *args, **kwargs):
        super(SummaryWeb, self).__init__(*args, **kwargs)
        self.start_urls = [url] if url else []

    def parse(self, response):

        content = ' '.join(response.css('p::text').getall())
        title = response.css('title::text').get()
        return {'title': title, 'content': content}
    
class TextSummarizer:
    def  __init__(self):
        self.stopwords = set(stopwords.words('english') + list(punctuation))

    #tokenize the text
    def preprocess(self, text):

        sentences = sent_tokenize(text)
        word = word_tokenize(text.lower())
        words = [word for word in word if word not in self.stopwords]
        return sentences, words
    
    #calculate the frequency of each word
    def frequency(self, words):

        word_freq = defaultdict(int)
        for word in words:
            word_freq[word] += 1

        max_freq = max(word_freq.values())
        for word in words:
            max_freq[word] = max_freq[word] / max_freq

        return word_freq
    
    