import numpy as np
from sympy import Matrix
import re

def read_alphabet_mapping(content):
    """Lit le contenu du fichier alphabet et retourne le dictionnaire de mappage"""
    # Évaluation sécurisée du texte pour obtenir le dictionnaire
    alphabet_dict = eval(content)
    
    # Créer un mapping inverse (valeur -> caractère)
    inverse_mapping = {v: k for k, v in alphabet_dict.items()}
    
    # Créer des listes ordonnées pour faciliter la conversion
    ordered_chars = [inverse_mapping[i] for i in range(len(alphabet_dict))]
    
    return alphabet_dict, ordered_chars, inverse_mapping

def map_text_to_numbers(text, alphabet_dict):
    """Convertit le texte en valeurs numériques selon l'alphabet"""
    return [alphabet_dict[char] for char in text]

def map_numbers_to_text(numbers, inv_mapping):
    """Convertit les valeurs numériques en texte selon le mapping inverse"""
    return ''.join(inv_mapping[num % len(inv_mapping)] for num in numbers)

def chunks(lst, n):
    """Divise une liste en groupes de taille n"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def extend_to_multiple(numbers, size, padding_value=0):
    """Étend la liste pour qu'elle soit un multiple exact de la taille donnée"""
    if len(numbers) % size != 0:
        padding_needed = size - (len(numbers) % size)
        return numbers + [padding_value] * padding_needed
    return numbers

def decrypt_hill(ciphertext_nums, key_matrix, mod_value):
    """Déchiffre un texte en utilisant la clé inverse et le chiffrement de Hill"""
    # Calculer l'inverse de la matrice clé modulo mod_value
    key_matrix_mod = Matrix(key_matrix) % mod_value
    key_inverse = Matrix(key_matrix_mod).inv_mod(mod_value)
    key_inverse_np = np.array(key_inverse.tolist(), dtype=int)
    
    # Traiter le texte par blocs de taille key_size
    key_size = len(key_matrix)
    result = []
    
    for block in chunks(ciphertext_nums, key_size):
        if len(block) < key_size:
            block = extend_to_multiple(block, key_size)
        
        # Multiplier le bloc par la matrice inverse
        decrypted_block = np.dot(key_inverse_np, block) % mod_value
        result.extend(decrypted_block)
    
    return result

def find_key_with_known_text(ciphertext, known_plain_text, alphabet_dict, inv_mapping, mod_value):
    """
    Essaie de trouver la clé en utilisant une portion connue du texte en clair.
    Pour une matrice 3x3, nous avons besoin d'au moins 3 triplets (9 caractères).
    """
    known_plain = map_text_to_numbers(known_plain_text, alphabet_dict)
    matrix_size = 3  # Nous savons que c'est une matrice 3x3
    
    # Nous avons besoin d'au moins matrix_size triplets
    if len(known_plain) < matrix_size * matrix_size:
        print(f"Le texte en clair connu est trop court. Nous avons besoin d'au moins {matrix_size * matrix_size} caractères.")
        return None
    
    # Vérifier toutes les positions possibles du texte connu dans le message chiffré
    for start_pos in range(len(ciphertext) - len(known_plain) + 1):
        # Extraire la portion correspondante du texte chiffré
        cipher_segment = ciphertext[start_pos:start_pos + len(known_plain)]
        cipher_nums = map_text_to_numbers(cipher_segment, alphabet_dict)
        
        # Diviser en triplets (pour une matrice 3x3)
        plain_triplets = list(chunks(known_plain, matrix_size))
        cipher_triplets = list(chunks(cipher_nums, matrix_size))
        
        # S'assurer que nous avons assez de triplets complets
        if len(plain_triplets) < matrix_size or len(cipher_triplets) < matrix_size:
            continue
        
        try:
            # Construire des matrices à partir des triplets
            P = np.array([plain_triplets[i] for i in range(matrix_size)]).T
            C = np.array([cipher_triplets[i] for i in range(matrix_size)]).T
            
            # Calculer la matrice clé: K = C * P^(-1) mod N
            P_matrix = Matrix(P)
            try:
                P_inv = P_matrix.inv_mod(mod_value)
            except:
                # Si la matrice n'est pas inversible modulo mod_value, passer à la position suivante
                continue
                
            C_matrix = Matrix(C)
            
            # Multiplier C par P^(-1)
            K = (C_matrix * P_inv) % mod_value
            K_np = np.array(K.tolist(), dtype=int)
            
            # Vérifier si cette clé fonctionne en déchiffrant un segment plus long
            test_length = min(30, len(ciphertext) - start_pos)
            test_cipher = ciphertext[start_pos:start_pos + test_length]
            test_cipher_nums = map_text_to_numbers(test_cipher, alphabet_dict)
            
            decrypted_test = decrypt_hill(test_cipher_nums, K_np, mod_value)
            decrypted_text = map_numbers_to_text(decrypted_test, inv_mapping)
            
            # Vérifier si le début du texte déchiffré correspond au texte en clair connu
            if known_plain_text in decrypted_text:
                print(f"Clé potentielle trouvée à la position {start_pos}:")
                print(K_np)
                
                # Essayer de déchiffrer tout le message
                all_cipher_nums = map_text_to_numbers(ciphertext, alphabet_dict)
                all_decrypted = decrypt_hill(all_cipher_nums, K_np, mod_value)
                all_text = map_numbers_to_text(all_decrypted, inv_mapping)
                
                if known_plain_text in all_text:
                    print(f"La clé fonctionne pour tout le message!")
                    return K_np, all_text
        
        except Exception as e:
            # Ignorer les erreurs et continuer avec la position suivante
            continue
    
    # Si nous arrivons ici, nous n'avons pas trouvé de clé fonctionnelle
    print("Aucune clé n'a été trouvée avec le texte en clair connu.")
    return None, None

