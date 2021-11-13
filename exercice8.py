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
    #-------------------------------------------------------------------------------------------#
    # Recherche dans la bdd les employés du département ayant suivi au moins une formation      #
    #           mais qui a effectué le moins d’heures de formation.                             #
    #-------------------------------------------------------------------------------------------#
    curseur.execute("""SELECT E.prenomEmploye, E.nomEmploye, SUM(dureeFormation), 
                        D.nomDepartement FROM Employes AS E 
                        INNER JOIN Departements AS D ON E.departement = D.idDepartement 
                        INNER JOIN Employes AS E2 ON D.idSuperviseur = E2.idEmploye
                        INNER JOIN FormationsSuivies AS FS ON E.idEmploye = FS.idEmploye
                        INNER JOIN Formations AS F ON FS.idFormation = F.idFormation
                        WHERE UPPER(E2.prenomEmploye) = UPPER(?) AND UPPER(E2.nomEmploye) = UPPER(?)
                        GROUP BY E.prenomEmploye, E.nomEmploye
                        HAVING SUM(dureeFormation) = (
                            SELECT SUM(dureeFormation) AS dureeFormation FROM Employes AS E
                            INNER JOIN Departements AS D ON E.departement = D.idDepartement 
                            INNER JOIN Employes AS E2 ON D.idSuperviseur = E2.idEmploye
                            INNER JOIN FormationsSuivies AS FS ON E.idEmploye = FS.idEmploye
                            INNER JOIN Formations AS F ON FS.idFormation = F.idFormation
                            WHERE UPPER(E2.prenomEmploye) = UPPER(?) AND UPPER(E2.nomEmploye) = UPPER(?)
                            GROUP BY E.prenomEmploye, E.nomEmploye
                            HAVING COUNT(F.idFormation) >=1
                        ORDER BY dureeFormation ASC
                        LIMIT 1);""", 
                        (prenomSuperviseur, nomSuperviseur, prenomSuperviseur, nomSuperviseur))
    employes = curseur.fetchall()

    # Affichage des employés du département ayant suivi au moins une formation mais qui a effectué le moins d’heures de formation.  
    if len(employes) > 0 :
        print("""\nLes employés du departement de ce superviseur qui ont suivi au moins une formation mais qui ont effectué le moins
         d’heures de formation sont : """)
        for employe in employes :
            print(f"\t- Employé : {employe[0]} {employe[1]} ; Nombre d'heures de formation : {employe[2]} heure(s).")
    # Si personne dans le département a suivi aucune formation (le cas si on saisi le nom de la directrice)
    else :
        print("\nLes employés de ce departement n'ont pas suivi les formations.")

# Déconnexion de la base de données
bdd.close()





