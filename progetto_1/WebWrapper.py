import json
from bs4 import BeautifulSoup
import os
import re
import operator

keyList = ['temperature','megapixel','output','voltage','storage','humidity','light','exposure','LCD','touchscreen','raw'
           'flash','display','timer', 'screen','battery','recording','voice','microphone','resizing','focus','reflex',
           'rotating','memory','speed','aperture','range','hdmi','resolution','ratio','connectivity','power','auto','zoom',
           'jpeg','height','weight','hd','iso','1280','interface','port','video','audio','connectivity','size','usb',
           '1024','2560','1920','768','4032','3024']

keyMap = {}

OUTPUT_PATH = '/Users/valerio/Desktop/output'                      #cartella dove voglio tutto il mio output
INPUT_PATH = '/Users/valerio/Desktop/dexter_urls_category_camera'  #cartella dove ci sono le cartelle e pagine scaricate allo step 0



def wrapper():

    try:
        os.chdir(INPUT_PATH)
    except:
        print('Error in INPUT_PATH, set della variabile errato')
        exit(1)

    for domainDir in os.listdir('.'):

        if(os.path.isdir(domainDir) and not(checkInCache(domainDir))):

            print('extraction data from ' + domainDir + ' ... ')
            os.chdir(OUTPUT_PATH)
            os.makedirs(domainDir)
            os.chdir(os.path.join(INPUT_PATH,domainDir))

            for site in os.listdir('.'):

                if(site != 'index.txt' and site != '.DS_Store'):

                    print('processing ' + site)
                    textData = readData(site)

                    if(checkErrorOrHtmlEmpty(textData)):
                        createJSON('','',site,domainDir)
                    else:
                        totalDistribution = {}
                        allText = list()
                        extractData(textData,totalDistribution,allText)
                        spec = evaluete(totalDistribution)
                        createJSON(allText,spec,site,domainDir)

            os.chdir('..')
        else:
            print(domainDir + ': ... skipped')


    return "SUCCESS"




#controllo se la cartella in output è già presente, in tal caso è già stato processato quel dominio.
#il programma si impalla? ricomincia da dove sei arrivato
def checkInCache(domainDir):

    if(os.path.isdir(os.path.join(OUTPUT_PATH,domainDir))):
        return True
    return False









#utilizzo la libreria di beautifulSoup per prendere tutti i testi della mia pagina
def readData(site):

    fileSite = open(site, "r")
    htmlSite = fileSite.read()
    soup = BeautifulSoup(htmlSite, 'html.parser')

    for script in soup(["script", "style"]):
        script.extract()

    html = soup.prettify()

    betterSoup = BeautifulSoup(html, 'html.parser')
    textReturned = betterSoup.get_text()
    print(textReturned)
    fileSite.close()

    return textReturned




#faccio un parsing mio su tutti i testi, separandoli tutti da uno o piu *
def extractData(textData,totalDistribution, allText):

    textElem = prepareData(textData, allText)

    for elem in textElem:

        if(not stopWordsPresence(elem)):
            calculateDistribution(elem,totalDistribution)






def prepareData(textData, allText):

    lines = textData.split("\n")
    listText = list()
    listIndex = list()

    j=0

    for elem in lines:

        if(len(elem)>0 and not presenceStringOnlyBlankSpace(elem)):

            allText.append(elem)
            c=0

            for char in elem:

                if(char == " "):
                    c=c+1
                else:
                    break

            if(len(listIndex) == 0 and len(listText) == 0):

                listText.append(elem)
                listIndex.append(c)
                j=j+1
            else:
                backCont = listIndex[j-1]
                if(c >= backCont-1 and c<= backCont+1):
                    listText[j-1] = listText[j-1] + elem
                    listIndex[j-1]=c
                else:
                    listText.append(elem)
                    listIndex.append(c)
                    j = j+1

    return listText



def presenceStringOnlyBlankSpace(s):

    for i in range(len(s)):

        if(s[i] != ' '):

            return False
    return True






#mi calcolo per ogni frammento di testo, la distribuzione di tutte le parole chiavi
#al suo interno. il punteggio che ogni parola chiave assegna a quel testo diminuisce con
#il ripetersi di tale parola
def calculateDistribution(text,totalDistribution):

    textLow = text.lower()
    keyMapCopy = keyMap.copy()
    distribution = 0

    for key in keyMapCopy.keys():

        c = 0
        occurranceArray = [m.start() for m in re.finditer(key, textLow)]

        for elem in occurranceArray:

            c = c + 1

        while (c>0):

            distribution = distribution + keyMapCopy[key]
            keyMapCopy[key] = keyMapCopy[key]-1
            c = c-1

    text = text.replace(u'\xa0', u' ')
    totalDistribution[text]=distribution




#valuto tutte le distribuzioni dei testi. prendo quella maggiore e solo se è >=9
def evaluete(totalDistributionsSite):

    if(len(totalDistributionsSite)>0):
        sorted_x = sorted(totalDistributionsSite.items(), key=operator.itemgetter(1))
        [spec,distributionValue] = sorted_x[len(sorted_x)-1]
    else:
        return ''

    if(distributionValue>=12):
        return spec
    return ''




#creo json con le specifiche
def createJSON(allText,spec,site,domainDir):

    os.chdir(os.path.join(OUTPUT_PATH,domainDir))

    keyValueMap = extractKeyValue(allText,spec)

    nameSite=site.split('.')

    with open(nameSite[0] + '.json', 'w') as f:
        json.dump(keyValueMap, f)

    os.chdir(os.path.join(INPUT_PATH, domainDir))






def extractKeyValue(allText,spec):

    keyValueMap = dict()

    if(len(spec)>0):
        i=0
        start=0
        final=0

        while i < (len(allText)-2):

            tmpString = allText[i] + allText[i+1] + allText[i+2]

            if(len(tmpString)<len(spec)):

                if(equalInitialPart(tmpString, spec)):
                    start = i

                elif(equalFinalPart(tmpString, spec)):
                    final = i+2

            i += 1


        while(start<final):

            keyValueMap[allText[start].strip()] = allText[start+1].strip()
            start = start + 2


    return keyValueMap





#verifica la presenza di stopwords, che faranno si che tale frammento di testo, venga ignorato a prescindere
def stopWordsPresence(text):

    stopwords = ['help & faq','facebook','twitter','instagram','pinterest','terms & conditions','contact us']
    textLow = text.lower()

    for elem in stopwords:

        occurranceArray = textLow.find(elem)
        if(occurranceArray != -1): return True

    return False




#controllo se html vuoto o pagina di errore
def checkErrorOrHtmlEmpty(textSite):

    occurranceArray = [m.start() for m in re.finditer('sorry', textSite.lower())]
    if(len(textSite) <= 0 or len(occurranceArray)>0):
        return True

    return False



#creo una mappa parole_chiavi:3
def buildMap():

    for elem in keyList:
        keyMap[elem] = 3
    return keyMap





def equalInitialPart(stringShort, stringLong):

    i=0
    for char in stringShort:

        if(char != stringLong[i]):
            return False
        i +=1

    return True




def equalFinalPart(stringShort, stringLong):

    i=0
    for char in stringShort:

        if(stringShort[len(stringShort)-1-i] != stringLong[len(stringLong)-1-i]):
            return False
        i +=1

    return True



def main():

    buildMap()
    wrapper()





if __name__ == '__main__' :
	main()