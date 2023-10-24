#-------------------------------------------------------------------------
# AUTHOR: your name
# FILENAME: title of the source file
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #1
# TIME SPENT: how long it took you to complete the assignment
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# --> add your Python code here
import psycopg2
from psycopg2.extras import RealDictCursor

import re

def connectDataBase():

    # Create a database connection object using psycopg2
    # --> add your Python code here
    #TODO: DATABASE CONNECTION
    DB_NAME = 'corpus'
    DB_USER = 'postgres'
    DB_PASS = 'aj100500'
    DB_HOST = 'localhost'
    DB_PORT = '5432'

    try:
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT,
                                cursor_factory=RealDictCursor)
        return conn
    except:
        print("database connection unsuccessful")

def createTables(cur, conn):
    try:
        catTableCreate = '''CREATE TABLE categories
                          (id INTEGER PRIMARY KEY,
                           name CHARACTER VARYING NOT NULL)'''
        cur.execute(catTableCreate)

        docTableCreate = '''CREATE TABLE documents 
                          (id INTEGER PRIMARY KEY, 
                           category_id INTEGER REFERENCES categories(id),
                           text CHARACTER VARYING NOT NULL, 
                           title CHARACTER VARYING NOT NULL, 
                           length INTEGER NOT NULL, 
                           date DATE NOT NULL)'''
        cur.execute(docTableCreate)

        termTableCreate = '''CREATE TABLE terms 
                           (term CHARACTER VARYING PRIMARY KEY, 
                            length INTEGER NOT NULL, 
                            date DATE)'''
        cur.execute(termTableCreate)

        indexCreate = '''CREATE TABLE index 
                       (document_id INTEGER REFERENCES documents(id) NOT NULL, 
                        term CHARACTER VARYING REFERENCES terms(term) NOT NULL, 
                        count INTEGER NOT NULL)'''
        cur.execute(indexCreate)

        conn.commit()

    except Exception as e: 
        #print(e)
        conn.rollback()
        print("There was a problem during database creation or the database has already been created")

def createCategory(cur, catId, catName):

    # Insert a category in the database
    sql = "INSERT INTO categories (id, name) VALUES (%s, %s)"

    recset = [catId, catName]
    cur.execute(sql, recset)

def createDocument(cur, docId, docText, docTitle, docDate, docCat):

    # 1 Get the category id based on the informed category name
    catIdQuery = "SELECT id FROM categories WHERE name like %(name)s"
    cur.execute(catIdQuery, {'name':docCat})
    catId = cur.fetchall()[0]['id']

    # 2 Insert the document in the database. For num_chars, discard the spaces and punctuation marks.
    # --> add your Python code here
    docInsertQuery = "INSERT INTO documents (id, text, title, length, date, category_id) VALUES (%s, %s, %s, %s, %s, %s)"
    num_chars = len(re.sub(r'[\s\W]+', '', docText)) #remove whitespace and non alphanumeric chars, then take the lengh of the remaining string
    docset = [docId, docText, docTitle, num_chars, docDate, catId]
    cur.execute(docInsertQuery, docset)

    # 3 Update the potential new terms.
    # 3.1 Find all terms that belong to the document. Use space " " as the delimiter character for terms and Remember to lowercase terms and remove punctuation marks.
    terms = re.findall(r'[\w]+', docText.lower()) #lowercase, then split on non alphanumerics
    print(terms)

    # 3.2 For each term identified, check if the term already exists in the database
    termQuery = "SELECT * FROM terms WHERE term = %(term)s"
    termInsertQuery = "INSERT INTO terms (term, length, date) VALUES (%s, %s, %s)"
    for term in terms:
        cur.execute(termQuery, {'term':term})
        # 3.3 In case the term does not exist, insert it into the database
        if (not cur.fetchall()):
            termset = [term, len(term), docDate]
            cur.execute(termInsertQuery, termset)

    # 4 Update the index
    # 4.1 Find all terms that belong to the document
    # 4.2 Create a data structure the stores how many times (count) each term appears in the document
    termcount = {}
    for term in terms:
        if term in termcount:
            termcount[term] += 1
        else:
            termcount[term] = 1
    # 4.3 Insert the term and its corresponding count into the database
    indexQuery = "INSERT INTO index (document_id, term, count) VALUES (%s, %s, %s)"
    for term in termcount.keys():
        indexset = [docId, term, termcount[term]]
        cur.execute(indexQuery, indexset)


def deleteDocument(cur, docId):

    # 1 Query the index based on the document to identify terms
    termQuery = 'SELECT term FROM index WHERE document_id = %(id)s'
    cur.execute(termQuery, {'id':docId})
    termSet = cur.fetchall()

    # 1.1 For each term identified, delete its occurrences in the index for that document
    deleteIndexQuery = 'DELETE FROM index WHERE document_id = %(id)s'
    cur.execute(deleteIndexQuery, {'id':docId})

    # 1.2 Check if there are no more occurrences of the term in another document. If this happens, delete the term from the database.
    checkIndexQuery = 'SELECT document_id FROM index WHERE term = %(term)s'
    deleteTermQuery = 'DELETE FROM terms WHERE term = %(term)s'
    for term in termSet:
        cur.execute(checkIndexQuery, {'term':term['term']}) #this line of code makes me angry
        indices = cur.fetchall()

        if (not indices):
            cur.execute(deleteTermQuery, {'term':term['term']})


    # 2 Delete the document from the database
    deleteQuery = 'DELETE FROM documents WHERE id = %(id)s'
    cur.execute(deleteQuery, {'id':docId})

def updateDocument(cur, docId, docText, docTitle, docDate, docCat):

    # 1 Delete the document
    deleteDocument(cur, docId)

    # 2 Create the document with the same id
    createDocument(cur, docId, docText, docTitle, docDate, docCat)

def getIndex(cur):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    sql = 'SELECT documents.title, index.term, index.count FROM documents INNER JOIN index ON documents.id = index.document_id'
    cur.execute(sql)
    recset = cur.fetchall()
    queryReturn = {}
    for rec in recset:
        if rec['term'] not in queryReturn:
            queryReturn[rec['term']] = {}

        queryReturn[rec['term']][rec['title']] = rec['count']

    return queryReturn