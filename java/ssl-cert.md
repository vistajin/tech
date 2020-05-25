### Terms

- SSL - Secure Sockets Layer, RFC6101, deprecated

- TLS - Transport Layer Security (TLS1.3) RFC8446

- X.509- is a **standard** defining the format of [public key certificates](https://en.wikipedia.org/wiki/Public_key_certificate)., use RSA key

- CA - Certificate Authority （受到广泛信任的机构）

- PEM - Privacy Enhanced Mail, BASE64

  TO view PEM:

  ```
  openssl x509 -in certificate.pem -text -noout
  ```

- DER - Distinguished  Encoded Rules, Binary format

  ```
  openssl x509 -in certificate.der -inform der -text -noout
  ```

- CRT - Certificate, can be DER or PEM, X.509
- CER - Still it is certificate, most for windows, X.509
- KEY - store public or private key, not a X.509 certificate
- CSR - Certificate Signing Request, not a certificate, it is a request to get certificate, generated together with the private key.
- PFX / P12 - processor of PKCS#12, for windows, contains CRT + Private Key with password to extract it
- PCKS - Public Key Cryptography **Standards**, RSA  (p1, p8, p12)

- EV SSL - Extended V





### SSL Handshake

<img src="/home/vistajin/tech/java/ssl-handshake.png" style="zoom:80%;" />