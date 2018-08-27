# import the necessary packages
from threading import Thread
import requests
import time


import requests

url = "http://localhost:8080/function/scraper"

payload = "{\"url\":\"www.fb.com\"}"


def call_predict_endpoint(n):
    """
    call the predication api

    Args:
        n: ``int``
            called number
    
    """
    
    # submit the request
    r = requests.request("POST", url, data=payload)

    # ensure the request was sucessful
    if r.status_code==200:
        print("[INFO] thread {} OK".format(n))

    # otherwise, the request failed
    else:
        print("[INFO] thread {} FAILED".format(r.raw))

# loop over the number of threads
for i in range(0, 300):
    # start a new thread to call the API
    t = Thread(target=call_predict_endpoint, args=(i,))
    t.daemon = True
    t.start()
    time.sleep(0.05)
    
    
time.sleep(300)

