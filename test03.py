import sys
import json
import stream
import csv

''' Creation of expandible word dictionary with frequency '''

def main():
    cols = ['anger', 'anticipation', 'disgust', 'fear',
        'joy', 'negative', 'positive', 'sadness', 'surprise', 'trust', 'freq']
    if len(sys.argv) != 3:
        print '''Usage:
        python test03.py <Dictionary CSV> <Tweeter stream json>'''
        sys.exit(0)

    dictFile  = sys.argv[1]
    tweetFile = open(sys.argv[2])
    mainDict = {}
    with open(dictFile) as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            mainDict[row['Word']] = [int(row[i]) for i in cols if i != 'freq']
        for word in mainDict:
            mainDict[word].append(1)
            # print word, mainDict[word]

    # print mainDict
    scoring(tweetFile,mainDict)
    # output('streamTest03.csv',mainDict)

def scoring(tweetFile,mainDict):
    cols = ['anger', 'anticipation', 'disgust', 'fear',
        'joy', 'negative', 'positive', 'sadness', 'surprise', 'trust', 'freq']

    for line in tweetFile:
        tweet = json.loads(line)
        try:
            if tweet[u'lang'] != 'en':
                continue
            line = tweet[u'text'].replace('.','').replace(',','').replace(';','').replace(':','').replace('\t',' ').replace('\n',' ')
            words = line.split(' ')
            tweetScore = [0.0] * 10
            csvline = {}
            oldFlreq = 0
            for word in words:
                if word in mainDict:
                    oldFlreq = mainDict[word][-1] # Save old frequency
                    for i in range(len(tweetScore)-1): ## Watch out for fequency: its in the same array
                        tweetScore[i] += float(mainDict[word][i])
                        csvline[cols[i]] = tweetScore[i] / oldFlreq ## normalize before adding
                    csvline[cols[-1]] = oldFlreq + 1 # Increase frequency by 1
            if not bool(csvline):
                continue
            ## TODO: add to dic.
            print csvline
        except KeyError: # If tweet is empty, continue
            continue
        except:
            print 'Unexpected error'
            raise

def output(outfile,mainDict):
    cols = ['word', 'anger', 'anticipation', 'disgust', 'fear',
        'joy', 'negative', 'positive', 'sadness', 'surprise', 'trust', 'freq']
    with open(outfile, 'w') as outf:
        writer = csv.DictWriter(outf,fieldnames=cols)
        writer.writeheader()
        for word in mainDict:
            rowlist = [word]+mainDict[word]
            row = {}
            for i in range(len(rowlist)):
                row[cols[i]] = rowlist[i]
            writer.writerow(row)

if __name__ == '__main__':
    main()
