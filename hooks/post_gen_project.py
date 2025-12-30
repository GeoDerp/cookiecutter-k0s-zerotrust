import os
import sys

def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2    # copy R bits to X
    os.chmod(path, mode)

if __name__ == "__main__":
    scripts_dir = "scripts"
    
    if os.path.exists(scripts_dir):
        for root, dirs, files in os.walk(scripts_dir):
            for file in files:
                if file.endswith(".sh") or file.endswith(".py"):
                    make_executable(os.path.join(root, file))
    
    print(">>> K0s Zero Trust Project initialized!")
    print(">>> Next steps:")
    print("1. cd {{ cookiecutter.project_slug }}")
    print("2. ./scripts/install-k0s.sh")
    print("3. ./scripts/bootstrap-argocd.sh")
