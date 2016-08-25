import sys
import json
import stream
import csv

''' Extraction of twitter scores from file to stdout '''

def main():
    if len(sys.argv) != 3:
        print '''Usage:
        python test02.py <Dictionary CSV> <Tweeter stream json>'''
        sys.exit(0)

    dictFile  = sys.argv[1]
    tweetFile = open(sys.argv[2])

    cols = ['anger', 'anticipation', 'disgust', 'fear',
            'joy', 'negative', 'positive', 'sadness', 'surprise', 'trust']
    mainDict = {}
    with open(dictFile) as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            mainDict[row['Word']] = [int(row[i]) for i in cols]
    # print mainDict
    scoring(tweetFile,mainDict)

def scoring(tweetFile,mainDict):
    for line in tweetFile:
        tweet = json.loads(line)
        try:
            if tweet[u'lang'] != 'en':
                continue
            line = tweet[u'text'].replace('.','').replace(',','').replace(';','').replace(':','').replace('\t',' ').replace('\n',' ')
            words = line.split(' ')
            tweetScore = [0] * 10
            for word in words:
                if word in mainDict:
                    for i in range(len(tweetScore)):
                        tweetScore[i] += mainDict[word][i]
            print line
            print tweetScore
        except KeyError: # If tweet is empty, continue
            # print 'Error: no text'
            pass
        except:
            print 'Unexpected error'
            raise

if __name__ == '__main__':
    main()
