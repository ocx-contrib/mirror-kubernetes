# /// script
# requires-python = ">=3.13"
# dependencies = ["ocx-mirror-sdk~=0.6.0"]
# ///
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 The OCX Authors

"""Generate url_index JSON for kubectl from dl.k8s.io.

kubernetes/kubernetes GitHub releases carry NO binary assets — binaries ship
from dl.k8s.io, the official release CDN, under the documented scheme

    https://dl.k8s.io/release/v<ver>/bin/<os>/<arch>/kubectl[.exe]

(the same URL the upstream install docs tell users to curl). So this generator
uses GitHub releases only as the VERSION LIST and constructs the download URL
per platform. Asset names are synthesised as `kubectl-<os>-<arch>[.exe]` —
upstream serves every platform's binary under the same basename, and the
mirror's `assets:` patterns need one distinct name per platform.

The tag regex drops rc/alpha/beta tags (`v1.37.0-rc.1`); `include_prereleases`
is off as a second belt. Every constructed URL for every in-range version was
HEAD-verified 200 at authoring; a future gap fails that platform's prepare
download loudly (exit 74) rather than passing silently.
"""

import re

from ocx_mirror_sdk import IndexBuilder, github

REPO = "kubernetes/kubernetes"
TAG_RE = re.compile(r"^v(?P<version>\d+\.\d+\.\d+)$")

# (os, arch) as dl.k8s.io spells them -> the six platforms kubectl ships for.
PLATFORMS = [
    ("linux", "amd64"),
    ("linux", "arm64"),
    ("darwin", "amd64"),
    ("darwin", "arm64"),
    ("windows", "amd64"),
    ("windows", "arm64"),
]


def main() -> None:
    index = IndexBuilder()
    for rel in github.list_releases(REPO, include_prereleases=False, include_drafts=False):
        m = TAG_RE.match(rel.tag_name)
        if not m:
            continue
        version = m.group("version")
        assets = {}
        for os_, arch in PLATFORMS:
            ext = ".exe" if os_ == "windows" else ""
            name = f"kubectl-{os_}-{arch}{ext}"
            assets[name] = f"https://dl.k8s.io/release/v{version}/bin/{os_}/{arch}/kubectl{ext}"
        index.add_version(version, assets=assets, prerelease=rel.prerelease)
    index.emit()


if __name__ == "__main__":
    main()
