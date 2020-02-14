export http_proxy=http://127.0.0.1:8087
export https_proxy=http://127.0.0.1:8087

* fatal: unable to access 'https://github.com/vistajin/tech.git/': server certificate verification failed. CAfile: /etc/ssl/certs/ca-certificates.crt CRLfile: none

```sh
git config --global http.sslverify "false"
```


* error: RPC failed; curl 56 GnuTLS recv error (-110): The TLS connection was non-properly terminated.

```

```
