"""
File: test_config.py
Author: Yuri Golub
Email: yuri.golub@gmail.com
Github: https://github.com/BeProduct
Description:
"""
import os
import json


class TestConfiguration(object):

    """ Test configuration """

    def __init__(self):
        """ Setting up variables """
        self.TEST_DIR = os.path.dirname(os.path.realpath(__file__))

        # load default.json first
        self.set_conf('default')

        # auth
        self.set_conf('auth')
        if 'CLIENT_ID' not in dir(self):
            self.CLIENT_ID = os.environ.get('CLIENT_ID')
            self.CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
            self.REFRESH_TOKEN = os.environ.get('REFRESH_TOKEN')
            self.COMPANY_DOMAIN = os.environ.get('COMPANY_DOMAIN')

        if self.COMPANY_DOMAIN:
            self.set_conf(self.COMPANY_DOMAIN)

    def set_conf(self, *args):
        """ Sets properties of config classes from local files """
        for arg in args:
            if os.path.exists(os.path.join(self.TEST_DIR, 'configs', arg + '.json')):
                with open(os.path.join(
                        self.TEST_DIR, 'configs', arg + '.json'), 'r') as f:
                    conf_dict = json.load(f)
                for k in conf_dict:
                    self.__setattr__(k, conf_dict[k])

            elif os.path.isdir(os.path.join(self.TEST_DIR, 'configs', arg)):
                for json_file in os.listdir(
                        os.path.join(self.TEST_DIR, 'configs', arg)):
                    with open(
                            os.path.join(self.TEST_DIR, 'configs',
                                         arg, json_file),
                            'r') as f:
                        conf_dict = json.load(f)
                        for k in conf_dict:
                            self.__setattr__(
                                json_file.replace('.json', '').upper(), conf_dict)
