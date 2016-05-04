from flask import Flask, Response, request, render_template
from flask_socketio import SocketIO, emit
import oauth2 as oauth
import urllib2 as urllib
import json
from csv import DictReader
import eventlet
eventlet.monkey_patch()
import myKeys # Personal keys

api_key = myKeys.api_key
api_secret = myKeys.api_secret
access_token_key = myKeys.access_token_key
access_token_secret = myKeys.access_token_secret

# Create oauth tokens and signature
oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)
signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

# Create req handler
http_method = "GET"
http_handler  = urllib.HTTPHandler(debuglevel=0)
https_handler = urllib.HTTPSHandler(debuglevel=0)
def twitterreq(url, method, parameters):
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url,
                                             parameters=parameters)
    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)
    headers = req.to_header()
    if http_method == "POST":
      encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()
    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)
    response = opener.open(url, encoded_post_data)
    return response

def fetch(term):
    if term:
        url = "https://stream.twitter.com/1.1/statuses/filter.json?language=en&track=" + term
    else:
        url = "https://stream.twitter.com/1.1/statuses/sample.json"
    parameters = []
    response = twitterreq(url, "GET", parameters)
    for line in response:
        yield line

# Emotional processing
cols = ['anger', 'anticipation', 'disgust', 'fear',
        'joy', 'negative', 'positive', 'sadness',
        'surprise', 'trust']
dictFile  = 'dict.csv'
mainDict = {}

with open(dictFile) as csvFile:
        reader = DictReader(csvFile)
        for row in reader:
            mainDict[row['Word']] = [int(row[i]) for i in cols]

# Scoring function
def score(data):
    global mainDict
    try:
        tweet = json.loads(data)
        line = tweet[u'text'].replace('.','').replace(',','').replace(';','').replace(':','').replace('\t',' ').replace('\n',' ')
        words = line.split(' ')
        tweetScore = [0] * 10
        for word in words:
            if word in mainDict:
                for i in range(len(tweetScore)):
                    tweetScore[i] += mainDict[word][i]
        if tweetScore:
            return tweetScore
    except KeyError: # If tweet is empty, continue.
        pass
    except ValueError: # JSON could come empty too.
        pass
    except:
        pass

# Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = myKeys.secret_key
socketio = SocketIO(app)
streamThread = None
threadFlag = False

@app.route("/")
def index():
    return render_template('index.html', name=index)

@socketio.on('term')
def threadStream(term):
    global streamThread, threadFlag
    if not threadFlag:
        threadFlag = True
        streamThread = eventlet.greenthread.spawn(stream, term, request)
    else:
        emit('error', 'Too many connections')

def stream(term, req):
    with app.test_request_context():
        request = req
        try:
            for line in fetch(term[u'data']):
                vector = score(line)
                if vector == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                    continue
                socketio.emit('vector', vector)
        except:
            print "ERROR: Stream stopped"
            raise

@socketio.on('disconnect')
def disconnect():
    try:
        global streamThread, threadFlag
        print('Client disconnected, killing stream')
        eventlet.greenthread.kill(streamThread)
        threadFlag = False
        print('Stream killed')
    except AttributeError:
        pass

if __name__ == "__main__":
    # socketio.run(app, debug=True)
    socketio.run(app)
