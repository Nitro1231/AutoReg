import configparser
from AutoReg import *


config = configparser.ConfigParser()
config.read('user.key')
user_id, user_pw = config['user']['id'], config['user']['pw']
print('[UCI LOGIN INFO]', user_id, user_pw)


webreg = WebReg()
webreg.login(user_id, user_pw)
webreg.study_list()
webreg.logout()
