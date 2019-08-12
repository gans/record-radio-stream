#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import requests
from datetime import datetime

chunk_size = 1024 * 1024 # read 1MB on memory
max_size = chunk_size * 100 # max file size 100MB
stream_url = "http://198.100.150.244:8017/stream.aac"
r = f = None
current_size = 0

while True:
    try:
        r.close()
    except:
        pass

    try:
        r = requests.get(stream_url, stream=True)
    except:
        # server dies?
        print("unable to get stream chunks, waiting 60s...")
        time.sleep(60)
        continue

    print("{0} - starting chunks...".format(datetime.now().strftime("%Y%m%d%H%M%S")))
    for chunk in r.iter_content(chunk_size): # read in memory chunk_size bytes 
        # then white on disk

        if not chunk:
            # stream dead ?
            f.flush()
            f.close()
            f = None
            current_size = 0
            break

        if not f:
            filename = "{0}.aac".format(datetime.now().strftime("%Y%m%d-%H-%M"))
            f = open(filename, "wb")

        f.write(chunk)
        f.flush()
        current_size += chunk_size
        print("{0} - {1}".format(datetime.now().strftime("%Y%m%d%H%M%S"), current_size))
        if current_size >= max_size:
            current_size = 0
            f.close()
            f = None

            


