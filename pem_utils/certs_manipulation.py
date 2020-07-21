"""
Implement --dumpvalues --createpriv --createpub --generate
"""
from gmpy2 import invert 
from Crypto.PublicKey import RSA

"""
Takes a path to a public/private key and dumps its values using pycryptodome RSA methods
"""
def dump_values_from_pem(path: str) -> None:

    try:
        keyfile = open(path, 'rb')
        key = RSA.importKey(keyfile.read())

        print("[+] Key imported")

        print("[*] n: ", key.n)
        print("[*] e:", key.e)

        if key.has_private():
            print("[*] p: ", key.p)
            print("[*] q: ", key.q)
            print("[*] d: ", key.d)
            print()
            print("[#] dp: ", key.d%(key.p-1))
            print("[#] dq: ", key.d%(key.q-1))
            print("[#] pinv: ", int(invert(key.p, key.q)))
            print("[#] qinv: ", int(invert(key.q, key.p)))
    except Exception as e:
        print("certs_manipulation.py:dump_values_from_pem ->", e)