import os

def afficher_fichiers_txt(repertoire):
    for chemin_racine, dossiers, fichiers in os.walk(repertoire):
        for fichier in fichiers:
            if fichier.endswith('.txt'):
                chemin_complet = os.path.join(chemin_racine, fichier)
                print(chemin_complet)

# Remplacez 'votre_dossier' par le chemin de votre dossier
dossier_a_parcourir = 'xp0lssho4ybg7x56xkd5k5ne5ncx8t'
afficher_fichiers_txt(dossier_a_parcourir)
