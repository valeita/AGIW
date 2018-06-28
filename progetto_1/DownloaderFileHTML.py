import json
import os
import grequests

#funzione per che esegue lo step 0 dell'homework
def processingJsonFile():

    data = json.load(open('dexter_3.json'))          #leggo il file, parsing e risultato in data

    if(os.path.isdir("/Users/valerio/Desktop/workspace pyCharm/homework_1/dexter_urls_category_camera") == True):
        os.chdir("dexter_urls_category_camera")                                             #essendo già presente mi ci sposto dentro
    else:
        os.makedirs("dexter_urls_category_camera")                                          #creo cartella categoria
        os.chdir("dexter_urls_category_camera")                                             #mi sposto al suo interno

    for domain in data:                                 #ciclo sui domini, quindi su tutte le chiavi dell'intero json

        print("processing domain: " + str(domain))
        i = 1                                           #contatore per nominare le cartelle

        os.makedirs(domain)                             #creo cartella col nome di domain e qui dentro scaricherò le pagine relative a questo dominio
        os.chdir(domain)                                #mi posiziono al suo interno
        indexFile = open("index.txt","w")               #creo il file locale index.txt

        requestData = (grequests.get(site) for site in data[domain])                 #richiesta http per scaricare dati di un url
        mapResponse = grequests.map(requestData, gtimeout=1000)

        for response in mapResponse:

            print("work in progress")

            if(response == None):
                indexFile.write(data[domain][i - 1] + "\t" + "network error" + "\n")

            elif(response.status_code == 200):

                indexFile.write(data[domain][i-1] + "\t" + str(i) + ".html\n")
                fileTmp = open(str(i) + ".html", "w")
                fileTmp.write(response.text)
                fileTmp.close()
            else:
                indexFile.write(data[domain][i-1] + "\t" + str(response.status_code) + "\n")

            i = i+1
        indexFile.close()
        os.chdir("..")

    return "SUCCESS"


processingJsonFile()






