from hashlib import sha256
import base64

def generate_nk_combo(name,key):
    if '#' in name:
        return '0'
    return f"{name}#{key}"

def hash_key(key):
    return base64.urlsafe_b64encode(bytes.fromhex(sha256(key.encode('utf-8')).hexdigest())).decode()

