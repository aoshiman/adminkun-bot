# -*- coding: utf-8 -*-

import os
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

class ParseConf(object):
    _config_file_initial_content = """
#Examples of valid configurations:
#[twitter-@ham]
#token=xxxxxxxxxxxxxxxxxx
#secret=yyyyyyyyyyyyyyyyy
#
#[twitter-@spam]
#token=xxxxxxxxxxxxxxxxxx
#secret=yyyyyyyyyyyyyyyyyy
"""

    def __init__(self, config_file='~/.twibot'):
        self._config_file = config_file
        self.config_file = os.path.expanduser(self._config_file)
        self.config = configparser.RawConfigParser()
        self.config.read(self.config_file)

        if not os.path.isfile(self.config_file):
            self.create_config_file()


    def create_config_file(self):
        with open(self._config_file, 'w') as f:
            f.write(self._config_file_initial_content)
        print('Created sample configurations, Please edit as your setting')



    def get_sections(self):
        sections = self.config.sections()
        return sections


    def get_items(self, account):
        items = self.config.items(account)
        return dict(items)


    def get_token(self, account, token):
        try:
            token = self.config.get(account, token)
        except:
            token = None
        return token
