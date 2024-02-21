#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 14:56:22 2023

@author: maissa
"""
import time
import tkinter as tk
import random
from tkinter import *
import os
from tkinter import ttk
import csv
import json
from tkinter import *
from tkinter import ttk
import os
from collections import Counter

'-------------------------------------------------------------------------------------------------------'

def login():
    username = username_entry.get()
    password = password_entry.get()
    File_name = os.listdir()
    if str(username)+".csv" in File_name:
        File = open(str(username)+".csv", "r")
        liste_info = File.read().split(",")
        File.close()
        if password == liste_info[1] :
            messagebox.showinfo("Connexion réussie", f"Connexion réussie pour {username}")
            # Fermez la fenêtre de connexion
            root1.destroy()
            # Appelez la fonction pour afficher la fenêtre de jeu
            fenetre1(username,password)
            # Démarrer l'application
            root.mainloop()
            return
        else:
            messagebox.showerror("Erreur", "Mot de passe incorrect. Réessayez.")
            return
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur non trouvé. Veuillez vous inscrire.")
    return username,password
    
def register():
    username = username_entry.get()
    password = password_entry.get()    
    File = os.listdir()
    if str(username)+".csv" in File:
        messagebox.showerror("Erreur", "Ce nom d'utilisateur est déjà utilisé. Choisissez un autre.")
        return
    else: 
        File = open(str(username)+".csv", "w")
        File.write(str(username)+","+str(password)+",")
        File.close()
        print("Message 2 : Votre comte a été crée avec succès !")
        messagebox.showinfo("Inscription réussie", f"Inscription réussie pour {username}")
        # Fermez la fenêtre de connexion
        root1.destroy()
        # Appelez la fonction pour afficher la fenêtre de jeu
        fenetre1(username,password)
        # Démarrer l'application
        root.mainloop()
        return
    return username,password
'-------------------------------------------------------------------------------------------------------'
def fenetre1(username,password):
    
    def lire():
        f = open("yelp_academic_dataset_business.json",'r', encoding="utf8")
        json_lines = []
        lines = f.readlines()
        for i in range(0,len(lines)):
            data = json.loads(lines[i])
            json_lines.append(data)
        return json_lines
    
    def rechercher():
        
        def lire():
            f = open("yelp_academic_dataset_business.json",'r', encoding="utf8")
            json_lines = []
            lines = f.readlines()
            for i in range(0,len(lines)):
                data = json.loads(lines[i])
                json_lines.append(data)
            return json_lines   
        
        texte_recherche = entry.get()
        recherche_par = option_menu.get()  # Récupère le choix de l'option
        resultat_label.config(text=f"Vous avez recherché : {texte_recherche}")
        json_lines=lire()
        
        
        def triplet(cle, operateur, valeur):
            dictio=	{}
            for business in json_lines:
                if operateur == "=":
                    if business[cle] == valeur:
                        ide=business['business_id']
                        nom = business['name']
                        ville = business['city']
                        categories = business.get('categories', '')  # Utilisation de get pour gérer le cas où 'categories' est absent
                        note = str(business['stars'])          
                        # Ajoutez chaque restaurant au dictionnaire
                        dictio[ide] = {"nom":nom,"ville": ville, "categorie": categories, "note": note}
                                           
            if not dictio:  # Si dictio est vide
                return 0
            else:
                return dictio
                        
        def triplet2(cle, operateur, valeur):
            dictio=	{}
            for business in json_lines:
                if operateur == "=":
                    liste=str(business[cle]).split(',')
                    if valeur in liste:
                        ide=business['business_id']
                        nom = business['name']
                        ville = business['city']
                        categories = business.get('categories', '')  # Utilisation de get pour gérer le cas où 'categories' est absent
                        note = str(business['stars'])          
                        # Ajoutez chaque restaurant au dictionnaire
                        dictio[ide] = {"nom":nom,"ville": ville, "categorie": categories, "note": note}
                                           
            if not dictio:  # Si dictio est vide
                return 0
            else:
                return dictio
                    
        def best_of(dictio):
            if dictio==0:
                return 0
            else:
                liste_paire=[]
                for ide, infos in dictio.items():
                    liste_paire.append((ide,infos["note"]))
                liste_paire_triee=[]
                while liste_paire:
                    max_pair=liste_paire[0]
                    for pair in liste_paire:
                        if pair[1]>max_pair[1]:
                            max_pair=pair
                    liste_paire.remove(max_pair)
                    liste_paire_triee.append(max_pair)
                    
                dictio_triee={}
                for pair in liste_paire_triee:
                    ide,note=pair
                    dictio_triee[ide]=dictio[ide]
                return dictio_triee
        
                            
        def address_by_name(business_name, data):                  
            for business in data:
                if business['name'] == business_name:
                    return business['address']
        def note_by_name(business_name,data):
            for business in data:
                if business['name'] == business_name:
                    return business['stars']
        def recommandation_by_name(business_name,data):
            for business in data:
                if business['name'] == business_name:
                    return business['review_count']
                
        def categorie_by_name(business_name,data):
            for business in data:
                if business['name'] == business_name:
                    return business['categories'] 
                
        def hours_by_name(business_name,data):
            for business in data:
                if business['name'] == business_name:
                    return business['hours']       
        
        if recherche_par == "Ville":
            print("vous cherchez par localisation")
            resultats = triplet("city","=",texte_recherche)
            if resultats != 0:
                best_of_restaurant=best_of(resultats)
                compteur =0
                liste_best=[]
                for ide, infos in best_of_restaurant.items():
                    liste_best.append(f"Nom : {infos['nom']}")
                    liste_best.append(f"Ville : {infos['ville']}")
                    liste_best.append(f"Note : {infos['note']}")
                    compteur+=1
                    if compteur ==5:
                        break
                liste_formatee="\n".join(liste_best)
                resultat_label2.config(text=f"Voila les meilleurs restaurant à : {texte_recherche}")
                resultat_label3.config(text=f"{liste_formatee}")
                File = open(str(username)+".csv", "a")
                File.write(","+str(recherche_par)+","+str(texte_recherche))
                File.close()
            else: 
                resultat_label3.config(text=f"Erreur : le texte rechercher n'existe pas ")

        if recherche_par=="Nom":
            print("vous cherchez par nom")
            
            resultats=triplet("name", "=", texte_recherche)
            if resultats!=0:
                best_of_restaurant=best_of(resultats)
                compteur =0
                liste_best=[]
                for ide, infos in best_of_restaurant.items():
                    liste_best.append(f"Nom : {infos['nom']}")
                    liste_best.append(f"Ville : {infos['ville']}")
                    liste_best.append(f"Note : {infos['note']}")
                    compteur+=1
                    if compteur ==5:
                        break
                liste_formatee="\n".join(liste_best)
                resultat_label2.config(text=f"Voila les meilleurs restaurant : {texte_recherche}")
                resultat_label3.config(text=f"{liste_formatee}")
                File = open(str(username)+".csv", "a")
                File.write(","+str(recherche_par)+","+str(texte_recherche))
                File.close()
            else: 
                resultat_label3.config(text=f"Erreur : le texte rechercher n'existe pas ") 
               
        if recherche_par=="Categorie":
            print("vous cherchez par gategorie")
            
            resultats=triplet2("categories", "=", texte_recherche)
            if resultats!=0:
                best_of_restaurant=best_of(resultats)
                compteur =0
                liste_best=[]
                for ide, infos in best_of_restaurant.items():
                    liste_best.append(f"Nom : {infos['nom']}")
                    liste_best.append(f"Ville : {infos['ville']}")
                    liste_best.append(f"Note : {infos['note']}")
                    compteur+=1
                    if compteur ==5:
                        break
                liste_formatee="\n".join(liste_best)
                resultat_label2.config(text=f"Voila les meilleurs restaurant de : {texte_recherche}")
                resultat_label3.config(text=f"{liste_formatee}")
                File = open(str(username)+".csv", "a")
                File.write(","+str(recherche_par)+","+str(texte_recherche))
                File.close()                
            else: 
                resultat_label3.config(text=f"Erreur : le texte rechercher n'existe pas ") 
                
    def recommandation():
        File = open(str(username)+".csv", "r")
        liste_info = File.read().split(",")
        File.close()
        liste_ville=[]
        liste_nom=[]
        liste_categorie=[]
        for i in range(len(liste_info)):
            if liste_info[i]=="Ville":
                liste_ville.append(liste_info[i+1])
            elif liste_info[i]=="Nom":
                liste_nom.append(liste_info[i+1])
            elif liste_info[i]=="Categorie":
                liste_categorie.append(liste_info[i+1])
        print(liste_info,liste_nom,liste_ville)
        def compteur(liste):
            compteur=Counter(liste)
            
            element, frequence = compteur.most_common(1)[0]
            
            return element
        
        ville=compteur(liste_ville)
        nom=compteur(liste_nom)
        categorie=compteur(liste_categorie)
        dictionaire={}
        for business in json_lines:
            liste_cat=str(business['categories']).split(',')
            if business['city']==ville and categorie in liste_cat:
                ide=business['business_id']
                nom = business['name']
                ville = business['city']
                categories = business.get('categories', '')  # Utilisation de get pour gérer le cas où 'categories' est absent
                note = str(business['stars'])          
                # Ajoutez chaque restaurant au dictionnaire
                dictionaire[ide] = {"nom":nom,"ville": ville, "categorie": categories, "note": note}
        if not dictionaire:
            return 0
        else :
            return dictionaire
     
    json_lines=lire()    
    recomandation=recommandation()
    if recomandation!=0:
        compteur=0
        liste_recomandation=[]
        for ide, infos in recomandation.items():
            liste_recomandation.append(f"Nom : {infos['nom']}")
            liste_recomandation.append(f"Ville : {infos['ville']}")
            liste_recomandation.append(f"Note : {infos['note']}")
            compteur+=1
            if compteur ==5:
                break
        liste_reco_formatee="\n".join(liste_recomandation)
        
    def tuto() :
        messagebox.showerror("Tuto", "Il suffit de choisir le critere de recherche.\nUne fois selectionner vous tapez dans la barre de recherche un mot clé/un nom/une ville et les resultats s'afficheront.\nATTENTION ! Il faut écrire en anglais pour les mots clés et utiliser la bonne orthographe avec des majuscules au bonne endroit pour les noms. Pour l'instant, seulement les villes d'USA sont répertoriés dans notre base de donnée.\nChercher pas exemple : McDonald's, Burgers, Philadelphia, Santa Barbara, Subway etc.")
        return
       
    # Création de la fenêtre principale
    fenetre = tk.Tk()
    fenetre.title("YELP")
    
    # Définir la taille de la fenêtre
    fenetre.geometry("800x600")
    
    # Changer la police
    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 14))
    
    # Création de la barre de recherche
    entry = tk.Entry(fenetre, font=("Helvetica", 12))
    entry.pack(pady=10)
    
    # Options de recherche
    options = ["Ville", "Nom","Categorie"]

    # Création du bouton déroulant pour choisir l'option de recherche
    option_menu = tk.StringVar()
    option_menu.set(options[0])  # Option par défaut
    option_dropdown = tk.OptionMenu(fenetre, option_menu, *options)
    option_dropdown.pack(pady=5)
    
    # Création du bouton "Rechercher"
    bouton = tk.Button(fenetre, text="Rechercher", font=("Helvetica", 12), command=rechercher)
    bouton.pack()
    
    tuto=tk.Button(fenetre, text="Tuto", font=("Helvetica", 12), command=tuto)
    tuto.pack()
    
    # Étiquette pour afficher le résultat de la recherche
    resultat_label = tk.Label(fenetre, text="", font=("Helvetica", 14))
    resultat_label.pack(pady=10)
    
    resultat_label2 = tk.Label(fenetre, text="", font=("Helvetica", 14))
    resultat_label2.pack(pady=10)
    
    resultat_label3 = tk.Label(fenetre, text="", font=("Helvetica", 14))
    resultat_label3.pack(pady=10)
    
    resultat_label4 = tk.Label(fenetre, text="", font=("Helvetica", 14))
    resultat_label4.pack(pady=10)
    
    resultat_label5 = tk.Label(fenetre, text="", font=("Helvetica", 14))
    resultat_label5.pack(pady=10)  

    resultat_label6 = tk.Label(fenetre, text="", font=("Helvetica", 14))
    resultat_label6.pack(pady=10) 

    resultat_label5.config(text=f"Voila les meilleurs restaurant pour vous")
    resultat_label6.config(text=f"{liste_reco_formatee}")    
    
    # Démarrez la boucle principale de l'interface utilisateur
    fenetre.mainloop()


'----------------------------------------------------------------------------------------------'
# Créez la fenêtre de connexion
root1 = tk.Tk()
root1.title("YELP - Connexion")

# Créez les widgets pour le nom d'utilisateur et le mot de passe
username_label = tk.Label(root1, text="Nom d'utilisateur:")
username_entry = tk.Entry(root1)

password_label = tk.Label(root1, text="Mot de passe:")
password_entry = tk.Entry(root1, show="*")  # Montre des astérisques pour le mot de passe

# Créez les boutons d'inscription et de connexion
register_button = tk.Button(root1, text="S'inscrire", command=register)
login_button = tk.Button(root1, text="Se connecter", command=login)

# Placez les widgets sur la fenêtre
username_label.pack()
username_entry.pack()
password_label.pack()
password_entry.pack()
register_button.pack()
login_button.pack()

# Exécutez la fenêtre principale
root1.mainloop()
