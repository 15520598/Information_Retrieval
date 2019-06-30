import os
import re
import sys
import math
import string
import operator

def PrintData(data):
	if type(data) is dict:
		for key, value in data.items():
			if type(value) is dict:
				print(key, ":")
				for subKey, subValue in value.items():
					print("\t", subKey.ljust(15), ":", subValue)
			elif type(value) is list:
				print(key, ":")
				if value != [] and type(value[0]) is list:
					for subValue in value:
						print("\t", subValue)
				else:
					print("\t", value)
			else:
				print(str(key).ljust(20), ":\t", value)
	elif type(data) is list:
		for value in data:
			print(value)
	else:
		print(data)

def textPreprocessing(string):
	listTerm = []
	string = string.lower()
	string = re.compile('\W+|\d+').sub(' ', string)
	listTerm = string.split()
	return listTerm

def DocumentParser(Path):
	dict_DocumentName = {}
	dict_Document = {}
	idDocument = 1
	for fileName in os.listdir(Path):
		f = open(os.path.join(Path, fileName), 'r')
		string = f.read()
		dict_DocumentName['Document {:0>4}'.format(str(idDocument))] = os.path.join(os.getcwd(), Path, fileName)
		dict_Document['Document {:0>4}'.format(str(idDocument))] = textPreprocessing(string)
		idDocument += 1
		f.close()
	return dict_DocumentName, dict_Document

def QueryParser(Path):
	dict_Query = {}
	idQuery = 1
	with open(Path) as f:
		for string in f:
			dict_Query['Query {:0>3}'.format(str(idQuery))] = textPreprocessing(string)
			idQuery += 1
	return dict_Query

def CreateListTerm(dict_Document):
	list_Term = []
	for nameDocument in dict_Document:
		list_Term.extend(dict_Document[nameDocument])
	list_Term = list(set(list_Term))
	list_Term.sort()
	return list_Term

def CreateDictTermFrequency(list_Term, dict_Document):
	dict_TermFreq = {}
	for term in list_Term:
		dict_TermFreq[term] = {}	
	for key, document in dict_Document.items():
		list_Term = list(set(document))
		for term in list_Term:
			freq = document.count(term)
			dict_TermFreq[term][key] = freq
	return dict_TermFreq

def CreateDictTermDocumentCount(list_Term, dict_Document):
	dict_DocumentSet = {}
	dict_TermDocFreq = {}
	for term in list_Term:
		dict_TermDocFreq[term] = 0
	for key, document in dict_Document.items():
		dict_DocumentSet[key] = {}
		list_Term = list(set(document))
		list_Term.sort()
		for term in list_Term:
			freq = document.count(term)
			dict_DocumentSet[key][term] = freq
			dict_TermDocFreq[term] += 1 
	return dict_DocumentSet, dict_TermDocFreq

def CreateDictDocumentLengthAndAVG(dict_Document):
	dict_DocLength = {}
	avgDocLength = 0
	for key, document in dict_Document.items():
		docLength = len(document)
		dict_DocLength[key] = docLength
		avgDocLength += docLength
	avgDocLength /= len(dict_Document)
	return avgDocLength, dict_DocLength

def CreateDictIDFTerm(list_Term, dict_Document):
	dict_IDF = {}
	renumber = 0.0
	docCount = len(dict_Document)
	dictTermDocumentCount = CreateDictTermDocumentCount(list_Term, dict_Document)[1]
	for term in list_Term:
		docFreq = dictTermDocumentCount[term]
		IDF = math.log(renumber + (docCount - docFreq + 0.5) / (docFreq + 0.5))
		if IDF >= 0.5:
			dict_IDF[term] = IDF
	return dict_IDF

def CreateDictTFTermDocument(list_Term, dict_Document):
	k = 1.2
	b = 0.75
	dict_TF = {}
	avgDocLength, dictDocLength = CreateDictDocumentLengthAndAVG(dict_Document)
	dictTermFrequency = CreateDictTermFrequency(list_Term, dict_Document)
	for term in list_Term:
		dict_TF[term] = {}
	for nameDoc, document in dict_Document.items():
		list_Term = list(set(document))
		for term in list_Term:
			freq = dictTermFrequency[term][nameDoc]
			L = dictDocLength[nameDoc]/avgDocLength
			TF = ((k+1.0)*freq)/(k*(1.0-b+b*L)+freq)
			dict_TF[term][nameDoc] = TF 
	return dict_TF

def CreateDictScoreBM25(list_Term, dict_Document):
	dict_ScoreBM25 = {}
	dict_IDF = CreateDictIDFTerm(list_Term, dict_Document)
	dict_TF = CreateDictTFTermDocument(list_Term, dict_Document)
	for term in dict_TF.keys():
		dict_ScoreBM25[term] = {}
		for idDocument in dict_TF[term].keys():
			if term in dict_IDF.keys():
				IDF = dict_IDF[term]
			else:
				continue
			TF = dict_TF[term][idDocument]
			scoreBM25 = IDF * TF
			dict_ScoreBM25[term][idDocument] = scoreBM25
	return dict_ScoreBM25

def CreateDictRank(dict_Query, dict_Document, dict_ScoreBM25):	
	rank = {}
	for idQuery, query in dict_Query.items():
		l = []
		for idDocument, document in dict_Document.items():
			score_document = 0
			for term in query:
				if term in dict_ScoreBM25.keys():
					if idDocument in dict_ScoreBM25[term].keys():
						score_document += dict_ScoreBM25[term][idDocument]
			if score_document > len(query)*0.20:
				l.append([idDocument, score_document])
		l.sort(key = operator.itemgetter(1), reverse = True)
		rank[idQuery] = l
	return rank

def WriteFile(dictRank, dictDocumentName):
	os.makedirs("Results/", exist_ok=True)
	for idQuery, ranks in dictRank.items():
		file = open("Results/" + str(int(idQuery.split()[1])) + ".txt", "w")
		for idDocument, score in ranks:
			nameDocument = os.path.basename(dictDocumentName[idDocument])
			nameDocument = nameDocument[:-4]
			file.write(nameDocument + "\n");
			# file.write(nameDocument + '\t' + str(score) + "\n");
		file.close()


def main(src1, src2):
	dictDocumentName, dictDocument = DocumentParser(src1)
	dictQuery = QueryParser(src2)
	listTerm = CreateListTerm(dictDocument)
	dictScoreBM25 = CreateDictScoreBM25(listTerm, dictDocument)
	dictRank = CreateDictRank(dictQuery, dictDocument, dictScoreBM25)
	WriteFile(dictRank, dictDocumentName)

if __name__ == '__main__':
	src1 = sys.argv[1]
	src2 = sys.argv[2]
	main(src1, src2)