#!/usr/bin python3
# -*- coding: utf-8 -*- 

# Importation des packages
import sqlite3

# Connection à la bdd
bdd = sqlite3.connect ('Formation.db') 
bdd.text_factory = str # format pour UTF-8 permettant de lire d'UTF-8 au lieu d'ASCII
curseur = bdd.cursor() # permet de manipuler la BDD (création, séléction, supression de données)

# Permet de saisir le prénom et le nom du superviseur au clavier
prenomSuperviseur = input("Saisir le prénom du superviseur : ")
nomSuperviseur = input("Saisir le nom du superviseur : ")

#-----------------------------------------------------------------------------------------------#
#                 Recherche dans la bdd si le superviseur existe                                #
#-----------------------------------------------------------------------------------------------#   
curseur.execute("""SELECT idEmploye FROM Employes
                WHERE UPPER(prenomEmploye) = UPPER(?) AND UPPER(nomEmploye) = UPPER(?);""", 
                (prenomSuperviseur, nomSuperviseur))
superviseur = curseur.fetchall()

if len(superviseur) == 0 :
    # Affichage d'un message d'erreur si l'employé n'existe pas
    print(f"\nLe superviseur {prenomSuperviseur} {nomSuperviseur} n'existe pas !")
else :
    #-----------------------------------------------------------------------------------------------#
    #                 Recherche dans la bdd les formations qui n’ont pas été suivies dans           #
    #                           le département cette année par ordre alphabétique                   #
    #-----------------------------------------------------------------------------------------------#   
    curseur.execute("""SELECT nomsFormations FROM Formations WHERE idFormation NOT IN(
                            SELECT F.idFormation FROM Employes AS E
                            INNER JOIN FormationsSuivies AS FS ON E.idEmploye = FS.idEmploye 
                            INNER JOIN Formations AS F ON FS.idFormation = F.idFormation 
                            INNER JOIN Departements AS D ON E.departement = D.idDepartement 
                            INNER JOIN Employes AS E2 ON D.idSuperviseur = E2.idEmploye 
                            WHERE UPPER(E2.prenomEmploye) = UPPER(?) AND UPPER(E2.nomEmploye) = UPPER(?)
                            AND FS.dateFormation BETWEEN '2020-01-01' AND '2020-12-31')
                        ORDER BY UPPER(nomsFormations) ASC;""", 
                        (prenomSuperviseur, nomSuperviseur))
    formations  = curseur.fetchall()

    # Affichage des formations qui n’ont pas été suivies dans le département cette année par ordre alphabétique
    if len(formations) > 0 :
        print("\nLes formations qui n’ont pas été suivies dans le département sont : ")
        for formation in formations  :
            print(f"\t- {formation[0]}")
    else :
        print("\nToutes les formations ont été suivies.")


    #-----------------------------------------------------------------------------------------------#
    #      Recherche dans la bdd les employés d'un département qui n’ont suivi aucune formation     #
    #-----------------------------------------------------------------------------------------------#   
    curseur.execute("""SELECT E.prenomEmploye, E.nomEmploye, COUNT(F.idFormation) AS nombreFormation
                        FROM Employes AS E
                        INNER JOIN Departements AS D ON E.departement = D.idDepartement 
                        INNER JOIN Employes AS E2 ON D.idSuperviseur = E2.idEmploye
                        LEFT OUTER JOIN FormationsSuivies AS FS ON E.idEmploye = FS.idEmploye
                        LEFT OUTER JOIN Formations AS F ON FS.idFormation = F.idFormation
                        WHERE UPPER(E2.prenomEmploye) = UPPER(?) AND UPPER(E2.nomEmploye) = UPPER(?)
                        GROUP BY E.prenomEmploye, E.nomEmploye
                        HAVING COUNT(F.idFormation) = 0;""", 
                        (prenomSuperviseur, nomSuperviseur))
    employes  = curseur.fetchall()

    # Affichage des employés qui n’ont suivi aucune formation
    if len(employes) > 0 :
        print("\nLes employés qui n’ont suivi aucune formation sont : ")
        for employe in employes  :
            print(f"\t- {employe[0]} {employe[1]}")
    else :
        print("\nTous les employés ont suivi une formation.")  # si 0 employé dans la réponse de la requête

# Déconnexion de la base de données
bdd.close()
