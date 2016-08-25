import sys
import json
import stream
import csv

''' Extraction of twitter scores from file to csv '''

cols = ['anger', 'anticipation', 'disgust', 'fear',
        'joy', 'negative', 'positive', 'sadness', 'surprise', 'trust', 'freq']

def main():
    global cols
    if len(sys.argv) != 3:
        print '''Usage:
        python test02.py <Dictionary CSV> <Tweeter stream json>'''
        sys.exit(0)

    dictFile  = sys.argv[1]
    tweetFile = open(sys.argv[2])
    with open(dictFile) as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            mainDict[row['Word']] = [int(row[i]) for i in cols]
    # print mainDict
    scoring(tweetFile,mainDict)

def scoring(tweetFile,mainDict):
    global cols

    outf = open('streamTest02.csv', 'w')
    writer = csv.DictWriter(outf, fieldnames=cols)
    writer.writeheader()
    for line in tweetFile:
        tweet = json.loads(line)
        try:
            if tweet[u'lang'] != 'en':
                continue
            line = tweet[u'text'].replace('.','').replace(',','').replace(';','').replace(':','').replace('\t',' ').replace('\n',' ')
            words = line.split(' ')
            tweetScore = [0] * 10
            csvline = {}
            for word in words:
                if word in mainDict:
                    for i in range(len(tweetScore)):
                        tweetScore[i] += mainDict[word][i]
                        csvline[cols[i]] = tweetScore[i]
            if not bool(csvline):
                continue
            writer.writerow(csvline)

        except KeyError: # If tweet is empty, continue
            continue
        except:
            print 'Unexpected error'
            raise

if __name__ == '__main__':
    main()
