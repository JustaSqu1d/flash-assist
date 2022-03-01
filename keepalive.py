from flask import Flask, render_template
from threading import Thread
from replit import db

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

@app.route('/<stats>/<int:id>/')
def API(stats,id):
    try:
      data = db[str(id)]["stats"][stats]
    except:
      return ""
    return data

@app.route('/ed/<stat>/')
def API2(stat):
  try:
    data = db["enderdragon"][stat]
  except:
    return ""
  return data

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()