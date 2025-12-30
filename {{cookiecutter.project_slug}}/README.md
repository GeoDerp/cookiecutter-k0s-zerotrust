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

## Adding User Applications

You can add applications to the cluster in two ways: using the scaffold script or manually.

### Option 1: Scaffold Script (Recommended)
The included script generates a Deployment, Service, and Linkerd Policy adhering to Zero Trust principles.

```bash
./scripts/scaffold-service.py
```
1. Follow the interactive prompts.
2. The manifests are generated in `gitops/apps/<service-name>`.
3. Commit and push the changes:
   ```bash
   git add gitops/apps/
   git commit -m "Add new service: <service-name>"
   git push
   ```

### Option 2: Manual Addition
1. Create a new directory for your application: `gitops/apps/<my-app>`.
2. Add your Kubernetes manifests (Deployment, Service, Ingress, etc.) to this directory.
3. Commit and push to the repository.

### How ArgoCD Syncs
The `workloads` Application in ArgoCD watches the `gitops/apps` directory recursively.
- **Automatic Sync**: ArgoCD is configured to automatically sync changes (approx. every 3 minutes).
- **Manual Sync**: You can trigger a sync immediately via the ArgoCD UI or CLI.

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
