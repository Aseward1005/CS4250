#-------------------------------------------------------------------------
# AUTHOR: your name
# FILENAME: title of the source file
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #1
# TIME SPENT: how long it took you to complete the assignment
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard arrays

#importing some Python libraries
import csv
import math

documents = []
labels = []

#reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append(row[0])
            labels.append(row[1])

#Conduct stopword removal.
#--> add your Python code here
stopWords = {'I', 'and', 'She', 'They', 'her', 'their'}

noStopDoc = [document for document in documents]
for stopWord in stopWords:
    noStopDoc = [document.replace(stopWord, '') for document in noStopDoc]

#print(noStopDoc)

#Conduct stemming.
#--> add your Python code here
stemming = {
  "cats": "cat",
  "dogs": "dog",
  "loves": "love",
}

stemDoc = [doc for doc in noStopDoc]
for stemKey in stemming.keys():
    stemDoc = [document.replace(stemKey, stemming[stemKey]) for document in stemDoc]

#print(stemDoc)

#Identify the index terms.
#--> add your Python code here
longsentence = ' '.join(stemDoc)
#print(longsentence)
terms = list(set(longsentence.split()))
#print(terms)

#Build the tf-idf term weights matrix.
#--> add your Python code here
tokenDocs = [doc.split() for doc in stemDoc]
#count the amount of each term and store it in a dictionary
tokenDicts = [{term : 0 for term in terms} for doc in tokenDocs]
for i, tokenDict in enumerate(tokenDicts):
    for token in tokenDocs[i]:
        tokenDict[token] += 1

#print(tokenDicts)
#use tokenDicts to calculate tf
tfs = [tokens for tokens in tokenDicts]
for tf in tfs:
    numTerms = sum(tf.values())
    for key in tf.keys():
        tf[key] = tf[key] / numTerms

#print(tfs)

D = len(documents)
#print(D)

#use tokenDicts to calculate df
dfs = {term:0 for term in terms}
for tokenDict in tokenDicts:
    for key in tokenDict.keys():
        if tokenDict[key] > 0:
            dfs[key] += 1

#print(dfs)

idf = {term:math.log10(D/dfs[term]) for term in terms}

#print(idf)

docMatrix = [{term:tf[term]*idf[term] for term in terms} for tf in tfs]
#print(docMatrix)

#Calculate the document scores (ranking) using document weigths (tf-idf) calculated before and query weights (binary - have or not the term).
#--> add your Python code here
query = "cats and dogs"

#stopword removal
for stopword in stopWords:
    query = query.replace(stopword, '')

#stemming
for stemkey in stemming.keys():
    query = query.replace(stemkey, stemming[stemkey])

#tokenization
queryTerms = list(set(query.split()))
#print(queryTerms)

#scoring
#iterate through documents
#add tf-idf schores of terms in queryterms
docScores = [sum([doc[term] for term in queryTerms]) for doc in docMatrix]
#print(docScores)

#Calculate and print the precision and recall of the model by considering that the search engine will return all documents with scores >= 0.1.
#--> add your Python code here
#precision = correct guesses (correct)/total guesses(yes)
#recall = correct guesses/total relevant(rel)
correct = 0
yes = 0
rel = 0
for score, label in zip(docScores, labels):
    g = False

    if (score >= 0.1): #guessing relevant
        yes += 1
        g = True

    if ('R' in label):
        rel += 1
        if g:
            correct += 1
#print(labels)

print(f'Precision: {correct/yes * 100}')
print(f'Recall: {correct/rel * 100}')