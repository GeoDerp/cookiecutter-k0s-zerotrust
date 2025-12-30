#!/usr/bin/env python3
import os
import sys

def create_manifests(service_name, port, image):
    base_dir = f"gitops/apps/{service_name}"
    os.makedirs(base_dir, exist_ok=True)
    
    # Deployment
    with open(f"{base_dir}/deployment.yaml", "w") as f:
        f.write(f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {service_name}
  namespace: default
  labels:
    app: {service_name}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {service_name}
  template:
    metadata:
      labels:
        app: {service_name}
      annotations:
        linkerd.io/inject: enabled
    spec:
      containers:
      - name: {service_name}
        image: {image}
        ports:
        - containerPort: {port}
""")

    # Service
    with open(f"{base_dir}/service.yaml", "w") as f:
        f.write(f"""apiVersion: v1
kind: Service
metadata:
  name: {service_name}
  namespace: default
spec:
  selector:
    app: {service_name}
  ports:
  - port: {port}
    targetPort: {port}
""")

    # Linkerd Policy (Zero Trust)
    with open(f"{base_dir}/policy.yaml", "w") as f:
        f.write(f"""apiVersion: policy.linkerd.io/v1beta1
kind: Server
metadata:
  name: {service_name}-server
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: {service_name}
  port: {port}
  proxyProtocol: HTTP/1
---
apiVersion: policy.linkerd.io/v1alpha1
kind: AuthorizationPolicy
metadata:
  name: {service_name}-authz
  namespace: default
spec:
  targetRef:
    group: policy.linkerd.io
    kind: Server
    name: {service_name}-server
  requiredAuthenticationRefs:
  # Modify this to allow specific SPIFFE IDs
  # - kind: MeshTLSAuthentication
  #   name: ...
  - kind: NetworkAuthentication
    name: default-deny # Assume a default deny exists or list nothing to deny all
""")

    print(f"Created manifests in {base_dir}")

if __name__ == "__main__":
    print(">>> Scaffold New Microservice")
    name = input("Service Name: ")
    port = input("Port (e.g. 8080): ")
    image = input("Image (e.g. nginx:alpine): ")
    
    create_manifests(name, int(port), image)
    print("Don't forget to git add, commit and push!")
