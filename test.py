import json, subprocess,urllib.request,urllib.request,urllib.parse, flask_login
from flask import Flask, render_template,request, jsonify, redirect, url_for
import urllib.request
from subprocess import PIPE
from flask_login import LoginManager, UserMixin

app = Flask(__name__)
app.secret_key= "JKDLASnlkva9312@&*#!)@015DA"
lm = LoginManager()
lm.init_app(app)



class User(UserMixin):
    pass

users = {'kpmu': {'pw': '1234'}}

@lm.user_loader
def user_load(nick):
    if nick not in users:
        return

    user = User()
    user.id = nick
    return user


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='nick' id='nick' placeholder='id'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''


    nick = request.form['nick']
    if request.form['pw'] == users[nick]['pw']:
            user = User()
            user.id = nick
            flask_login.login_user(user,remember=True)
            return redirect('/')
    return "Very bad login"



@app.route('/')
@app.route('/streams')
@app.route('/streams/<int:id>')
def main(id=0):
    qq = id
    if id > 0:
        qq = id * 5
    return render_template("index.html", call = apiCall(qq)['top'],id=id)


@app.route('/game/<games>')
@app.route('/game/<games>/<int:id>')
@flask_login.login_required
def game(games,id=0):
    qq = id
    if id > 0:
        qq = id * 5
    games = urllib.parse.quote(games)
    return render_template("games.html", call = apiGame(games,qq)['streams'],id=id,games=games)

@app.route('/player/<channel>')
@flask_login.login_required
def player(channel):
    return render_template("player.html", channel = channel)

@lm.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized login, Please do not do that'

@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return 'Logged out'

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
    app.run(debug=True)

