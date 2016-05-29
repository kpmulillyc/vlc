import json, subprocess,urllib.request,urllib.request,urllib.parse
from flask import Flask, render_template,request, jsonify
import urllib.request
from subprocess import PIPE



def apiCall(entries):
    req = urllib.request.Request('https://api.twitch.tv/kraken/games/top?limit=5&offset='+str(entries))
    url = urllib.request.urlopen(req).read().decode("utf-8")
    return json.loads(url)

def apiGame(games,entries):
    req = urllib.request.Request('https://api.twitch.tv/kraken/streams?game=' + games+"&limit=5&offset="+str(entries))
    url = urllib.request.urlopen(req).read().decode("utf-8")
    return json.loads(url)

def apiChannel(channel):
    req = urllib.request.Request('https://api.twitch.tv/kraken/channels/' + channel)
    url = urllib.request.urlopen(req).read().decode("utf-8")
    return json.loads(url)

def search(query):
    req = urllib.request.Request('https://api.twitch.tv/kraken/search/channels?q=' + query)
    url = urllib.request.urlopen(req).read().decode("utf-8")
    return json.loads(url)

app = Flask(__name__)

@app.route('/')
@app.route('/<int:id>')
def main(id=0):
    qq = id
    if id > 0:
        qq = id * 5
    return render_template("index.html", call = apiCall(qq)['top'],id=id)

@app.route('/game/<games>')
@app.route('/game/<games>/<int:id>')
def game(games,id=0):
    qq = id
    if id > 0:
        qq = id * 5
    games = urllib.parse.quote(games)
    return render_template("games.html", call = apiGame(games,qq)['streams'],id=id,games=games)

@app.route('/player/<channel>')
def player(channel):
    return render_template("player.html", channel = channel)

@app.route('/play')
def play():
    qua = request.args.get('quality')
    chname = request.args.get('channel')
    cmd = ["livestreamer --player-external-http --player-external-http-port 8913 twitch.tv/"+chname+" "+qua]
    p = subprocess.call(cmd,shell=True)
    p.terminate()
    p.wait()



@app.route('/stop', methods=['POST'])
def stop():
    cmd = ["pkill livestreamer"]
    hi = "good"
    p = subprocess.call(cmd,shell=True)
    p.terminate()
    p.wait()
    return hi

@app.route('/check')
def check():
    cmd = ["nc -vn 127.0.0.1 8913"]
    p = subprocess.Popen(cmd,shell=True,stdin=PIPE,stdout=PIPE,stderr=PIPE)
    output, error = p.communicate()
    if p.returncode==0:
        return jsonify(result="Server is running")
    else:
        return jsonify(result="Server is DOWN")
    p.terminate()
    p.wait()

if __name__ == '__main__':
    app.run()

