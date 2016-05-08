import json, subprocess,urllib.request,urllib.request,urllib.parse
from flask import Flask, render_template,request, jsonify
import urllib.request



def apiCall(category):
    req = urllib.request.Request('https://api.twitch.tv/kraken/'+category)
    url = urllib.request.urlopen(req).read().decode("utf-8")
    return json.loads(url)

def apiGame(games):
    req = urllib.request.Request('https://api.twitch.tv/kraken/streams?game=' + games)
    url = urllib.request.urlopen(req).read().decode("utf-8")
    return json.loads(url)

def apiChannel(channel):
    req = urllib.request.Request('https://api.twitch.tv/kraken/channels/' + channel)
    url = urllib.request.urlopen(req).read().decode("utf-8")
    return json.loads(url)

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("index.html", call = apiCall('games/top?limit=5')['top'])

@app.route('/game/<games>')
def game(games):
    games = urllib.parse.quote(games)
    return render_template("games.html", call = apiGame(games)['streams'])

@app.route('/player/<channel>')
def player(channel):
    global cname
    cname = channel
    return render_template("player.html", channel = channel)

@app.route('/play', methods=['POST'])
def play():
    chname = cname
    qua = request.form.get('quality')
    cmd = ["livestreamer --player-external-http --player-external-http-port 8913 twitch.tv/"+chname+" "+qua]
    call1 = subprocess.call(cmd,shell=True)
    call1.terminate()
    call1.wait()



@app.route('/stop', methods=['POST'])
def stop():
    cmd = ["pkill livestreamer"]
    call2 = subprocess.call(cmd,shell=True)
    call2.terminate()
    call2.wait()

@app.route('/check', methods=['POST'])
def check():
    #cmd = ['nc -vn 127.0.0.1 8913']
    #p = subprocess.check_output(cmd,shell=True)
    return jsonify('test')
    #p.terminate()
    #p.wait()


if __name__ == '__main__':
    app.run()
