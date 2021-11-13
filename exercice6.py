import sqlite3
import datetime

# Connection à la BD
bdd = sqlite3.connect ('Formation.db')

# L'histoire d'encodage
bdd.text_factory = str

curseur = bdd.cursor() # permet de manipuler la BDD (creation, selection, supression de données)

# Permet de saisir le prénom et le nom du superviseur au clavier
prenomSuperviseur = input("Saisir le prénom du superviseur : ")
nomSuperviseur = input("Saisir le nom du superviseur : ")
dateSaisie = input("Saisir une date sous la forme YYYY-MM-DD : ")

try:
    datetime.datetime.strptime(dateSaisie, '%Y-%m-%d')

    #----------------------------------------------------------------------------------------------#
    #               Recherche dans la base de donnée si le superviseur existe                      #                
    #----------------------------------------------------------------------------------------------#
    curseur.execute("SELECT idEmploye FROM Employes \
                    WHERE UPPER(prenomEmploye) = UPPER(?) AND UPPER(nomEmploye) = UPPER(?);", 
                    (prenomSuperviseur, nomSuperviseur))

    superviseur = curseur.fetchall()

    if len(superviseur) == 0 :
        print(f"\nLe superviseur {prenomSuperviseur} {nomSuperviseur} n'existe pas !") # Affichage d'un message d'erreur si l'employé existe pas
    else :
        #----------------------------------------------------------------------------------------------#
        # Recherche dans la BD les formations suivies à l’échelle du département avant le 10 mars 2020 #                
        #----------------------------------------------------------------------------------------------#
        curseur.execute("""SELECT F.nomsFormations
                            FROM Employes AS E
                            INNER JOIN FormationsSuivies AS FS ON E.idEmploye = FS.idEmploye 
                            INNER JOIN formations AS F ON FS.idFormation = F.idFormation 
                            INNER JOIN Departements AS D ON E.departement = D.idDepartement 
                            INNER JOIN Employes AS E2 ON D.idSuperviseur = E2.idEmploye 
                            WHERE UPPER(E2.prenomEmploye) = UPPER(?) AND UPPER(E2.nomEmploye) = UPPER(?)
                            AND FS.dateFormation BETWEEN '2020-01-01' AND ?
                            GROUP BY F.idFormation;""", 
                            (prenomSuperviseur, nomSuperviseur, dateSaisie))

        formations  = curseur.fetchall()

        # Affichage des formations suivies à l’échelle du département avant le 10 mars 2020
        if len(formations) > 0 :
            print(f"\nLes formations suivies à l’échelle du département avant le {dateSaisie} sont :")
            for formation in formations  :
                print(f"\t- {formation[0]}")
        else :
            print(f"\nPas de formation avant le {dateSaisie} suivie à l’échelle du département.\n")

        #----------------------------------------------------------------------------------------------#
        #               Par exemple, on voudra afficher les formations suivies à l’échelle du          #
        #                               groupe avant la date saisie en entrée                          #                
        #----------------------------------------------------------------------------------------------#
        curseur.execute("""SELECT F.nomsFormations FROM Employes AS E
                            INNER JOIN FormationsSuivies AS FS ON E.idEmploye = FS.idEmploye 
                            INNER JOIN Formations AS F ON FS.idFormation = F.idFormation 
                            WHERE FS.dateFormation BETWEEN '2020-01-01' AND ?
                            GROUP BY F.idFormation;""", 
                            (dateSaisie,))

        formationsGroupe  = curseur.fetchall()

        # Affichage des formations suivies à l’échelle du groupe avant la date saisie
        if len(formationsGroupe) > 0 :
            print(f"\nLes formations suivies à l’échelle du groupe avant le {dateSaisie} sont :")
            for formation in formationsGroupe  :
                print(f"\t- {formation[0]}")
        else :
            print(f"\nPas de formation avant le {dateSaisie} suivie à l’échelle du groupe.")


    # déconnexion de la base de données
    bdd.close()

except ValueError:
    print("La date saisie est incorrecte ou pas au bon format (YYYY-MM-DD) !")
    bdd.close()