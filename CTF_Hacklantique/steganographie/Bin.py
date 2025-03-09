from PIL import Image

# Charger l'image
image_path = "solved.bmp"  # Remplace par le bon chemin
image = Image.open(image_path)

# Convertir en noir et blanc (binaire)
gray_image = image.convert("1")

# Récupérer la première ligne de pixels
width, height = gray_image.size
pixels = list(gray_image.getdata())[:width]

# Convertir en binaire (0 = noir, 1 = blanc)
binary_string = "".join(["0" if pixel == 255 else "1" for pixel in pixels])

# Afficher la chaîne binaire brute (utile pour debug)
print("Binaire extrait :")
print(binary_string)

# Vérifier que la longueur est un multiple de 8
if len(binary_string) % 8 != 0:
    print("\n⚠️ Attention : La longueur du message binaire n'est pas un multiple de 8, il peut y avoir un décalage !")

# Convertir en texte ASCII
decoded_text = "".join(
    chr(int(binary_string[i:i+8], 2)) 
    for i in range(0, len(binary_string) - (len(binary_string) % 8), 8)
)

# Nettoyer le texte (enlever les caractères non imprimables)
decoded_text_clean = "".join(c if 32 <= ord(c) <= 126 else "�" for c in decoded_text)

print("\nMessage caché (nettoyé) :", decoded_text_clean)
