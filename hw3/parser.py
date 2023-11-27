from bs4 import BeautifulSoup
import pymongo
import re

def getDict(source, target):
    return source.find_one({'url':target})

def getFacultyTags(html):
    bs = BeautifulSoup(html, 'html.parser')
    return bs.find_all('div', {'class':'clearfix'})
    
def storeInfo(html, dest):
    name = html.find('h2')
    if name is None:
        return
    
    name = name.get_text()
    info = getInfo(html)
    info['name'] = name
    print(info)

    dest.insert_one(info)

def getInfo(html):
    infoHtml = html.find('p')
    result = {}

    fields = infoHtml.find_all('strong')
    #print([field.next_sibling for field in fields])
    #0 is title
    result['title'] = fields[0].next_sibling.replace(':', '')
    #print(title)
    #1 is office
    result['office'] = fields[1].next_sibling.replace(':', '')
    #print(office)
    #2 is phone, which was not asked for

    fields = infoHtml.find_all('a')
    #print([field.get_text() for field in fields])
    #0 is email
    result['email'] = fields[0].get_text()
    #print(email)
    #1 is website
    result['website'] = fields[1].get_text()
    #print(website)

    return result


def main():
    target = 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml'

    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.corpus
    pages = db.pages
    professors = db.professors
    
    html = getDict(pages, target)['html']
    profs = getFacultyTags(html)

    print('\n')
    for prof in profs:
        storeInfo(prof, professors)

if __name__ == '__main__':
    main()