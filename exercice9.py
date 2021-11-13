#!/usr/bin python3
# -*- coding: utf-8 -*- 

# Importation des packages
import sqlite3

# Connection à la bdd
bdd = sqlite3.connect ('Formation.db') 
bdd.text_factory = str # format pour UTF-8 permettant de lire d'UTF-8 au lieu d'ASCII
curseur = bdd.cursor() # permet de manipuler la bdd (création, séléction, supression de données)

# Permet de saisir le prénom et le nom du superviseur au clavier
prenomSuperviseur = input("Saisir le prénom du superviseur : ")
nomSuperviseur = input("Saisir le nom du superviseur : ")

#-----------------------------------------------------------------------------------------------#
#                 Recherche dans la bdd si le superviseur existe                                #
#-----------------------------------------------------------------------------------------------#   
curseur.execute("""SELECT idEmploye FROM Employes
                WHERE UPPER(prenomEmploye) = UPPER(?) AND UPPER(nomEmploye) = UPPER(?)""", 
                (prenomSuperviseur, nomSuperviseur))
superviseur = curseur.fetchall()

if len(superviseur) == 0 :
    # Affichage d'un message d'erreur si l'employé n'existe pas
    print(f"\nLe superviseur {prenomSuperviseur} {nomSuperviseur} n'existe pas !")
else :
    #----------------------------------------------------------------------------------------------------------#
    #   Recherche dans la bdd les employés du département qui ont rempli leur quota de formation pour l’année  #
    #----------------------------------------------------------------------------------------------------------#
    curseur.execute("""SELECT E.prenomEmploye, E.nomEmploye, COUNT(F.idFormation) AS nombreFormation
                        FROM Employes AS E
                        INNER JOIN Departements AS D ON E.departement = D.idDepartement 
                        INNER JOIN Employes AS E2 ON D.idSuperviseur = E2.idEmploye
                        INNER JOIN FormationsSuivies AS FS ON E.idEmploye = FS.idEmploye
                        INNER JOIN Formations AS F ON FS.idFormation = F.idFormation
                        WHERE UPPER(E2.prenomEmploye) = UPPER(?) AND UPPER(E2.nomEmploye) = UPPER(?)
                        AND FS.dateFormation BETWEEN '2020-01-01' AND '2020-12-31'
                        GROUP BY E.prenomEmploye, E.nomEmploye
                        HAVING COUNT(F.idFormation) >=5;""", 
                        (prenomSuperviseur, nomSuperviseur))
    employes  = curseur.fetchall()

    # Affichage des employés du département qui ont rempli leur quota de formation pour l’année
    if len(employes) > 0 :
        print("\nLes employés du département qui ont rempli leur quota de formation sont : ")
        for employe in employes  :
            print(f"\t- {employe[0]} {employe[1]}")
    else :
        print("\nAucun employé du département n'a rempli son quota de formation.")

# Déconnexion de la base de données
bdd.close()