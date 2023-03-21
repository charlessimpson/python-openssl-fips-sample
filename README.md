Enabling FIPS mode in OpenSSL in Python
=======================================

This document describes how to enable FIPS mode in OpenSSL in Python. If you
don't have a compliance reason to enable FIPS mode, you probably shouldn't do
it.

The approach for setting FIPS varies depending on the version of OpenSSL Python
is linked against, but in both cases, we use Python's
[ctypes](https://python.readthedocs.io/en/stable/library/ctypes.html) to
interact directly with the OpenSSL library. Setting FIPS mode should be done as
early as possible in the exceution of the Python program before any
cryptographic operations are run.

All of this requires a FIPS-enabled build of OpenSSL. Red Hat's Universal Basic
Images serve as good demonstrators, but other distributions may also work.

To demonstrate that FIPS mode has been activated, we attempt to load a
non-compliant algorithm for a digest. First, observe that normally (in non-FIPS
mode) we can load the an MD5 hash:

```python
import hashlib

hashlib.new("md5")
```

OpenSSL 1.x
-----------

In OpenSSL 1.x, we can explicitly set FIPS mode using
[`FIPS_mode_set()`](https://wiki.openssl.org/index.php/FIPS_mode_set()):

```python
from ctypes import CDLL

# Might be "libcrypto.so.10" or some other name
libcrypto = CDLL("libcrypto.so.1.1")
assert libcrypto.FIPS_mode_set(1) != 0
assert libcrypto.FIPS_mode() == 1

import hashlib

# Expect this to fail with an error like:
# ValueError: [digital envelope routines: EVP_DigestInit_ex] disabled for FIPS
hashlib.new("md5")

# Expect this to succeed
hashlib.new("sha256")
```

OpenSSL 3.x
-----------

OpenSSL 3 completely changed its API for enabling FIPS mode. From OpenSSL's
[`fips_module` man
page](https://www.openssl.org/docs/man3.0/man7/fips_module.html):

> Note that the old functions `FIPS_mode()` and `FIPS_mode_set()` are no longer
> present so you must remove them from your application if you use them.

The easiest approach to enabling FIPS is to enable it system-wide, as described
in "Making all applications use the FIPS module by default". If, for whatever
reason you don't want to do that, we can follow the approach outlined in
"Programmatically loading the FIPS module (default library context)" using
`ctypes` like above.

```python
from ctypes import CDLL

libcrypto = CDLL("libcrypto.so.3")
assert libcrypto.OSSL_PROVIDER_load(None, b"fips") != 0
assert libcrypto.OSSL_PROVIDER_load(None, b"base") != 0
assert libcrypto.EVP_set_default_properties(None, b"fips=yes") == 1

import hashlib

# Expect this to fail with an error like:
# ValueError: unsupported hash type md5(in FIPS mode)
hashlib.new("md5")

# Expect this to succeed
hashlib.new("sha256")
```
