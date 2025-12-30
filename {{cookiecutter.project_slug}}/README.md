# {{ cookiecutter.project_name }}

A Zero Trust k0s cluster managed by ArgoCD and Linkerd.

## Prerequisites

- A Linux Node (e.g. Raspberry Pi, VM, Bare Metal)
- `curl`, `git`, `sudo`
- `kubectl` (optional, but recommended)

## Quick Start

### 1. Install k0s
Run the installation script to set up the single-node controller and verify networking requirements.

```bash
./scripts/install-k0s.sh
```

### 2. Bootstrap GitOps
Initialize ArgoCD and apply the "App of Apps".

```bash
./scripts/bootstrap-argocd.sh
```

### 3. Add a Service
Use the helper script to scaffold a new microservice with Zero Trust policies (Linkerd injected + Default Deny).

```bash
./scripts/scaffold-service.py
```
Follow the prompts, then commit the generated files to Git. ArgoCD will automatically sync them (after you push and ArgoCD detects the change).

## Architecture

- **Control Plane**: k0s (Single Node Controller+Worker)
- **GitOps**: ArgoCD (App of Apps Pattern)
- **Service Mesh**: Linkerd
- **Identity**: SPIFFE/SPIRE (Workload Identity)
- **Policy**: OPA Gatekeeper
- **Observability**: Falco

## Directory Structure

- `gitops/bootstrap`: The entry point for ArgoCD.
- `gitops/components`: Reusable infrastructure components.
- `gitops/apps`: User workloads.
- `scripts`: Helper scripts for lifecycle management.
