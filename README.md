# Cookiecutter k0s Zero Trust

A cookiecutter template for deploying a Zero Trust k0s cluster with GitOps, Linkerd, SPIRE, and more.

## Usage

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Run cookiecutter:
   ```bash
   uv run cookiecutter .
   ```

## Features

- **Single Node k0s**: Hardened configuration.
- **GitOps**: ArgoCD pre-configured with App of Apps.
- **Service Mesh**: Linkerd with SPIRE mTLS.
- **Security**: OPA Gatekeeper, Sealed Secrets.
- **Observability**: Falco, Osquery/Uptycs support.