def sliding_window_search(ciphertext, known_text, alphabet_dict, inv_mapping, mod_value):
    """
    Recherche le texte connu en utilisant une fenêtre glissante sur le texte chiffré.
    Cela peut aider à identifier où le texte connu pourrait se trouver.
    """
    known_nums = map_text_to_numbers(known_text, alphabet_dict)
    matrix_size = 3
    
    # Tester différentes positions de départ
    for i in range(0, len(ciphertext) - len(known_text) + 1, matrix_size):
        # Essayer de trouver une clé qui déchiffre une fenêtre du texte chiffré 
        # en "HACKLANTIQUE{"
        cipher_window = ciphertext[i:i + len(known_text) + matrix_size]  # Ajouter quelques caractères supplémentaires
        cipher_nums = map_text_to_numbers(cipher_window, alphabet_dict)
        
        # Essayer différentes matrices clés simples
        for det in range(1, min(100, mod_value)):
            if np.gcd(det, mod_value) != 1:
                continue  # Le déterminant doit être premier avec mod_value
                
            # Essayer une matrice triangulaire supérieure avec déterminant det
            for a in range(1, min(20, mod_value)):
                if a * a * a % mod_value == det:  # Si a³ ≡ det (mod N)
                    key = np.array([
                        [a, 0, 0],
                        [0, a, 0],
                        [0, 0, a]
                    ])
                    
                    try:
                        decrypted = decrypt_hill(cipher_nums, key, mod_value)
                        decrypted_text = map_numbers_to_text(decrypted, inv_mapping)
                        
                        if known_text.lower() in decrypted_text.lower():
                            print(f"Clé potentielle trouvée à la position {i} avec matrice:")
                            print(key)
                            print(f"Texte déchiffré: {decrypted_text}")
                            
                            # Tester sur tout le texte
                            all_cipher_nums = map_text_to_numbers(ciphertext, alphabet_dict)
                            all_decrypted = decrypt_hill(all_cipher_nums, key, mod_value)
                            all_text = map_numbers_to_text(all_decrypted, inv_mapping)
                            
                            return key, all_text
                    except:
                        continue
    
    # Si nous avons atteint ce point, essayer d'autres types de matrices
    print("Essai de matrices plus complexes...")
    
    # Essayer quelques valeurs simples pour identifier des clés potentielles
    for a in range(1, 10):
        for b in range(1, 10):
            for c in range(1, 10):
                if np.gcd(a * b * c, mod_value) != 1:
                    continue
                
                key = np.array([
                    [a, b, c],
                    [c, a, b],
                    [b, c, a]
                ])
                
                try:
                    # Test sur un segment du texte chiffré
                    test_segment = ciphertext[:30]  # Prendre les 30 premiers caractères
                    test_nums = map_text_to_numbers(test_segment, alphabet_dict)
                    decrypted = decrypt_hill(test_nums, key, mod_value)
                    decrypted_text = map_numbers_to_text(decrypted, inv_mapping)
                    
                    if known_text[:5].lower() in decrypted_text.lower():  # Vérifier les 5 premiers caractères
                        print(f"Clé potentielle trouvée avec matrice:")
                        print(key)
                        print(f"Début du texte déchiffré: {decrypted_text}")
                        
                        # Tester sur tout le texte
                        all_cipher_nums = map_text_to_numbers(ciphertext, alphabet_dict)
                        all_decrypted = decrypt_hill(all_cipher_nums, key, mod_value)
                        all_text = map_numbers_to_text(all_decrypted, inv_mapping)
                        
                        return key, all_text
                except:
                    continue
    
    return None, None

def extract_flag(text):
    """Extrait le flag au format HACKLANTIQUE{...} du texte déchiffré"""
    pattern = r'HACKLANTIQUE\{[^}]*\}'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(0)
    return "Flag non trouvé"

