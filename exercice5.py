#!/usr/bin python3
# -*- coding: utf-8 -*- 

# Importation des packages
import sqlite3

# Connection à la bdd
bdd = sqlite3.connect ('Formation.db') 
bdd.text_factory = str # format pour UTF-8 permettant de lire d'UTF-8 au lieu d'ASCII
curseur = bdd.cursor() # permet de manipuler la BDD (création, séléction, supression de données)

# Permet de saisir le prénom et le nom du superviseur au clavier
prenomSuperviseur = input("Saisissez le prénom du superviseur : ")
nomSuperviseur = input("Saisissez le nom du superviseur : ")


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
    #------------------------------------------------------------------------------------------------#
    # Recherche dans la bdd du nombre de formations suivies cette année par ses employés directs     #
    # et le volume horaire que cela représente                                                       #
    #------------------------------------------------------------------------------------------------#
    curseur.execute("""SELECT E.prenomEmploye, E.nomEmploye, COUNT(F.idFormation) AS nombreFormation,
                        COALESCE(SUM(dureeFormation),0) AS dureeFormation FROM Employes AS E
                        INNER JOIN Employes AS E2 ON E.idSuperieur = E2.idEmploye
                        LEFT OUTER JOIN FormationsSuivies AS FS ON E.idEmploye = FS.idEmploye
                        LEFT OUTER JOIN Formations AS F ON FS.idFormation = F.idFormation
                        WHERE UPPER(E2.prenomEmploye) = UPPER(?) AND UPPER(E2.nomEmploye) = UPPER(?)
                        GROUP BY E.prenomEmploye, E.nomEmploye
                        UNION
                        SELECT E.prenomEmploye, E.nomEmploye, COUNT(F.idFormation) AS nombreFormation,
                        COALESCE(SUM(dureeFormation),0) AS dureeFormation FROM Employes AS E 
                        LEFT OUTER JOIN FormationsSuivies AS FS ON E.idEmploye = FS.idEmploye
                        LEFT OUTER JOIN Formations AS F ON FS.idFormation = F.idFormation
                        WHERE UPPER(E.prenomEmploye) = UPPER(?) AND UPPER(E.nomEmploye) = UPPER(?);""", 
                        
                        (prenomSuperviseur, nomSuperviseur, prenomSuperviseur, nomSuperviseur))
    nombreVolumeEmployeDirect  = curseur.fetchall()

    # Affichage du nombre total de formations suivies et le volume horaire total pour chaque employé
    if len(nombreVolumeEmployeDirect) > 0 :
        print("\nNombre de formations suivies cette année par ses employés directs et le volume horaire que cela représente : ")
        for employe in nombreVolumeEmployeDirect  :
            print(f"\t- Employé : {employe[0]} {employe[1]}; Nombre de formation : {employe[2]}; Durée: {employe[3]} heure(s).")
    else :
        print(f"\nPas de formations suivies pour les employés du superviseur {prenomSuperviseur} {nomSuperviseur}.")

    #----------------------------------------------------------------------------------#
    # Recherche dans la bdd le nombre de formations pour chaque employé du département #
    #----------------------------------------------------------------------------------#
    curseur.execute("""SELECT E.prenomEmploye, E.nomEmploye, COUNT(F.idFormation) AS nombreFormation
                        FROM Employes AS E
                        INNER JOIN Departements AS D ON E.departement = D.idDepartement
                        INNER JOIN Employes AS E2 ON D.idSuperviseur = E2.idEmploye
                        LEFT OUTER JOIN FormationsSuivies AS FS ON E.idEmploye = FS.idEmploye
                        LEFT OUTER JOIN Formations AS F ON FS.idFormation = F.idFormation
                        WHERE UPPER(E2.prenomEmploye) = UPPER(?) AND UPPER(E2.nomEmploye) = UPPER(?)
                        GROUP BY E.prenomEmploye, E.nomEmploye;""", 
                    (prenomSuperviseur,nomSuperviseur))
    nombreFormationParEmploye  = curseur.fetchall()

    # Affichage du nombre de formations pour chaque employé du département
    if len(nombreFormationParEmploye) > 0 :
        print("\nNombre de formations suivies pour chaque employé du département :")
        for employe in nombreFormationParEmploye  :
            print(f"\t- {employe[0]} {employe[1]} : {str(employe[2])} formations.")
    else :
        print(f"\nPas de formations suivies pour le département du superviseur {prenomSuperviseur} {nomSuperviseur}.")
    
    #-----------------------------------------------------------------------------------------------#
    #                 Recherche dans la bdd de la formation la plus populaire du département        #
    #-----------------------------------------------------------------------------------------------#
    curseur.execute("""SELECT nomDepartement, F.nomsFormations, COUNT(F.idFormation) AS nombreFormation
                        FROM Employes AS E
                        JOIN FormationsSuivies AS FS ON E.idEmploye = FS.idEmploye
                        JOIN Formations AS F ON FS.idFormation = F.idFormation
                        JOIN Departements AS D ON E.departement = D.idDepartement
                        JOIN Employes AS E2 ON D.idSuperviseur = E2.idEmploye
                        WHERE UPPER(E2.prenomEmploye) = UPPER(?) AND UPPER(E2.nomEmploye) = UPPER(?)
                        GROUP BY nomDepartement, F.nomsFormations, F.idFormation
                        ORDER BY nombreFormation DESC
                        LIMIT 1;""", 
                        (prenomSuperviseur, nomSuperviseur))
    formationPlusPopulaire = curseur.fetchall()

    if len(formationPlusPopulaire) > 0 :
        for row in formationPlusPopulaire  :
            print(f'\nLa formation la plus populaire du département {row[0]} est "{row[1]}".')
    else :
        print(f"\nPas de formations suivies pour le département du superviseur {prenomSuperviseur} {nomSuperviseur}.")

# Déconnexion de la base de données
bdd.close()