# -*- coding: utf-8 -*-
import base64
import binascii
import datetime
import json
import os
import re
from urllib import parse

import requests
import rsa
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from bs4 import BeautifulSoup
from requests import exceptions

with open('config.json', mode='r', encoding='utf-8') as f:
    config = json.loads(f.read())


def writeLog(content):
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = 'mylogs/' + date + '.log'
    if not os.path.exists(filename):
        with open(filename, mode='w', encoding='utf-8') as n:
            n.write('【%s】的日志记录' % date)
    with open(filename, mode='a', encoding='utf-8') as l:
        l.write('\n%s' % content)


class Login(object):
    def __init__(self, base_url):
        self.base_url = base_url
        self.key_url = parse.urljoin(base_url, '/xtgl/login_getPublicKey.html')
        self.login_url = parse.urljoin(base_url, '/xtgl/login_slogin.html')
        self.headers = requests.utils.default_headers()
        self.headers["Referer"] = self.login_url
        self.headers["User-Agent"] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        self.headers["Accept"] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        self.sess = requests.Session()
        self.req = ''
        self.cookies = ''
        self.cookies_str = ''
        self.runcode = 1
        if config["proxy"] == "none":
            self.proxies = None
        else:
            self.proxies = {
                'http': config["proxy"]
            }

    def login(self, sid, password):
        """登陆"""
        try:
            # print("开始...")
            req = self.sess.get(self.login_url, headers=self.headers, proxies=self.proxies, timeout=3)
            # print('加载登录页面...')
            soup = BeautifulSoup(req.text, 'lxml')
            tokens = soup.find(id='csrftoken').get("value")
            # print('获取token...')
            res = self.sess.get(self.key_url, headers=self.headers, proxies=self.proxies, timeout=3).json()
            # print('获取公钥...')
            n = res['modulus']
            e = res['exponent']
            hmm = self.get_rsa(password, n, e)
            # print('解密编码...')

            login_data = {'csrftoken': tokens,
                          'yhm': sid,
                          'mm': hmm}
            self.req = self.sess.post(self.login_url, headers=self.headers, data=login_data, proxies=self.proxies,
                                      timeout=3)
            # print('登录请求...')
            ppot = r'用户名或密码不正确'
            if re.findall(ppot, self.req.text):
                self.runcode = 2
                return self.runcode
            self.cookies = self.sess.cookies
            self.cookies_str = '; '.join([item.name + '=' + item.value for item in self.cookies])
            self.runcode = 1
        except exceptions.Timeout:
            # requests.get('https://sc.ftqq.com/SCU48704T2fe1a554a1d0472f34720486b88fc76e5cb0a8960e8be.send?text=登录超时&desp=' + str(e))
            content = ('【%s】[%s]登录超时！' % (datetime.datetime.now().strftime('%H:%M:%S'), sid))
            writeLog(content)
            self.runcode = 3
            return {'err': 'Connect Timeout'}

    @classmethod
    def encrypt_sqf(cls, pkey, str_in):
        """加载公钥"""
        private_key = pkey

        private_keybytes = base64.b64decode(private_key)
        prikey = RSA.importKey(private_keybytes)
        # noinspection PyTypeChecker
        signer = PKCS1_v1_5.new(prikey)
        signature = base64.b64encode(signer.encrypt(str_in.encode("utf-8")))
        return signature

    @classmethod
    def get_rsa(cls, pwd, n, e):
        """对密码base64编码"""
        message = str(pwd).encode()
        rsa_n = binascii.b2a_hex(binascii.a2b_base64(n))
        rsa_e = binascii.b2a_hex(binascii.a2b_base64(e))
        key = rsa.PublicKey(int(rsa_n, 16), int(rsa_e, 16))
        encropy_pwd = rsa.encrypt(message, key)
        result = binascii.b2a_base64(encropy_pwd)
        return result