# Données d'entrée
alphabet_content = """
{
    'A': 10, 'B': 32, 'C': 44, 'D': 9, 'E': 61, 'F': 37, 'G': 20, 'H': 12, 'I': 5, 'J': 6, 'K': 67,
    'L': 27, 'M': 30, 'N': 45, 'O': 54, 'P': 8, 'Q': 11, 'R': 15, 'S': 23, 'T': 7, 'U': 49, 'V': 43,
    'W': 19, 'X': 51, 'Y': 31, 'Z': 0, 'a': 26, 'b': 59, 'c': 63, 'd': 2, 'e': 58, 'f': 42, 'g': 62,
    'h': 68, 'i': 46, 'j': 28, 'k': 47, 'l': 64, 'm': 16, 'n': 41, 'o': 50, 'p': 39, 'q': 33, 'r': 48,
    's': 60, 't': 52, 'u': 57, 'v': 1, 'w': 24, 'x': 38, 'y': 13, 'z': 55, 'é': 21, 'ê': 35, 'è': 65,
    'ô': 3, 'à': 17, ' ': 22, ',': 29, '.': 4, '!': 25, '{': 53, '}': 14, '€': 18, '#': 34, '*': 36,
    '"': 56, "'": 66, '_': 40
}
"""

ciphertext = """Eebô#b"h_uy!DoUgé"Frêê PVàhwàZ YQikwôfaR iéWèGNdèC*ELTmX ELT{JQSVGèhVD€CIl,CAy.SqVmh.ôànUI{kàSr'gMGVULMyfR€SHB€Gk,eSjcl€#uPeNAoV,bBitDycYTnéGLxd'!}*KBèY#àêu*KB.sSt}èôfaN Kxsq.wê#uP_hAfênêéngdIlyeLjXosSR igdIUeNWjPôxlTéLvNôBG*VGAKNyj{q"iC #tOzD#uP"h_uy!J,aY'iwmZI,oyihgkgpRhèhVD€CSL_eKk ThLVfô#bN KgwêD'sMOSRp}h!LVnnRiI' cô#b!BA{J"DgaQmIT'Pe""bfrwjNnéGLxd#êHétàôLèO#fm},'V.ôYWNJè!hjAtêô_gISjYDQulWéWèbfr.X{ELTR.dEA",kIQQPMwaYgoh!L!{lRxhQàê BnqAZc}dEàHOi*gMGVULé!hirBe}o*KBYQEIRwa_cfVueMêVkNGWa"""

# Traitement
alphabet_dict, ordered_chars, inv_mapping = read_alphabet_mapping(alphabet_content)
mod_value = len(alphabet_dict)  # Taille de l'alphabet (69 caractères)
known_text = "HACKLANTIQUE{"  # Le texte connu qui doit être dans le message déchiffré

print(f"Recherche de la clé pour déchiffrer le message...")
print(f"Texte connu qui doit se trouver dans le message déchiffré: '{known_text}'")
print(f"Taille de l'alphabet: {mod_value} caractères")
print(f"Longueur du texte chiffré: {len(ciphertext)} caractères")

# Approche 1: Recherche avec texte connu
print("\n--- Approche 1: Recherche avec texte connu ---")
key_matrix, decrypted_text = find_key_with_known_text(ciphertext, known_text, alphabet_dict, inv_mapping, mod_value)

# Si l'approche 1 échoue, essayer l'approche 2
if key_matrix is None:
    print("\n--- Approche 2: Recherche par fenêtre glissante ---")
    key_matrix, decrypted_text = sliding_window_search(ciphertext, known_text, alphabet_dict, inv_mapping, mod_value)

# Si nous avons trouvé une clé
if key_matrix is not None and decrypted_text is not None:
    print("\n=== RÉSULTATS ===")
    print(f"Matrice clé trouvée:\n{key_matrix}")
    print(f"\nTexte déchiffré:\n{decrypted_text}")
    
    # Extraire le flag
    flag = extract_flag(decrypted_text)
    print(f"\nFlag extrait: {flag}")
else:
    # Essayer une autre approche: matrice identité multipliée par une valeur
    print("\n--- Approche 3: Essai avec matrices simples ---")
    
    for scalar in range(1, mod_value):
        if np.gcd(scalar, mod_value) != 1:
            continue  # Scalar doit être premier avec mod_value
            
        key = scalar * np.eye(3, dtype=int)
        
        try:
            # Test sur le début du texte
            test_cipher = ciphertext[:50]
            test_nums = map_text_to_numbers(test_cipher, alphabet_dict)
            decrypted = decrypt_hill(test_nums, key, mod_value)
            decrypted_text = map_numbers_to_text(decrypted, inv_mapping)
            
            if known_text[:5].lower() in decrypted_text.lower():
                print(f"Clé trouvée avec scalaire {scalar}:")
                print(key)
                
                # Déchiffrer tout le texte
                all_nums = map_text_to_numbers(ciphertext, alphabet_dict)
                all_decrypted = decrypt_hill(all_nums, key, mod_value)
                all_text = map_numbers_to_text(all_decrypted, inv_mapping)
                
                print(f"\nTexte déchiffré:\n{all_text}")
                flag = extract_flag(all_text)
                print(f"\nFlag extrait: {flag}")
                break
        except:
            continue
    else:
        print("Aucune clé n'a été trouvée avec toutes les approches.")
        print("Vous pourriez avoir besoin d'une approche plus spécialisée ou d'informations supplémentaires.")