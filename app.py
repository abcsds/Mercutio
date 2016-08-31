#!/usr/bin/env python
# Setting up twitter API conection requiren oauth authentication
import oauth2 as oauth
import urllib2 as urllib
import json
from csv import DictReader
import os # Personal keys

apiKey = os.environ['apiKey']
apiSecret = os.environ['apiSecret']
accessTokenKey = os.environ['accessTokenKey']
accessTokenSecret = os.environ['accessTokenSecret']

# Create oauth tokens and signature
oauthToken    = oauth.Token(key=accessTokenKey, secret=accessTokenSecret)
oauthConsumer = oauth.Consumer(key=apiKey, secret=apiSecret)
signatureMethod = oauth.SignatureMethod_HMAC_SHA1()

# Create req handler
httpMethod   = 'GET'
httpHandler  = urllib.HTTPHandler(debuglevel=0)
httpsHandler = urllib.HTTPSHandler(debuglevel=0)
def twitterreq(url, method, parameters):
    '''Request handler for twitter API'''
    req = oauth.Request.from_consumer_and_token(oauthConsumer,
                                                token=oauthToken,
                                                http_method=httpMethod,
                                                http_url=url,
                                                parameters=parameters)
    req.sign_request(signatureMethod, oauthConsumer, oauthToken)
    headers = req.to_header()
    if httpMethod == 'POST':
      encodedPostData = req.to_postdata()
    else:
        encodedPostData = None
        url = req.to_url()
    opener = urllib.OpenerDirector()
    opener.add_handler(httpHandler)
    opener.add_handler(httpsHandler)
    response = opener.open(url, encodedPostData)
    return response

def fetch(term):
    if term:
        url = 'https://stream.twitter.com/1.1/statuses/filter.json?language=en&track=' + term
    else:
        url = 'https://stream.twitter.com/1.1/statuses/sample.json'
    parameters = [] # FEATURE: Could ask for specific parameters from API
    response = twitterreq(url, "GET", parameters)
    for line in response:
        yield line

# Emotional processing
cols = ['anger',
        'anticipation',
        'disgust',
        'fear',
        'joy',
        'negative',
        'positive',
        'sadness',
        'surprise',
        'trust']
dictFile  = 'static/dict.csv'
mainDict = {}

# Read dictionary from csv
with open(dictFile) as csvFile:
        reader = DictReader(csvFile)
        for row in reader:
            mainDict[row['Word']] = [int(row[i]) for i in cols]

def score(data):
    '''Score tweet by lexical analysis'''
    global mainDict
    try:
        tweet = json.loads(data)
        # FEATURE: change replace for regex
        line = tweet[u'text'].replace('.','').replace(',','').replace(';','').replace(':','').replace('\t',' ').replace('\n',' ')
        words = line.split(' ')
        tweetScore = [0] * 10
        for word in words:
            if word in mainDict:
                for i in range(len(tweetScore)):
                    tweetScore[i] += mainDict[word][i]
        if tweetScore:
            return tweetScore #, tweet[u'user'][u'screen_name'], tweet[u'text']
    except: # If there is any error while reading the json, skip
        pass


# Setting variable asyncMode
asyncMode = None
if asyncMode is None:
    try:
        import eventlet
        asyncMode = 'eventlet'
    except ImportError:
        pass
    if asyncMode is None:
        try:
            from gevent import monkey
            asyncMode = 'gevent'
        except ImportError:
            pass
    if asyncMode is None:
        asyncMode = 'threading'
    print('asyncMode is ' + asyncMode)

# monkey patching is necessary because this application uses a background
# thread
if asyncMode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif asyncMode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

# Start flask app
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, disconnect
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = myKeys.secretKey
socketio = SocketIO(app, async_mode=asyncMode)
streamThread = None
term = ''

def backgroundThread():
    '''Constantly emiting vectors'''
    global term
    try:
        for line in fetch(term):
            vector = score(line)
            if vector == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                continue
            if vector == None:
                continue
            socketio.emit('vector', vector, namespace='/', broadcast=True)
    except:
        print "ERROR: Stream stopped"
        raise

@app.route("/")
def index():
    global streamThread
    if streamThread is None:
        streamThread = Thread(target=backgroundThread)
        streamThread.daemon = True
        streamThread.start()
    return render_template('index.html', name=index)

@socketio.on('term') # FEATURE: authentication can be added here
def threadStream(word):
    '''Change the term being looked up'''
    global term
    term = word[u'data']
    # print "Looking up term:", word[u'data']

@socketio.on('connect')
def connect():
    emit('status', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0')
