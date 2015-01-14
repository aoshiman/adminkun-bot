# -*- coding: utf-8 -*-

import requests
from twython import Twython, TwythonError
try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
from docopt import docopt
import conf
from setting import DOMAIN, END_POINT, TEXT, UA


__usage__="""
Usage:
    adminkun.py tweet [--user=<account>] [--no-tweet]

Options:
    -h --help           Show this screen
    --version           Show version
    --user=<account>    tweet user [default: ad_min_kun]
    --no-tweet          tweet to stdout

"""


def fetch_episodes():
    headers = {'User-Agent': UA}
    response = requests.get(DOMAIN + END_POINT, headers=headers)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text)
    episodes = []
    for node in soup.findAll('div', {'class': 'newbox'}):
        for tag in node('table', {'width': '100%', 'cellpadding': '3'}):
            for atag in tag('a'):
                if atag.string != None:
                    episodes.append([atag['href'], atag.string])
    episodes.reverse()
    return episodes


def get_list(f):
    try:
        with open(f) as fp:
            return fp.readlines()
    except:
        pass


def tweet_episode():
    """OAuth setting and Twit(if episode is new)"""
    args = docopt(__usage__)
    config = conf.ParseConf()
    oauth_conf = config.get_items('oauth_conf')
    if args['--user']:
        access_conf = config.get_items(args['--user'])
    twitter = Twython(
    oauth_conf['consumer_key'],
    oauth_conf['consumer_secret'],
    access_conf['access_token'],
    access_conf['access_secret']
    )

    lines = get_list(TEXT)
    episodes = fetch_episodes()
    with open(TEXT, 'a+') as fp:
        for episode in episodes:
            url, title, uid = episode[0], episode[1], episode[0] + '\n'
            if not lines or uid not in lines:
                post = u'{0} {1}'.format(title, url)
                if args['--no-tweet']:
                    print(post)
                else:
                    try:
                        twitter.update_status(status = post)
                    except TwythonError as e:
                        print(e)
                fp.write(uid)

if __name__ == '__main__':
    tweet_episode()
