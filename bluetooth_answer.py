import base64
from Crypto.Cipher import AES
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
# AES解密函數
def decrypt(encrypted_text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_text = cipher.decrypt(base64.b64decode(encrypted_text))
    return decrypted_text.strip().decode('utf-8')

# 假設從藍牙外設讀取到的加密數據
encrypted_data_from_ble = b'cqs7+i2gdm5yQIGST39nNK6PoKID9AuajKDIZ33LA0Y='

# AES密鑰，必須是16、24或32字節長
key = b'1234567891234567'

# 解密
decrypted_data = decrypt(encrypted_data_from_ble, key)
print("解密後的數據:", decrypted_data)