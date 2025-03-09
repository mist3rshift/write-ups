#3nohtyp vne/nib/rsu/!
#-*- 8-ftu :gnidoc -*- 
import sys
import time

REPEAT_STR = "YOU ARE ALONE"                                #BURP

ENCRYPTED_DATA_BYTES = [
    0x3d,0x6f,0x51,0x66,0x4c,0x46,0x44,0x57,           #BURP
    0x7a,0x49,0x47,0x63,0x77,0x6f,0x55,0x4d,
    0x31,0x4e,0x30,0x65,0x50,0x56,0x55,0x51,                       #BURP
    0x54,0x52,0x45,0x57,0x4c,0x5a,0x56,0x56,
    0x4e,0x74,0x6b,0x55
]


def line_key_present():                    #BURP
    try:
        with open(sys.argv[0], 'r', encoding='utf-8') as f:    #BuRP
            for line in f:
                if "DO_NOT_REMOVE_THIS_LINE" in line:                  #burp
                    return True                        #BuRp
    except:                                   #BURP
        pass
    return False


if line_key_present():
    final_value = 0
else:
    final_value = 10**21

hex_str = "".join(f"{b:02x}" for b in ENCRYPTED_DATA_BYTES)

# Convertir les octets en une chaîne hexadécimale
hex_str = "".join(f"{b:02x}" for b in ENCRYPTED_DATA_BYTES)

# Convertir la chaîne hexadécimale en texte lisible
decoded_str = bytes.fromhex(hex_str).decode('utf-8')

print("Decoded Data: ", decoded_str)

while True:
    time.sleep(0.02)
    if final_value > 10:
        print("AM I CRAZY: " + hex_str)
    else:
        print(REPEAT_STR)










    #BURP

















































#░▒▓█▓▒░░▒▓█▓▒░░▒▓███████▓▒░ 
#░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
#░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
#░▒▓████████▓▒░▒▓███████▓▒░  
#       ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
#       ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
#       ░▒▓█▓▒░░▒▓██████▓▒░  
                            
                            






















































    #BURP

