from flask import Flask, render_template
from threading import Thread
#from replit import db
import os 

app = Flask('')

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/privacy-policy')
def web2():
  return render_template('policy.html')

@app.route('/terms')
def web3():
  return render_template('tos.html')

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()