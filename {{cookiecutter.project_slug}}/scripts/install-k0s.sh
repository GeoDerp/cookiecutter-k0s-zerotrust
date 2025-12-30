#!/bin/bash
set -e

echo ">>> Installing k0s Single Node Controller..."

# 2.3 CNI Considerations for Service Mesh
echo ">>> Verifying IP forwarding..."
if [[ $(sysctl -n net.ipv4.ip_forward) != "1" ]]; then
    echo "Enabling net.ipv4.ip_forward..."
    echo "net.ipv4.ip_forward = 1" | sudo tee /etc/sysctl.d/99-k0s-forwarding.conf
    sudo sysctl -p /etc/sysctl.d/99-k0s-forwarding.conf
fi

# Install k0s
export K0S_VERSION="{{ cookiecutter.k0s_version }}"
curl --proto '=https' --tlsv1.2 -sSf https://get.k0s.sh | sudo sh

# 2.2 Hardening the API Server (Configuration)
sudo mkdir -p /etc/k0s
if [ ! -f /etc/k0s/k0s.yaml ]; then
    echo ">>> Generating default k0s config..."
    sudo k0s config create > k0s_default.yaml
    
    # We would modify k0s.yaml here for anonymous-auth=false if not default
    # For now, just moving it
    sudo mv k0s_default.yaml /etc/k0s/k0s.yaml
fi

# Install as systemd service
# --single: Configures the node as a single node cluster
# --enable-worker: Activates the worker profile
# --no-taints: Allows workloads on controller
echo ">>> Installing k0s service..."
sudo k0s install controller --single --enable-worker --no-taints

# Start service
echo ">>> Starting k0s..."
sudo k0s start

# Wait for k0s to be up
echo ">>> Waiting for k0s to be ready..."
sleep 10
sudo k0s status

echo ">>> Generating admin kubeconfig..."
mkdir -p $HOME/.kube
sudo k0s kubeconfig admin > $HOME/.kube/config
chmod 600 $HOME/.kube/config

echo ">>> Installation complete. You can now use 'kubectl'."
kubectl get nodes
