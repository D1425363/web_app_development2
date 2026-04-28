import os
from flask import Flask
from .routes.recipe_routes import recipe_bp
from .models.db import init_db

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # 基礎設定
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊 Blueprints
    app.register_blueprint(recipe_bp)

    return app
