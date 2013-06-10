from bs4 import BeautifulSoup
import urllib
import re
import os
import time
import HTMLParser

def extractTags(url):

    page = urllib.urlopen(url)
    soup = BeautifulSoup(page)

    for link in soup.find_all('a'):

        refType = str(link.get('href'))
    
        if refType.startswith('/tag/'):

            tagName = refType[5:].lower()
            tagName = urllib.unquote(tagName).replace('+',' ').replace('-', ' ')
            tagInfo.write(tagName + ',')
            #print(tagName)

            countSpan = link.find_next("span")
            #print(countSpan)
                                       
            if hasattr(countSpan, 'contents'):

                count = re.search('\d+', str(countSpan.contents))
                tagCount = count.group(0)
            
                #print(count)
            
            else:
                tagCount = '?'

            tagInfo.write('{0},'.format(tagCount))


tagDirectory = os.path.join(os.pardir, 'tag_data')
tagInfo = open(os.path.join(tagDirectory, 'tag_data.csv'), 'w')

titlesDirectory = os.path.join(os.pardir, 'book_titles')
for file in os.listdir(titlesDirectory):
    
    for line in open(os.path.join(titlesDirectory, file), 'r'):

        time.sleep(1)

        indexOfLastBy = line.rfind("by")
        title = line[0:indexOfLastBy].strip()
        author = line[indexOfLastBy + 2:].strip()

        tagInfo.write('{0},{1},'.format(title, author))

        url = 'http://www.librarything.com/title/' + title
        print(url)

        extractTags(url)

        tagInfo.write("\n")


tagInfo.close()
    
    
