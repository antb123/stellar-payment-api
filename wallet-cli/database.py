import json
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from settings import DATABASE_PATH


def write(key, data):
    with open('database.bin', 'wb') as file:
        file.write(encrypt(key.encode(), json.dumps(data).encode()))


def read(key):
    with open('database.bin', 'rb') as file:
        return json.loads(decrypt(key.encode(), file.read()).decode())


def encrypt(key: bytes, source: bytes):
    """ Code based on https://stackoverflow.com/a/44212550/3705710 """
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    return IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt


def decrypt(key: bytes, source: bytes):
    """ Code based on https://stackoverflow.com/a/44212550/3705710 """
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding")
    return data[:-padding]  # remove the padding
