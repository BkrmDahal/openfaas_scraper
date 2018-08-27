import json
from collections import Counter
import time
import requests
from bs4 import BeautifulSoup

# req = '{"url":"http://www.fb.com", "thershold": 2}'

stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", 
             "you", "your", "yours", "yourself", "yourselves", "he", "him",
             "his", "himself", "she", "her", "hers", "herself", "it", "its", 
             "itself", "they", "them", "their", "theirs", "themselves", "what", 
             "which", "who", "whom", "this", "that", "these", "those", "am", 
             "is", "are", "was", "were", "be", "been", "being", "have", "has", 
             "had", "having", "do", "does", "did", "doing", "a", "an", "the", 
             "and", "but", "if", "or", "because", "as", "until", "while", "of",
             "at", "by", "for", "with", "about", "against", "between", "into", 
             "through", "during", "before", "after", "above", "below", "to", 
             "from", "up", "down", "in", "out", "on", "off", "over", "under", 
             "again", "further", "then", "once", "here", "there", "when", 
             "where", "why", "how", "all", "any", "both", "each", "few", 
             "more", "most", "other", "some", "such", "no", "nor", "not", 
             "only", "own", "same", "so", "than", "too", "very", "s", "t", 
             "can", "will", "just", "don", "should", "now"]

def clean_html(text, stopwords, threshold):
    """clean html and removed stopwords"""
    soup  = BeautifulSoup(text, 'html.parser')
    soup.get_text()
    url = "test"

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = text.lower()

    text_list = text.split(' ')

    # remove stop words
    text_list = [i for i in text_list if i not in stopwords]

    return text, text_list
  
  

def handle(req):
    "Main funcation that return the ouput"
    t1 = time.time()
    json_req = json.loads(req)
    
    # get threshold if aviable
    threshold = json_req.get('threshold', 2)
    url = json_req["url"]
    if "http" not in url:
        url = "http://"+url
    
    r = requests.get(url)
    
    text, text_list = clean_html(r.text, stopwords, threshold)
    
    # count words and remove words less than threshold
    dict_counts = dict(Counter(text_list).most_common())
    dict_counts = {i:j for i, j in dict_counts.items() if j >= threshold}
    t2 = time.time()
    return json.dumps({'status':'ok', 
                     'url':url,
			"word_count":len(text_list),
                      'text_counts': dict_counts,
                     'text': text,
                       'time':t2-t1
                     })


