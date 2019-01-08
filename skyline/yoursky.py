#
#   Constructs URL and fetches image from Fourmilab Yoursky
#

import random
from multiprocessing.dummy import Pool as ThreadPool  # multiprocessing.dummy is a wrapper around threading
from io import BytesIO
from urllib import request
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from PIL import Image
from fwriter import Writer

class Yoursky:

    url_site = "https://www.fourmilab.ch"
    img_tags = SoupStrainer("img")

    def __init__(self, imgsize, lmag, n, using_pdf):

        self.n = n
        self.fwriter = Writer(n, using_pdf)

        # URL containing image parameters
        # scheme=1 : sets image colour scheme to black on white
        # dynimg=y : dynamically generates image but more importantly generates a much smaller HTML
        #            (not sure if this speeds up BeautifulSoup enough to warrant it)
        url_base = "/cgi-bin/Yoursky?date=0&limag={}&imgsize={}&scheme=1".format(lmag, imgsize)
        # generates list of URLs
        self.urls = [self._gen_url(url_base) for _ in range(n)]

    # returns URL with randomized coordinates
    def _gen_url(self, url_base):

        lat = random.uniform(-90.0, 90.0)
        lon = random.uniform(-180.0, 180.0)

        chunks = [self.url_site, url_base, "&lat={}%B0&lon={}%B0&".format(lat, lon)]
        return "".join(chunks)

    # downloads image
    def _get_img(self, url):

        # load page and search HTML for image source
        page = request.urlopen(url)

        soup = BeautifulSoup(page, features="html.parser", parse_only=self.img_tags)
        src = "{}{}".format(self.url_site, soup.img['src'])

        # get bytes from image source
        imghttp = request.urlopen(src)
        imgb = BytesIO(imghttp.read())
        return Image.open(imgb)

    # starts fetching images
    def fetch_imgs(self):

        # use only a maximum of 20 threads
        pool = ThreadPool(self.n if self.n <= 20 else 20)

        # passes image bytes to Writer when each thread is complete
        for url in self.urls:
            pool.apply_async(self._get_img, (url, ), callback=self.fwriter.write)

        # indicate no more jobs to be sent to pool
        pool.close()
        # blocks until all jobs are done
        pool.join()

        # starts writing to PDF if using_pdf == True
        self.fwriter.close()
