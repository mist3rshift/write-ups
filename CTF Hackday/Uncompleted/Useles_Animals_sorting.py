import socket
import base64
from PIL import Image
from io import BytesIO

# Définition des détails de connexion
host = 'challenges.hackday.fr'
port = 51259

# Création de l'objet socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # Connexion à l'hôte et au port spécifiés
    client_socket.connect((host, port))
    print(f"Connexion établie avec {host} sur le port {port}")

    # Réception et affichage de la réponse initiale
    response = client_socket.recv(1024)
    response_text = response.decode()
    print("Réponse reçue :", response_text)

    # Attendre un peu avant d'envoyer un "Enter" (simulé par \n)
    print("Envoi de la touche 'Enter'...")
    client_socket.send(b'\n')  # Envoi du caractère de nouvelle ligne (Enter)

    # Réception de la réponse suivante
    response = client_socket.recv(4096*100)
    response_text = response.decode()
    print("Réponse reçue après avoir envoyé 'Enter' :", response_text)
    image_data = base64.b64decode(response_text)

    # Convertir les données en une image
    image = Image.open(BytesIO(image_data))

    # Afficher l'image
    image.show()

except socket.error as e:
    print(f"Erreur de connexion : {e}")

finally:
    # Fermeture de la connexion
    client_socket.close()
