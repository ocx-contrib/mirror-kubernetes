# mirror-kubernetes

OCX mirrors for [Kubernetes](https://kubernetes.io) tooling. One repository,
one spec directory per package.

| Package | Spec | Publishes to | Announced as | Upstream SPDX |
|---|---|---|---|---|
| [kubectl](https://kubernetes.io/docs/reference/kubectl/) | [`kubectl/mirror.yml`](kubectl/mirror.yml) | `ghcr.io/ocx-contrib/kubernetes/kubectl` | `ocx.sh/kubernetes/kubectl` | `Apache-2.0` |

Each upstream release is discovered, re-bundled, smoke-tested per
`(version, platform)` and only then pushed with cascade tags, after which the
result is announced into the OCX index.

kubernetes/kubernetes GitHub releases carry **no binary assets** — binaries
ship from [dl.k8s.io](https://dl.k8s.io), the official release CDN. So this
mirror runs a small [`kubectl/scripts/generate.py`](kubectl/scripts/generate.py)
that lists versions from GitHub releases and constructs the documented
dl.k8s.io URL per platform, emitting a `url_index` JSON document. The script
uses [`ocx-mirror-sdk`](https://pypi.org/project/ocx-mirror-sdk/) from PyPI,
pinned to a floating patch via PEP 723 inline metadata, and runs under the
`uv` pinned in [`ocx.toml`](ocx.toml).

## Layout

```
mirror-base.yml         repo-wide policy every spec inherits via `extends:`
kubectl/
├── mirror.yml          the spec — never at the repo root
├── metadata.json       bundle interface
├── CATALOG.md          → ocx package describe
├── logo.svg / logo.png describe assets, 512px PNG
├── scripts/generate.py the url_index generator
└── tests/smoke.star    Starlark smoke test
```

`LICENSE` and `NOTICE.md` are shared at the root. Logos and generators are
**not** — each package carries its own inside its spec directory, because that
is what the workflow's `<pkg>/**` path trigger watches.

⚠️ `extends:` is a **shallow** merge of top-level keys. This repo deliberately
keeps `platforms:` **out of the base** (the mirror-kitware model): the
container matrix is downstream of a per-package libc measurement, and the k8s
release binaries are not uniform — kubectl measures static, while kubelet
(should it ever be added) is the classic dynamically-linked suspect. Each spec
carries its own measured `platforms:` block next to its own evidence comment.

## Platforms

`kubectl` publishes six platform entries: both Linux arches, both macOS arches
and both Windows arches. kubectl is pure-Go, built `CGO_ENABLED=0` upstream —
byte-measured on both Linux binaries from dl.k8s.io, neither carries a
`PT_INTERP` — so both Linux keys are **bare** and the `alpine:3.20` container
leg is what turns that claim into evidence. The measurement is recorded above
the `assets:` block in [`kubectl/mirror.yml`](kubectl/mirror.yml).

The version floor is `1.36.0` (owner decision 2026-08-03 — the current stable
line; older lines stay with upstream / OS package managers). All in-range
versions ship all six platforms; every constructed URL was HEAD-verified at
authoring.

## Editing

| File | Edit | Regenerate after |
|------|------|------------------|
| `mirror-base.yml`, `kubectl/mirror.yml` | hand | yes — see below |
| `kubectl/{metadata.json,CATALOG.md,logo.*}` | hand | — |
| `kubectl/scripts/generate.py` | hand | — |
| `kubectl/tests/smoke.star` | hand | — |
| `.github/workflows/*.yml` | **generated — never hand-edit** | re-run when a spec changes |

```bash
ocx-mirror package pipeline generate ci --spec kubectl/mirror.yml
```

**Name every spec.** `--spec` *appends* rather than replaces, so a command
naming a subset silently stops rendering the rest while staying green — and
the drift guard reds on a generated workflow the current spec set no longer
produces.

`verify-generated.yml` exits 65 on drift. If a generated workflow is wrong,
the spec or the renderer template is wrong — fix it there and regenerate.

Run `direnv allow` once to put the pinned toolchain on `PATH`, and invoke
`ocx-mirror` directly — never `ocx run -- ocx-mirror`, which pins
`OCX_BINARY_PIN` to the bootstrap `ocx` and false-reds the nested push.

## The binaries claim

dl.k8s.io ships kubectl as a **raw binary** — no archive, no `bin/` — so the
bundle's PATH is a bare `${installPath}` and `bin_scan` stays off (the scan
gate rejects a bare PATH). `kubectl/metadata.json` hand-declares
`binaries: ["kubectl"]`, which also makes `prepare` chmod the download to
0755 — the bare CDN download carries no exec bit.

## Required secrets

| Secret | Use |
|--------|-----|
| `OCX_ANNOUNCE_TOKEN` | opens the index pull request from the `ocx-contrib/index` fork |
| `OCX_MIRROR_DISCORD_HOOK` | notify-stage Discord webhook URL |

(Inherited from the `ocx-contrib` org with visibility ALL. GHCR pushes use the
run's own `GITHUB_TOKEN` — no registry secret needed.)

## License

Apache-2.0 — see [`LICENSE`](LICENSE). Upstream assets are out of scope; each
package's redistribution license is recorded in [`NOTICE.md`](NOTICE.md).
