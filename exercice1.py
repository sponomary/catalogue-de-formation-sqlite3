#!/usr/bin python3
# -*- coding: utf-8 -*- 

# Importation des packages
import sqlite3
import pandas as pd

bdd = sqlite3.connect ('Formation.db') # création d'une bdd
bdd.text_factory = str # format pour UTF-8 permettant de lire d'UTF-8 au lieu d'ASCII
curseur = bdd.cursor() # permet de manipuler la BDD (création, séléction, supression de données)


#-----------------------------------------------------------------------------------------------#
#                       Création des tables dans la base de données                             #
#-----------------------------------------------------------------------------------------------#
print("Création des tables de la base de données ...")
curseur.execute("""CREATE TABLE Formations
                (idFormation TEXT PRIMARY KEY,
                nomsFormations TEXT NOT NULL,
                dureeFormation INTEGER NOT NULL);""") 

curseur.execute("""CREATE TABLE Employes
                (idEmploye TEXT PRIMARY KEY,
                nomEmploye TEXT NOT NULL,
                prenomEmploye TEXT NOT NULL);""") 

curseur.execute("""CREATE TABLE Departements
                (idDepartement TEXT PRIMARY KEY,
                nomDepartement TEXT NOT NULL,
                idSuperviseur TEXT NOT NULL,
                FOREIGN KEY(idSuperviseur) REFERENCES Employes(idEmploye));""") 

curseur.execute("""CREATE TABLE FormationsSuivies
                (idEmploye TEXT NOT NULL,
                idFormation TEXT NOT NULL,
                dateFormation TEXT NOT NULL,
                PRIMARY KEY (idEmploye, idFormation, dateFormation));""") 



#-----------------------------------------------------------------------------------------------#
#                                   Ajouts des colonnes                                         #
#-----------------------------------------------------------------------------------------------#
# Ajout de la colonne avec la clé étrangère dans la table Employes
curseur.execute("ALTER TABLE Employes ADD COLUMN departement TEXT REFERENCES Departements(idDepartement);")

# Ajout de la colonne idSuperieur dans la table Employes pour créer la hiérachie entre les employés
curseur.execute("ALTER TABLE Employes ADD COLUMN idSuperieur TEXT REFERENCES Employes(idEmploye);")

# commit() est utilisé quand on modifie la bdd
bdd.commit()


#-----------------------------------------------------------------------------------------------#
#                Insertion des données dans la base de données avec Pandas                      #
#-----------------------------------------------------------------------------------------------#
print("Insertions des données dans la base de données ...")
# Traitement des données du fichier des formations
fichierCsv = pd.read_csv('formations.csv') # lecture du fichier
# Insertion des données
fichierCsv.to_sql('Formations', bdd, if_exists='append', index = False)

# Traitement des données du fichier des employes
fichierCsv = pd.read_csv('employes.csv')
# Insertion des données
fichierCsv.to_sql('Employes', bdd, if_exists='append', index = False)

# Traitement des données du fichier des departements
fichierCsv = pd.read_csv('departements.csv')
# Insertion des données
fichierCsv.to_sql('Departements', bdd, if_exists='append', index = False)

# Traitement des données du fichier des formationsSuivies
fichierCsv = pd.read_csv('formationsSuivies.csv')
# Insertion des données
fichierCsv.to_sql('FormationsSuivies', bdd, if_exists='append', index = False)



#---------------------------------------------------------------------------------------------#
#                           Modification du format de DATE                                    #
#---------------------------------------------------------------------------------------------#
curseur.execute("""UPDATE FormationsSuivies SET dateFormation = substr(dateFormation, 7) || '-' 
                || substr(dateFormation,4,2) || '-' || substr(dateFormation, 1,2);""")



#---------------------------------------------------------------------------------------------#
#                   Ajout de la hierarchie dans la table Employes                             #
#---------------------------------------------------------------------------------------------#
curseur.execute("UPDATE Employes SET idSuperieur ='N10267' WHERE idEmploye ='E81947';")
curseur.execute("UPDATE Employes SET idSuperieur ='G81311' WHERE idEmploye ='O45757';")
curseur.execute("UPDATE Employes SET idSuperieur ='N10267' WHERE idEmploye ='R96803';")
curseur.execute("UPDATE Employes SET idSuperieur ='Z10219' WHERE idEmploye ='J03677';")
curseur.execute("UPDATE Employes SET idSuperieur ='O45757' WHERE idEmploye ='R39037';")
curseur.execute("UPDATE Employes SET idSuperieur ='O45757' WHERE idEmploye ='G88363';")
curseur.execute("UPDATE Employes SET idSuperieur ='T29469' WHERE idEmploye ='A05562';")
curseur.execute("UPDATE Employes SET idSuperieur ='X76580' WHERE idEmploye ='W72933';")
curseur.execute("UPDATE Employes SET idSuperieur ='Z10219' WHERE idEmploye ='T29469';")
curseur.execute("UPDATE Employes SET idSuperieur ='Q45576' WHERE idEmploye ='A45580';")
curseur.execute("UPDATE Employes SET idSuperieur ='N10267' WHERE idEmploye ='O43477';")
curseur.execute("UPDATE Employes SET idSuperieur ='O45757' WHERE idEmploye ='N10267';")
curseur.execute("UPDATE Employes SET idSuperieur ='X76580' WHERE idEmploye ='Q30419';")
curseur.execute("UPDATE Employes SET idSuperieur ='Z10219' WHERE idEmploye ='X76580';")
curseur.execute("UPDATE Employes SET idSuperieur ='O45757' WHERE idEmploye ='Q45576';")
curseur.execute("UPDATE Employes SET idSuperieur ='G81311' WHERE idEmploye ='Z10219';")
curseur.execute("UPDATE Employes SET idSuperieur ='N10267' WHERE idEmploye ='K38048';")
curseur.execute("UPDATE Employes SET idSuperieur ='T29469' WHERE idEmploye ='I35422';")
curseur.execute("UPDATE Employes SET idSuperieur ='Q45576' WHERE idEmploye ='L64586';")


bdd.commit()


#---------------------------------------------------------------------------------------------#
#                           Validation de création des données                                #
#---------------------------------------------------------------------------------------------#
print("\nNombre d'enregistrements dans chaque table de la base de données : ")
curseur.execute("SELECT COUNT(idFormation) FROM Formations;")
print('       ' + str(curseur.fetchone()[0]) + ' enregistrements dans la table Formations' )

curseur.execute("SELECT COUNT(idEmploye) FROM Employes;")
print('       ' + str(curseur.fetchone()[0]) + ' enregistrements dans la table Employes' )

curseur.execute("SELECT COUNT(idDepartement) FROM Departements;")
print('       ' + str(curseur.fetchone()[0]) + ' enregistrements dans la table Departements' )

curseur.execute("SELECT COUNT(*) FROM FormationsSuivies;")
print('       ' + str(curseur.fetchone()[0]) + ' enregistrements dans la table FormationsSuivies' )


# déconnexion de la bdd
bdd.close()