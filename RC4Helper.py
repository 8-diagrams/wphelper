import base64

def rc4_core(data, key):
    """RC4 algorithm"""

    key = [ord(c) for c in key]  # or `key = key.encode()` for python3

    x = 0
    box = list(range(256))
    for i in range(256):
        x = (x + int(box[i]) + int(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]

    x = y = 0
    out = []
    for char in data:
        code = ord(char)
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        k = (box[x] + box[y]) % 256
        out.append(chr(code ^ box[k]))

    return ''.join(out)

def rc4encrypt2(data, key):
    raw = rc4_core( data, key )
    return str( base64.b64encode( raw.encode() )  )

def rc4decrypt2(b64data, key):
    raw = str( base64.b64decode( b64data )  )
    return rc4_core( raw, key )

def rc4encrypt(data, key):
    raw = rc4_core( data, key )
    return str( base64.b64encode( raw.encode() ), 'utf-8' )

def rc4decrypt(b64data, key):
    raw = str( base64.b64decode( b64data ) , 'utf-8' )
    return rc4_core( raw, key )


def crypt_random(raw, yourkey):
    import random
    random_s = 'DJNKSU' + str(random.randint(10000000000, 99999999999))
    
    data = rc4encrypt(random_s+":"+raw, yourkey)
    return data 

def decypt_random( enc , yourkey):
    
    data = rc4decrypt(enc, yourkey)
    #print( data )
    if data.startswith("DJNKSU"):
        return data.split(":")[1]

def decypt_random_ex(enc, yourkey):
    data = rc4decrypt(enc, yourkey)
    #print( data )
    if data.startswith("DJNKSU"):
        return data[len("DJNKSU"+'10000000000')+1:]
    return ""

import hashlib

def hash_me(s):
    m=hashlib.md5()
    m.update(s.encode('utf8'))
    return m.hexdigest()

def _getDecPass(pwd, dkey='defaults'):
    from Crypto.Cipher import ARC4 as rc4cipher
    import base64
    d = rc4cipher.new( bytes(dkey, encoding='utf8') )
    rawb = base64.b64decode( pwd )
    return d.decrypt(  rawb ).decode('utf8')


if __name__ == "__main__":
    cipher = rc4encrypt("", "mykey")
    print ( f"{[cipher]}" )

    bb = '112233'
    enc = rc4encrypt(bb, 'defaults')
    b2 = rc4decrypt( enc, 'defaults')
    print("enc:" , enc)
    print("b2:" , b2)
    raw = rc4decrypt2( '+Q+EH/FE' , "defaults" )
    
    print ( raw )
    
    raw2 = _getDecPass( '+Q+EH/NG' )

    print ( raw2 )