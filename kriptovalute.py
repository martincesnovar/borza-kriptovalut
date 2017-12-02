from bottle import *
import modeli

################################################
# PRVA 

@get('/')
def glavniMenu():
    return template('index.html')


run(host = 'localhost', port=8080)
