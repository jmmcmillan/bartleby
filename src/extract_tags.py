from bs4 import BeautifulSoup
import urllib
import re
import os
import time
import HTMLParser

def extractTags(url):

    #orginal URL
    page = urllib.urlopen(url)
    actualURL = page.geturl()

    #get item ID from redirected URL
    indexOfLastSlash = actualURL.rfind("/")
    workID = actualURL[indexOfLastSlash + 1:]

    #get page with all tags
    URLtoTags = 'http://www.librarything.com/ajaxinc_showbooktags.php?work={0}&all=1&print=1&doit=1'.format(workID)
    tagPage = urllib.urlopen(URLtoTags)

    print(URLtoTags)
    
    soup = BeautifulSoup(tagPage)

    for link in soup.find_all('a'):

        refType = str(link.get('href'))
    
        if refType.startswith('/tag/'):

            tagCount = 0
            countSpan = link.find_next("span")
            #print(countSpan)
                                       
            if hasattr(countSpan, 'contents'):

                count = re.search('\d+', str(countSpan.contents))
                tagCount = count.group(0)
            
                #print(tagCount)
            
            else:
                tagCount = '?'


            if (int(tagCount) > 1):

                tagName = refType[5:].lower()
                tagName = urllib.unquote(tagName).replace('+',' ').replace('-', ' ')
                #print(tagName)
            
                tagInfo.write(tagName + ',')
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
    
    
