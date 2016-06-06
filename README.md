# Mercutio
Twitter stream processing, emotion extraction and sonification using [Flask](http://flask.pocoo.org/) and [Tone.js](https://github.com/Tonejs/Tone.js).

## Run
This app requires twitter API keys, in a file called `myKeys.py`. After writing your keys as variables like these:
```python
apiKey = 'yourapiKey'
apiSecret = 'yourapiSecret'
accessTokenKey = 'youraccessTokenKey'
accessTokenSecret = 'youraccessTokenSecret'
secretKey = 'yoursecretKey'
```
You can run the app on a local environment by calling it with python:
```python
python app.py
```

## Deploy
Deployment on a server requires docker. This is how I have done it:

- Install docker and git
- Clone repo: `git clone https://github.com/abcsds/Mercutio`
- Write your API keys file.
- Build: `docker build -t mercutio:latest .`
- Run app: `docker run --name mercutio -p 80:5000 -d mercutio`

In this example I've used an AWS t2.micro server, with a reverse proxy to manage several entrance domains or subdomains.
