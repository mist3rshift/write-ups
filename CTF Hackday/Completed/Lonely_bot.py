import socket
import hashlib
import base64
import random
from deep_translator import GoogleTranslator

# Dictionnaire pour convertir les noms de langues en codes de langue
language_codes = {
    'english': 'en',
    'german': 'de',
    'french': 'fr',
    'spanish': 'es',
    'italian': 'it',
    'portuguese': 'pt',
    'chinese': 'zh',
    'russian': 'ru',
    'japanese': 'ja',
    'arabic': 'ar',
    'korean': 'ko'
}

# Fonction pour traduire un mot
def translate_word(word, language_name):
    # Obtenir le code de la langue à partir du nom
    target_language = language_codes.get(language_name.lower())
    
    if target_language:
        # Traduction du mot
        translated_word = GoogleTranslator(source='auto', target=target_language).translate(word)
        return translated_word
    else:
        return "Langue non prise en charge."


def determine_response(opponent_first_move):
    # Détermine le premier coup qui bat le coup de l'adversaire
    if opponent_first_move == "R":
        first_move = "P"  # Paper bat Rock
    elif opponent_first_move == "P":
        first_move = "S"  # Scissors bat Paper
    elif opponent_first_move == "S":
        first_move = "R"  # Rock bat Scissors
    else:
        raise ValueError("Invalid opponent move!")

    # Détermine un deuxième coup aléatoire pour couvrir plus de scénarios
    second_move = random.choice(["R", "P", "S"])

    return f"{first_move},{second_move}"

print("determine reponse :", determine_response('P'))
print("determine reponse :", determine_response('S'))
print("determine reponse :", determine_response('R'))
def detect_encoding(base_question):
    """
    Détecte si une chaîne est encodée en Base32, Base64 ou Base85.
    """
    # Tester dans un ordre strict pour éviter les faux positifs
    try:
        # Test Base64
        base64.b64decode(base_question, validate=True)
        return "base64"
    except Exception:
        pass

    try:
        # Test Base32
        base64.b32decode(base_question, casefold=True)
        return "base32"
    except Exception:
        pass

    try:
        # Test Base85
        base64.b85decode(base_question)
        return "base85"
    except Exception:
        pass

    return "Unknown or not encoded"

# Exemple d'utilisation
inputs = [
    "SSBrbm93IG1hbnkgZW5jb2RpbmcgYmFzZXMsIGJ1dCB3aGljaCBvbmUgaSdtIHVzaW5nLi4uPyAod3JpdGUgeW91ciBhbnN3ZXIgaW4gbG93ZXJjYXNlIGxpa2UgJ2Jhc2U2NCcp",
    "JEQGW3TPO4QG2YLOPEQGK3TDN5SGS3THEBRGC43FOMWCAYTVOQQHO2DJMNUCA33OMUQGSJ3NEB2XG2LOM4XC4LR7EAUHO4TJORSSA6LPOVZCAYLOON3WK4RANFXCA3DPO5SXEY3BONSSA3DJNNSSAJ3CMFZWKNRUE4UQ====",
    "Ng!)(Z+9SVVQzUKWo~0{WNB_^AYx&2WpgYbVs&&NcW7y2XdrKHWguxMZ6I}XX>MmOE-pVHD0gycbY&oUZ*_7YVQzDGWpW^CZXj%LcV%*8VRL05Y-wv{ASYsBb7eL(Cn*"
]

for i, input_str in enumerate(inputs, 1):
    result = detect_encoding(input_str)
    print(f"Input {i}: {result}")

# Définition des détails de connexion
host = 'challenges.hackday.fr'
port = 41525

