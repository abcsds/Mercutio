#!/usr/bin/env python
import oauth2 as oauth
import urllib2 as urllib
import json
from csv import DictReader
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


# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on available packages.
async_mode = None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, disconnect
from threading import Thread


# Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = myKeys.secret_key
socketio = SocketIO(app, async_mode=async_mode)
streamThread = None
term = ''

def background_thread():
    '''Constantly emiting vectors'''
    global term
    try:
        for line in fetch(term):
            vector = score(line)
            if vector == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                continue
            socketio.emit('vector', vector, namespace='/', broadcast=True)
    except:
        print "ERROR: Stream stopped"
        raise

@app.route("/")
def index():
    global streamThread
    if streamThread is None:
    #     streamThread = eventlet.greenthread.spawn(stream)
        streamThread = Thread(target=background_thread)
        streamThread.daemon = True
        streamThread.start()
    return render_template('index.html', name=index)

@socketio.on('term') # FEATURE: authentication can be added here
def threadStream(word):
    '''Change the term being looked up'''
    global term
    term = word[u'data']

@socketio.on('connect')
def connect():
    emit('status', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

if __name__ == "__main__":
    # socketio.run(app, debug=True)
    socketio.run(app)
