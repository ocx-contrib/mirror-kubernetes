# kubectl/tests/smoke.star — stable across upstream Kubernetes releases.
# Asserts behavior/contract (exit codes, version shape, a computed client-side
# manifest), never upstream-controlled prose. kubectl needs no cluster for any
# of this: `--client` and `--dry-run=client` are fully offline.
KUBECTL = "kubectl.exe" if ocx.target_platform.os == ocx.os.Windows else "kubectl"

# Hermetic env: HOME (and its Windows spelling USERPROFILE) point at scratch so
# kubectl's config discovery never touches the real user home; KUBECONFIG names
# a scratch path that does not exist — client-only operations must not need one.
ocx.mkdir("home")
home = ocx.scratch_root + "/home"
k_env = {
    "HOME": home,
    "USERPROFILE": home,
    "KUBECONFIG": ocx.scratch_root + "/kubeconfig",
}

# Tier 1 + 2: liveness + version SHAPE from structured output — the JSON field
# is the contract; prose around it is not.
r_version = ocx.run(KUBECTL, "version", "--client", "--output", "json", env=k_env)
expect.ok(r_version)
expect.matches(r_version.stdout, r"\"gitVersion\": \"v\d+\.\d+\.\d+\"")

# Tier 3: functional behavior, no cluster — a client-side dry-run COMPUTES a
# ConfigMap manifest from the literal. The token appears in the emitted JSON
# only if kubectl actually built the object; an echoed argv could not produce
# the surrounding structure.
r_dry = ocx.run(
    KUBECTL,
    "create", "configmap", "ocx-smoke",
    "--from-literal=token=ocx-kubectl-smoke-91",
    "--dry-run=client", "--output", "json",
    env=k_env,
)
expect.ok(r_dry)
expect.contains(r_dry.stdout, "\"kind\": \"ConfigMap\"")
expect.contains(r_dry.stdout, "\"token\": \"ocx-kubectl-smoke-91\"")
