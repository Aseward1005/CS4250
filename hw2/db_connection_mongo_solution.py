#-------------------------------------------------------------------------
# AUTHOR: your name
# FILENAME: title of the source file
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #2
# TIME SPENT: how long it took you to complete the assignment
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# --> add your Python code here
import pymongo
import re

def connectDataBase():
    # Create a database connection object using pymongo
    # --> add your Python code here
    client = pymongo.MongoClient(host='localhost', port=27017)
    return client.corpus

def createDocument(col, docId, docText, docTitle, docDate, docCat):

    # create a dictionary to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.
    # --> add your Python code here
    terms = re.findall(r'[\w]+', docText.lower()) #lowercase, then split on non alphanumerics
    termdict = {}
    for term in terms:
        if term not in termdict:
            termdict[term] = 0
    
        termdict[term] += 1


    # create a list of dictionaries to include term objects.
    # --> add your Python code here
    termlist = []
    for term in termdict.keys():
        termlist.append({'term':term, 'num_chars': len(term), 'count': termdict[term]})
    

    #Producing a final document as a dictionary including all the required document fields
    # --> add your Python code here
    doc = {
        '_id': docId,
        'text': docText,
        'title': docTitle,
        'num_chars': len(re.sub(r'[\s\W]+', '', docText)),
        'date': docDate,
        'category' : docCat,
        'terms' : termlist
        }

    # Insert the document
    # --> add your Python code here
    return col.insert_one(doc)

def deleteDocument(col, docId):

    # Delete the document from the database
    # --> add your Python code here
    col.delete_one({'_id': docId})

def updateDocument(col, docId, docText, docTitle, docDate, docCat):

    # Delete the document
    # --> add your Python code here
    deleteDocument(col, docId)

    # Create the document with the same id
    # --> add your Python code here
    return createDocument(col, docId, docText, docTitle, docDate, docCat)

def getIndex(col):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here
    docs = col.find()

    index = {}
    for doc in docs:
        for termdict in doc['terms']:
            if termdict['term'] not in index:
                index[termdict['term']] = {}

            index[termdict['term']][doc['title']] = termdict['count'] 

    return index