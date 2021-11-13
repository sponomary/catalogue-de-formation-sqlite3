#!/usr/bin python3
# -*- coding: utf-8 -*- 

# Importation des packages
import sqlite3

# Connection à la bdd
bdd = sqlite3.connect ('Formation.db') 
bdd.text_factory = str # format pour UTF-8 permettant de lire d'UTF-8 au lieu d'ASCII
curseur = bdd.cursor() # permet de manipuler la BDD (création, séléction, supression de données)

# Permet de saisir le prénom et le nom de l'employé au clavier
prenomEmploye = input("Saisissez le prénom de l'employé dont vous voulez consulter les informations : ")
nomEmploye = input("Saisissez le nom de l'employé dont vous voulez consulter les informations : ")

# Permet de saisir le prénom et le nom du superviseur au clavier
prenomSuperviseur = input("Saisissez le prénom du superviseur : ")
nomSuperviseur = input("Saisissez le nom du superviseur : ")

#-----------------------------------------------------------------------------------------------#
#                 Recherche dans la bdd si l'employé existe                                     #
#-----------------------------------------------------------------------------------------------#
curseur.execute("""SELECT idEmploye FROM Employes
                WHERE UPPER(prenomEmploye) = UPPER(?) AND UPPER(nomEmploye) = UPPER(?);""", 
                (prenomEmploye, nomEmploye)) 
employe = curseur.fetchall()

#-----------------------------------------------------------------------------------------------#
#                 Recherche dans la bdd si le superviseur existe                                #
#-----------------------------------------------------------------------------------------------#
curseur.execute("""SELECT idEmploye FROM Employes
                WHERE UPPER(prenomEmploye) = UPPER(?) AND UPPER(nomEmploye) = UPPER(?);""", 
                (prenomSuperviseur, nomSuperviseur))
superviseur = curseur.fetchall()

if len(employe) == 0 :
    # Affichage d'un message d'erreur si l'employé n'existe pas
    print(f"\nL'employé {prenomEmploye} {nomEmploye} n'existe pas !") 
elif len(superviseur) == 0 : 
    # Affichage d'un message d'erreur si l'employé n'existe pas
    print(f"\nLe superviseur {prenomSuperviseur} {nomSuperviseur} n'existe pas !") 
else :
    #-----------------------------------------------------------------------------------------------#
    #                Recherche dans la bdd si il s'agit du superviseur de l'employé                 #
    #-----------------------------------------------------------------------------------------------#
    curseur.execute("""SELECT E.prenomEmploye, E.nomEmploye, E2.prenomEmploye AS prenomSuperviseur, 
                        E2.nomEmploye AS nomSuperviseur FROM Employes AS E JOIN Employes AS E2 
                        ON E.idSuperieur = E2.idEmploye
                        WHERE UPPER(E.prenomEmploye) = UPPER(?) AND UPPER(E.nomEmploye) = UPPER(?)
                        AND UPPER(E2.prenomEmploye) = UPPER(?) AND UPPER(E2.nomEmploye) = UPPER(?);""", 
                        (prenomEmploye, nomEmploye, prenomSuperviseur, nomSuperviseur)) 
    isSuperviseur  = curseur.fetchall()
    if len(isSuperviseur) > 0 or ( prenomEmploye.upper() == prenomSuperviseur.upper() 
    and nomEmploye.upper() == nomSuperviseur.upper()):
        #-----------------------------------------------------------------------------------------------#
        #                Recherche dans la bdd les formations suivies par l'employé                     #
        #-----------------------------------------------------------------------------------------------#
        curseur.execute("""SELECT nomsFormations, dureeFormation, dateFormation FROM Employes AS E
                        JOIN FormationsSuivies AS FS ON E.idEmploye = FS.idEmploye
                        JOIN Formations AS F ON FS.idFormation = F.idFormation
                        WHERE UPPER(prenomEmploye) = UPPER(?) AND UPPER(nomEmploye) = UPPER(?);""", 
                        (prenomEmploye, nomEmploye))
        formations  = curseur.fetchall()

        # Affichage de la liste de formations pour l'employé saisi
        if len(formations) > 0 :
            print(f"\nLes formations suivies par {prenomEmploye} {nomEmploye} sont : ")
            for formation in formations :
                print(f"\t- Nom de la formation: {formation[0]}, Durée: {formation[1]} heure(s), Date: {formation[2]}.")
        else :
            print(f"\n{prenomEmploye} {nomEmploye} n'a suivi aucune formation.")

        #-----------------------------------------------------------------------------------------------#
        #     Recherche dans la bdd le nombre total de formations suivies et le volume horaire total    #
        #-----------------------------------------------------------------------------------------------#
        curseur.execute("""SELECT prenomEmploye, nomEmploye, COUNT(F.idFormation) AS nombreFormation,
                        COALESCE(SUM(dureeFormation),0) AS dureeFormation FROM Employes AS E
                        LEFT OUTER JOIN FormationsSuivies AS FS ON E.idEmploye = FS.idEmploye
                        LEFT OUTER JOIN formations AS F ON FS.idFormation = F.idFormation
                        WHERE UPPER(prenomEmploye) = UPPER(?) AND UPPER(nomEmploye) = UPPER(?);""", 
                        (prenomEmploye, nomEmploye))
        nombreVolumeFormation  = curseur.fetchone() # Une seule ligne de résultat
        # Affichage du nombre total de formations suivies et le volume horaire total
        print(f"\n{prenomEmploye} {nomEmploye} a suivi {str(nombreVolumeFormation[2])} \
formations pour un volume horaire total de {str(nombreVolumeFormation[3])} heure(s).")
    else :
       print("\nAccès non autorisé aux informations de cet employé.")

# Déconnexion de la base de données
bdd.close()