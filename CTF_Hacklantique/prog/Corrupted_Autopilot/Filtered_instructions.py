def filtrer_LRF(chaine):
    # On filtre les caractères 'L', 'R', 'F' dans la chaîne
    result = ''.join([char for char in chaine if char in 'LRF'])
    return result

with open('input.txt', 'r') as f:
    content = f.read()
    result = filtrer_LRF(content)
    print(result)
    