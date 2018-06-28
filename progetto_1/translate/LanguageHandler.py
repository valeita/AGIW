from bs4 import BeautifulSoup
import os
import langdetect
from langdetect import detect
import NLTKDetector

INPUT_PATH = '/home/emanuele/Scrivania/hw1_AGIW/dexter_urls_category_camera'
INPUT_PATH_PROVE = '/home/emanuele/Scrivania/INPUT'

def languageDetector():
    try:
        os.chdir(INPUT_PATH)
    except:
        print('Error in INPUT_PATH, set della variabile errato')
        exit(1)

    if (os.path.exists('languages.txt')):
        os.remove('languages.txt')
    os.mknod('languages.txt')

    languages = []
    for domainDir in os.listdir('.'):
        print(domainDir)
        if(domainDir != 'languages.txt'):
            os.chdir(os.path.join(INPUT_PATH, domainDir))
            if(os.path.exists('lang.txt')):     #indice file-lingua
                os.remove('lang.txt')
            os.mknod('lang.txt')
            langindex = open('lang.txt', 'w')
            for site in os.listdir('.'):
                if (site != 'index.txt' and site != 'lang.txt'):
                    attrlang = readLang(site)
                    if(attrlang != None):
                        lang = attrlang
                    else:
                        textData = readData(site)
                        toDetect = extractLongerStr(textData)
                        print(toDetect)
                        if(toDetect == '' or toDetect == None):
                            print("non è stato prelevato nulla")
                            lang = 'none'
                        else:
                            try:
                                #lang = NLTKDetector.detect_language(toDetect)       #Rilevazione della lingua con NLTK
                                lang = detect(toDetect)                            #Rilevazione della lingua con langdetect
                            except:
                                print('Eccezione durante la rilevazione della lingua')
                                lang = 'none'
                    print(site + ' ' + lang)
                    lang = processLang(lang)
                    langindex.write(site + ' ' + lang + '\n')
                    if(not(lang in languages) and lang != 'none'):
                        languages.append(lang)
            langindex.close()
    print('\n')
    os.chdir('..')
    langrecap = open('languages.txt', 'w')
    for lng in languages:
        langrecap.write(lng + '\n')
        print(lng)
        print('\n')
    langrecap.write('totale:' + str(len(languages)) + '\n')
    langrecap.close()
    print(len(languages))
    return len(languages)




def readLang(site):
    htmlFile = open(site, 'r')
    soup = BeautifulSoup(htmlFile, 'html.parser')
    lang = None
    try:
        html = soup.find('html')
        lang = html['lang']
    except:
        print("Il tag html non contiene l'attributo lang")

    if(lang == None or lang == ''):
        try:
            metaTags = BeautifulSoup.find_all('html')
            for meta in metaTags:
                try:
                    lang = meta['lang']
                except:
                    continue
        except:
            print('Nessun tag meta contenente lang')

    if(lang == None or lang == ''):
        return None
    else:
        return lang




def readData(site):

    fileSite = open(site, 'r')
    htmlSite = fileSite.read()
    soup = BeautifulSoup(htmlSite, 'html.parser')
    [s.extract() for s in soup('script')]
    [s.extract() for s in soup('style')]

    textReturned = soup.get_text()
    fileSite.close()

    return textReturned


def extractLongerStr(textData):
    textDataParsed = textData.replace('\n\n\n', '*')
    textDataParsed = textDataParsed.replace('\n\n', '*')
    textElem = textDataParsed.split('*')
    countmax = 0
    longerStr = ''

    for elem in textElem:
        #print(elem)
        length = len(elem.split())
        #print('LUNGHEZZA: ')
        #print(length)
        #print('\n')
        if(length > countmax ):
            countmax = length
            longerStr = elem

    return longerStr




def processLang(lang):
    if(lang.startswith('en')):
        return 'en'
    elif(lang.startswith('es')):
        return 'es'
    else:
        return lang




if __name__=='__main__':
    languageDetector()