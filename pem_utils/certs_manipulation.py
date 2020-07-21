"""
Implement --dumpvalues --createpriv --createpub --generate
"""
from gmpy2 import invert 
from Crypto.PublicKey import RSA

"""
Takes a path to a public/private key and dumps its values using pycryptodome RSA methods
the values will also be returned in a list: [n, e[, p, q, d, dp, dq, pinv, qinv]]
"""
def dump_values_from_pem(path: str) -> list:

    print("[+] Importing Key")
    try:
        keyfile = open(path, 'rb')
        key = RSA.importKey(keyfile.read())
    except Exception as e:
        print("certs_manipulation.py:dump_values_from_pem ->", e)
    print("[+] Key imported\n")

    res = []

    print("[*] n: ", key.n)
    print("[*] e: ", key.e)

    res += [key.n, key.e]

    if key.has_private():
        print("[*] p: ", key.p)
        print("[*] q: ", key.q)
        print("[*] d: ", key.d)
        print()

        dp = key.d%(key.p-1)
        dq = key.d%(key.q-1)
        pinv = int(invert(key.p, key.q))
        qinv = int(invert(key.q, key.p))

        print("[#] dp: ", dp)
        print("[#] dq: ", dq)
        print("[#] pinv: ", pinv)
        print("[#] qinv: ", qinv)

        res += [key.p, key.q, key.d, dp, dq, pinv, qinv]
    
    return res

    