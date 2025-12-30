from pytest_cookies.plugin import Cookies

def test_bake_project(cookies):
    result = cookies.bake(extra_context={"project_name": "My K0s Cluster"})
    
    assert result.exit_code == 0
    assert result.exception is None
    
    assert result.project_path.name == "my-k0s-cluster"
    assert result.project_path.is_dir()

    # Check scripts
    assert (result.project_path / "scripts" / "install-k0s.sh").exists()
    assert (result.project_path / "scripts" / "bootstrap-argocd.sh").exists()
    assert (result.project_path / "scripts" / "scaffold-service.py").exists()

    # Check GitOps structure
    assert (result.project_path / "gitops" / "bootstrap" / "root-app.yaml").exists()
    
    # Check content
    root_app = (result.project_path / "gitops" / "bootstrap" / "root-app.yaml").read_text()
    assert "repoURL: https://github.com/myorg/my-k0s-cluster.git" in root_app
    
    install_script = (result.project_path / "scripts" / "install-k0s.sh").read_text()
    assert "k0s install controller" in install_script

def test_scaffold_script(cookies):
    result = cookies.bake()
    script = result.project_path / "scripts" / "scaffold-service.py"
    assert script.exists()
    assert "Linkerd Policy" in script.read_text()