# Création de l'objet socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # Connexion à l'hôte et au port spécifiés
    client_socket.connect((host, port))
    print(f"Connexion établie avec {host} sur le port {port}")

    response = client_socket.recv(1024)
    response_text = response.decode()
    print("Réponse reçue :", response_text)
    

    response = client_socket.recv(1024)
    response_text = response.decode()
    print("Réponse reçue :", response_text)

    first_response_text = 'yes'
    client_socket.sendall(first_response_text.encode())

    response = client_socket.recv(1024)
    response_text = response.decode()
    print("Réponse reçue :", response_text)

    response = client_socket.recv(1024)
    response_text = response.decode()
    print("Réponse reçue :", response_text)

    second_response = 'mistershift'
    client_socket.sendall(second_response.encode())
    response = client_socket.recv(1024)
    response_text = response.decode()
    print("Réponse reçue :", response_text)

    response = client_socket.recv(1024)
    question_tempeture = response.decode()
    print("Réponse reçue :", question_tempeture)
    if 'Fahrenheit' in question_tempeture:
        tempeture_value = '1709'
    elif 'Celsius' in  question_tempeture :
        tempeture_value = '932'
    else :
        tempeture_value = '1205'
    print('Answer :', tempeture_value)
    client_socket.sendall(tempeture_value.encode())

    response = client_socket.recv(1024)
    response_text = response.decode()
    print("Réponse reçue :", response_text)
    response = client_socket.recv(1024)
    question_history = response.decode()
    print("Réponse reçue :", question_history)
    if 'electric' in question_history :
        history_value = '1879'
    elif 'vapor' in question_history:
        history_value = '1804'
    elif 'diesel' in question_history:
        history_value = '1903'
    else :
        history_value = '1979'
    print('Answer :', history_value)
    client_socket.sendall(history_value.encode())

    response = client_socket.recv(1024)
    response_text = response.decode()
    print("Réponse reçue :", response_text)


    response = client_socket.recv(1024)
    base_question = response.decode()
    print("Réponse reçue :", base_question)
    cleaned_data = base_question.strip()
    base_value = detect_encoding(cleaned_data)

    print('Answer :', base_value)
    client_socket.sendall(base_value.encode())

    response = client_socket.recv(1024)
    response_text = response.decode()
    print("Réponse reçue :", response_text)

    response = client_socket.recv(1024)
    hash_response = response.decode()
    print("Réponse reçue :", hash_response)

    all_data_response = second_response+','+tempeture_value+','+history_value+','+base_value
    if 'md5' in hash_response:
        
        hash_response = hashlib.md5(all_data_response.encode()).hexdigest()
        print('MD5 :', hash_response)
    elif 'sha256' in hash_response:
        hash_response = hashlib.sha256(all_data_response.encode()).hexdigest()
        print('sha256 :', hash_response)
    elif 'sha512' in hash_response:
        hash_response = hashlib.sha512(all_data_response.encode()).hexdigest()
        print('sha512 :', hash_response)
    else:
        hash_response = hashlib.sha1(all_data_response.encode()).hexdigest()
        print('sha1 :', hash_response)
    print('Answer :', hash_response)
    client_socket.sendall(hash_response.encode())

    response = client_socket.recv(1024)
    response_text = response.decode()
    print("Réponse reçue :", response_text)

    response = client_socket.recv(1024)
    response_text = response.decode()
    print("Réponse reçue :", response_text)
    #-------------------------------------------------------------------------------------------------------------------------
    # Part 2 
    print("Part 2\n\n")
    #-------------------------------------------------------------------------------------------------------------------------
    response = client_socket.recv(1024)
    response_text = response.decode()
    print("Réponse reçue :", response_text)
    
    
    while True:
        response = client_socket.recv(1024)
        paper_scissors = response.decode().strip()
        print("Réponse reçue :", paper_scissors)

        if "My first move is" in paper_scissors:
            # Extraire le coup de l'adversaire
            if 'P' in paper_scissors:
                opponent_first_move = 'P'
            elif 'S' in paper_scissors:
                opponent_first_move = 'S'
            else:
                opponent_first_move = 'R'
            print("opponent fisrt move", opponent_first_move)
            # Déterminer la réponse optimale
            paper_scissors_value = determine_response(opponent_first_move)
            print("Answer :", paper_scissors_value)

            # Envoyer la réponse
            client_socket.sendall(paper_scissors_value.encode())
        else:
            # Si aucune phrase correspondante n'est trouvée, fin de la boucle
            print("Fin du jeu ou réponse inattendue.")
            break

    response = client_socket.recv(1024)
    response_text = response.decode()
    print("Réponse reçue :", response_text)
    def guess_the_number():
        low = 0
        high = 20
        tries = 5

        while tries > 0:
            # Devine le milieu de l'intervalle
            guess = (low + high) // 2
            print(f"Guessing: {guess}")
            client_socket.sendall(str(guess).encode())  # Envoie la supposition

            # Reçoit la réponse
            response = client_socket.recv(1024).decode().strip()
            print("Réponse reçue :", response)

            if "found" in response:
                print("Trouvé ! Le nombre était :", guess)
                break
            elif "bigger" in response:
                low = guess + 1  # Réduire l'intervalle inférieur
            elif "smaller" in response:
                high = guess - 1  # Réduire l'intervalle supérieur
            else:
                print("Réponse inattendue :", response)
                break

            tries -= 1  # Décrémenter les essais restants

        if tries == 0:
            print("Échec ! Nombre d'essais épuisé.")

    # Exemple d'utilisation (simule la connexion à un serveur réel)
    guess_the_number()


    response = client_socket.recv(1024)
    traduction = response.decode()
    print("Réponse reçue :", traduction)
    parts = traduction.split(" ")
    word = parts[7].strip("/")  
    language = parts[9].strip("/")

    response = client_socket.recv(1024)
    response_text = response.decode()
    print("Réponse reçue :", response_text)

except socket.error as e:
    print(f"Erreur de connexion : {e}")

finally:
    # Fermeture de la connexion
    client_socket.close()
