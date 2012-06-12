import glob
import time
import random
import string
import gc

available = {}
try:
    import M2Crypto.EVP
except ImportError:
    available["m2crypto"] = False
else:
    available["m2crypto"] = True
try:
    import Crypto.Hash.SHA
    import Crypto.PublicKey.RSA
    import Crypto.Signature.PKCS1_v1_5
except ImportError:
    available["crypto"] = False
else:
    available["crypto"] = True


def get_signature_m2crypto(private_key, message):
    key = M2Crypto.EVP.load_key_string(private_key)
    key.reset_context(md='sha1')
    key.sign_init()
    key.sign_update(bytes(message))
    return key.sign_final()


def get_signature_crypto(private_key, message):
    key = Crypto.PublicKey.RSA.importKey(private_key)
    signer = Crypto.Signature.PKCS1_v1_5.new(key)
    sha1_hash = Crypto.Hash.SHA.new()
    sha1_hash.update(bytes(message))
    return signer.sign(sha1_hash)


def get_random_string(length):
    pool = string.letters + string.digits
    return "".join(random.choice(pool) for i in range(length))


get_signature = {
        "m2crypto": get_signature_m2crypto,
        "crypto": get_signature_crypto,
        }


def main():
    for key_file in glob.glob("*.pem"):
        with open(key_file, "r") as f:
            private_key = f.read()

        # Check that the signatures match.
        results = []
        for name, func in get_signature.items():
            if not available[name]:
                continue
            results.append((name, func(private_key, "foo bar")))
        print "{} using {}:".format(key_file, ", ".join(r[0] for r in results))
        signatures = dict((r[1], True) for r in results).keys()
        if len(signatures) == 1:
            print "  EQUAL"
        else:
            print "  NOT EQUAL"

        # Simple benchmark.
        iters = 500
        s = get_random_string(500)
        for name, func in get_signature.items():
            if not available[name]:
                continue
            print "running {} iterations of {}".format(iters, name)
            gc.disable()
            tic = time.time()
            for i in range(iters):
                func(private_key, s)
            toc = time.time()
            gc.enable()
            print "  took {:.3f}s".format(toc - tic)

        print


if __name__ == "__main__":
    main()
