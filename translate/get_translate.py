#!/usr/bin/python

import urllib2
import sys
import json


API_KEY = " "

def readHistory(fileName):
	with open(fileName,'r') as histFile:
		words = histFile.read().split()
	return words

def get_def(obj):
	return obj["def"]

def get_tr(obj):
	return obj["tr"]

def get_text(obj):
	return obj["text"]

def getWordTranslate(wrd):
	result = [] 
	yaDict = urllib2.urlopen("https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key="+API_KEY+"&lang=en-ru&text="+wrd)
	response = json.loads(yaDict.read())
	for defn in get_def(response):
		for translation in get_tr(defn):
			result.append(get_text(translation).encode('utf-8'))
	return result

def dumpWordResults(wordResults):
	with open("results.json",'w') as resultFile:
		json.dump(wordResults,resultFile)

def readWordResults():
	fileName = "results.json" 
	with open(fileName) as resultFile:
		return json.load(resultFile)

def makeWordResults(wordList):
	result = {}
	noTrans = [];
	for word in wordList:
		translation = getWordTranslate(word)
		if len(translation) != 0:
			result.update({word:{"right":0,"wrong":0}})
		else: 
			noTrans.append(word)
	return result,noTrans

def runTest(wordResults):
	for word in wordResults:
		print word
		usr_tr = raw_input("?")
		tr = getWordTranslate(word)
		if usr_tr in tr: 
			print "Right!",
			wordResults[word]["right"] += 1
		else:
			print "Wrong!",
			wordResults[word]["wrong"] += 1
			for t in tr: print t,
		print
		print "+("+str(wordResults[word]["right"])+")","-("+str(wordResults[word]["wrong"])+")"
 	return wordResults
	

if sys.argv[1] == "nd":
	results,hasNoTrans = makeWordResults(readHistory(sys.argv[2]))
	dumpWordResults(results)
	print "Has no translation:", hasNoTrans
elif sys.argv[1] == "tst":
	testResult = runTest(readWordResults())
	print "Completed, saving results!"
	dumpWordResults(testResult)

	




	
	
