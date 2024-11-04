from app.core.load_config import load_config_model, load_github_config
from app.service.service import Service

if __name__ == "__main__":
    cfg = load_config_model()
    github_cfg = load_github_config()

    service = Service(cfg, github_cfg)
    service.AppGenerator.create_app()
