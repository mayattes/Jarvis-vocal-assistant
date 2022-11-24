import os
import pyttsx3
import datetime
import speech_recognition as sr
import pyaudio
import wikipedia  
import smtplib
import webbrowser as wb
import pyautogui
import psutil

# création de l'audio
def parler(audio):
    av = pyttsx3.init()
    av.say(audio)
    av.runAndWait()
    voices = av.getProperty('voices')
    av.setProperty('voice', voices[1].id) #voix françaises

# fonction pour l'heure
def heure():
    h = datetime.datetime.now().strftime('%H:%M:%S')
    parler("l'heure exacte est:")
    parler(h)

# date du jour
def date():
    annee = str(datetime.datetime.now().year)
    mois = str(datetime.datetime.now().month)
    jour = str(datetime.datetime.now().day)
    parler("la date du jour est: ")
    parler(jour)
    parler(mois)
    parler(annee) 


# Créer la fonction de salutation
def salutation():
    parler("Bienvenue ") 
    h = datetime.datetime.now().hour
    if h>=6 and h<12:
        parler("Bonjour ")
    elif h>=12 and h<18:
        parler("Bonne après-midi ")
    else: 
        parler("Bonsoir ")
    parler("Je suis à votre service, comment puis-je vous aider ?")

# reconnaissance vocale 
def commande():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Je vous écoute...")
        r.pause_threshold=1
        audio = r.listen(source)
    try:
        print("En ecoute....")
        requete = r.recognize_google(audio,language='fr-FR')
        print(requete)
    except Exception as e:
        print(e)
        parler("S'il vous plaît répéter votre commande ...")
        return 'None'
    return requete


# envoi d'email
def envoi_email(cible, contenu):
    serveur = smtplib.SMTP("smtp@gmail.com", 587)
    serveur.ehlo()
    serveur.starttls()
    serveur.login("sydneykoita7@gmail.com", "mot de passe")
    serveur.sendmail("sydneykoita7@gmail.com", cible, contenu)
    serveur.close()

# capture écran
def capture():
    image = pyautogui.screenshot()
    image.save('//Users//koumbakoita//Desktop//bureau//koumba//IA//assistantVocal//cap.png')

# Processeur et batterie
def infoOrddi():
    nivProc = str(psutil.cpu_percent())
    parler(nivProc + ('pourcent utilisé par le processeur'))
    nivBat = str(psutil.sensors_battery().percent)
    parler(nivBat + " pourcent de batterie")

if __name__=="__main__":
    salutation()
    while True:
        req = commande().lower()
        if "heure" in req:
            heure()
        elif "date" in req:
            date()
        elif "fermer " in req:
            quit()
        #elif "quitter " in req:
        #    quit()
        #elif "au revoir " in req:
        #    quit()
        elif "wikipédia" in req:
            parler("recherche en cours .... ")
            req = req.replace("wikipédia", "")
            wikipedia.set_lang("fr")
            res = wikipedia.summary(req, sentences=2)
            print(res)
            parler(res)
        elif "email" in req:
            try:
                parler('Comment puis-je vous aidez ?')
                continu = commande()
                cible = "xyz@gmail.com"
                envoi_email(cible, contenu)
                parler("Email envoyer avec succès")
            except Exception as e:
                print(e)
                parler('Envoi impossible ')
        elif 'ouvrir youtube' in req:
            lien = commande()
            wb.open("youtube.com")
        elif 'ouvrir google' in req:
            lien = commande()
            wb.open("google.com")
        elif 'internet' in req:
            parler("Donner moi l'adresse du site internet ?")
            lien = commande()
            chemin = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome %s"
            wb.get(chemin).open_new_tab(lien)
        elif 'déconecter' in req:
            os.system('shutdown -l') #logout
        elif 'arrêter le system' in req:
            os.system('shudown /s/t 1') #shutdown
        elif 'redémarrer' in req:
            os.system('shudown /r/t 1') #restart
        # écouter de la musique
        elif 'musique' in req:
            chemin = "/System/Applications/Music.app"
            son = os.listdir(chemin)           
            os.system(os.path.join(chemin, son[0]))
        # fonction de rappel
        elif "note" in req:
            parler("Que dois-retenir pour vous ?")
            rappel = commande()
            parler("Vous m'avez demander de noter: " + rappel)
            fichier = open("Notes.app", 'w')
            fichier.write(rappel)
            fichier.close()
        # verification des notes
        elif "lire" in req:
            fichier = open('Note.app', 'r')
            parler("Vous m'avez demander de noter: " + fichier.read())

        elif 'capture' in req:
            capture()
            parler('La capture à bien été prise')

        elif "système" in req:
            infoOrddi()

