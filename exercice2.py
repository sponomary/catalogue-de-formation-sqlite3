#!/usr/bin python3
# -*- coding: utf-8 -*- 

# Importation des packages
import sqlite3

# Connection à la bdd
bdd = sqlite3.connect ('Formation.db') 
bdd.text_factory = str # format pour UTF-8 permettant de lire d'UTF-8 au lieu d'ASCII
curseur = bdd.cursor() # permet de manipuler la BDD (création, séléction, supression de données)


#-----------------------------------------------------------------------------------------------#
#                                   Le nombre total de départements                             #
#-----------------------------------------------------------------------------------------------#
curseur.execute("SELECT COUNT(idDepartement) FROM Departements;")
nombreDepartement  = str(curseur.fetchone()[0])

#-----------------------------------------------------------------------------------------------#
#                                   Le nombre total d’employés                                  #
#-----------------------------------------------------------------------------------------------#
curseur.execute("SELECT COUNT(idEmploye) FROM Employes;")
nombreEmploye  = str(curseur.fetchone()[0])


# On affiche le nombre total des departements et leurs employés
print(f"\nL'entreprise contient {nombreDepartement} départements pour un total de {nombreEmploye} employés.\n")


#-----------------------------------------------------------------------------------------------------------#
# Nom de chaque département et de la personne qui le dirige + le nombre d’employés dans chaque département  #
#-----------------------------------------------------------------------------------------------------------#
curseur.execute("""SELECT nomDepartement, E2.prenomEmploye, E2.nomEmploye, COUNT(E.idEmploye) AS nombreEmploye
                FROM Employes AS E JOIN Departements AS D
                ON E.departement = D.idDepartement JOIN Employes AS E2 
                ON E2.idEmploye = D.idSuperviseur
                GROUP BY idDepartement;""")
for resultat in curseur.fetchall():
    print(f"Le département '{ resultat[0]}' est dirigé par {str(resultat[1])} {str(resultat[2])} et contient {str(resultat[3])} employés.")


# Déconnexion de la base de données
bdd.close()