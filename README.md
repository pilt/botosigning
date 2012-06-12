Experiments with signing using [PyCrypto][pycrypto] and [M2Crypto][m2crypto].
Should be compatible with [Boto][boto]'s signing of CloudFront URLs.

## Example run

### Specs

Hardware:

* 1.7 GHz Intel Core i5
* 4 GB 1333 MHz DDR3

Python:

    Python 2.7.2 (default, Dec 30 2011, 18:21:22) 
    [GCC 4.2.1 (Based on Apple Inc. build 5658) (LLVM build 2336.1.00)] on darwin

### Results

    $ python sign.py
    rsa1024.pem using m2crypto, crypto:
      EQUAL
    running 500 iterations of m2crypto
      took 1.146s
    running 500 iterations of crypto
      took 2.682s

    rsa2048.pem using m2crypto, crypto:
      EQUAL
    running 500 iterations of m2crypto
      took 5.531s
    running 500 iterations of crypto
      took 10.623s

## Known issues

Signatures differ if non-ascii letters are included.

[pycrypto]: https://www.dlitz.net/software/pycrypto/
[m2crypto]: http://sandbox.rulemaker.net/ngps/m2/
[boto]: https://github.com/boto/boto
