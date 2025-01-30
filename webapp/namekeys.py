from hashlib import sha256
import base64
import re

def generate_nk_combo(name,key):
    if '#' in name:
        return '0'
    if '\x06' in name:
        return '0'
    if '\x06' in key:
        return '0'
    return f"{name}#{key}"

def decouple_nk_to_name(inp):
    name = re.search(r'.*(?=#)',inp).group()
    return f"{name}"

def hash_nk(nk):
    return base64.urlsafe_b64encode(bytes.fromhex(sha256(nk.encode('utf-8')).hexdigest())).decode()

def hash_nk_trunc(nk):
    out_trunc = base64.urlsafe_b64encode(bytes.fromhex(sha256(nk.encode('utf-8')).hexdigest())).decode()[:10]
    return f"{out_trunc}.."
