import math
import csv
import os

# Coordonnées de la navette
navette_coords = (93989.26972727024, 11093.029999241466, -61831.635981388965)

# Fonction pour calculer la distance euclidienne entre deux points dans l'espace 3D
def calculer_distance(coord1, coord2):
    x1, y1, z1 = coord1
    x2, y2, z2 = coord2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

# Chemin vers le fichier CSV
satellite_file = 'satellites.csv'

# Initialiser les variables pour le satellite le plus proche
satellite_proche = None
distance_minimale = float('inf')

try:
    # Vérifier si le fichier existe
    if not os.path.exists(satellite_file):
        raise FileNotFoundError(f"Le fichier {satellite_file} n'existe pas.")
    
    # Ouvrir et lire le fichier CSV
    with open(satellite_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Ignorer la première ligne (en-têtes)
        
        for row in reader:
            try:
                # Extraire les coordonnées et l'information sur l'antenne d'émission
                x, y, z = float(row[2]), float(row[3]), float(row[4])
                emission_antenna = row[5].lower() == 'true'
                
                # Si nous ne voulons considérer que les satellites avec antenne d'émission
                if not emission_antenna:
                    continue
                
                # Calculer la distance entre ce satellite et la navette
                distance = calculer_distance(navette_coords, (x, y, z))
                
                # Si ce satellite est plus proche, mettre à jour la distance minimale
                if distance < distance_minimale:
                    distance_minimale = distance
                    satellite_proche = row[1]  # Le nom du satellite
            except (IndexError, ValueError) as e:
                print(f"Erreur lors du traitement d'une ligne: {e}")
                continue

    # Afficher le satellite le plus proche
    if satellite_proche:
        print(f"Le satellite le plus proche de la navette est : {satellite_proche}")
        print(f"Distance : {distance_minimale:.2f} kilomètres")
    else:
        print("Aucun satellite trouvé dans le fichier ou répondant aux critères.")

except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(f"Une erreur inattendue s'est produite: {e}")