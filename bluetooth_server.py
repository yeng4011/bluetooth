import asyncio
from bleak import BleakClient, BleakScanner
from Crypto.Cipher import AES
import base64

# 確保輸出到終端的編碼是 UTF-8
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

# AES加密需要的填充函數
def pad(text):
    while len(text) % 16 != 0:
        text += ' '
    return text

# AES加密函數
def encrypt(text, key):
    text = pad(text)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_text = base64.b64encode(cipher.encrypt(text.encode('utf-8')))
    return encrypted_text

# 掃描BLE設備
async def scan():
    devices = await BleakScanner.discover()
    for d in devices:
        print(f"{d.address}: {d.name}")
    return devices

# 連接並發送加密數據
async def connect_and_send(address, key, message):
    async with BleakClient(address) as client:
        services = await client.get_services()
        for service in services:
            print(f"{service.uuid}: {service.handle}")

        SERVICE_UUID = "D1A7623F-E295-4369-817E-CAA555FA093A"
        CHARACTERISTIC_UUID = "6E4B3168-87D9-462A-B0A1-EC9E656AFCC6"

        # 加密消息
        encrypted_message = encrypt(message, key)

        # 發送加密數據
        await client.write_gatt_char(CHARACTERISTIC_UUID, encrypted_message)
        print("已發送加密數據")

async def main():
    key = b'1234567891234567'  # AES 密鑰，必須是16、24或32字節長
    address = "F4:BE:EC:0A:8A:0E"  # 替換為實際設備地址
    message = "一口炸雞一口可樂"  # 要發送的原始消息

    devices = await scan()

    # 假設你選擇第一個設備
    if devices:
        await connect_and_send(devices[0].address, key, message)
    else:
        print("未找到藍牙設備")

if __name__ == "__main__":
    asyncio.run(main())