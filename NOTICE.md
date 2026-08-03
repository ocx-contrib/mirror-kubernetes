# NOTICE

This repository packages and redistributes upstream software published by the
[Kubernetes project](https://kubernetes.io) (a CNCF project). The Apache-2.0
license in [`LICENSE`](LICENSE) covers the OCX pipeline files authored here.
It does **not** cover any upstream-derived asset — each package's
redistributed bytes carry their own license, recorded below.

| Package | GHCR path | Upstream SPDX |
|---|---|---|
| `kubectl` | `ghcr.io/ocx-contrib/kubernetes/kubectl` | `Apache-2.0` |

---

## `kubectl`

Upstream: <https://kubernetes.io> (source: <https://github.com/kubernetes/kubernetes>)
Published to `ghcr.io/ocx-contrib/kubernetes/kubectl`.

| Component | SPDX | Holder |
|---|---|---|
| kubectl binary | **Apache-2.0** | Copyright The Kubernetes Authors |

Permissive; redistribution in binary form is granted under the Apache License
2.0, the terms of which are those of
<https://github.com/kubernetes/kubernetes/blob/master/LICENSE>. Binaries are
fetched byte-for-byte from dl.k8s.io, the official Kubernetes release CDN.

Kubernetes® and the Kubernetes logo are registered trademarks of The Linux
Foundation, used for catalog identification under nominative fair use. The
logo shipped with this package is the upstream Kubernetes logomark
(`logo/logo.svg` from kubernetes/kubernetes), reproduced for catalog
identification only. The marks remain the property of their respective owners
and no endorsement is implied.

No modifications are made to any upstream artifact in this repository; they
are republished byte-for-byte inside an OCX bundle.
