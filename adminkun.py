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
    response.encoding = 'SHIFT_JIS'
    soup = BeautifulSoup(response.text)
    links = []
    titles = []
    for node in soup.findAll('div', {'id': 'adminkun-new-articles'}):
        for tag in node.findAll('a', href=True):
            #  print(tag['href'])
            links.append(tag['href'])

        for tag in node.findAll('h4'):
            #  print(tag.string)
            titles.append(tag.string)

    episodes = []
    for (title, link) in zip(titles, links):
        episodes.append([title, link])

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
            url, title, uid = episode[1], episode[0], episode[1] + '\n'
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
