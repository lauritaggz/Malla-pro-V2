import base64
import json
from functools import lru_cache
from pathlib import Path

import firebase_admin
from firebase_admin import credentials

from app.core.config import get_settings

BACKEND_DIR = Path(__file__).resolve().parents[2]


@lru_cache
def get_firebase_app() -> firebase_admin.App:
    """Initialize firebase_admin once, lazily. JSON (base64) has priority over the file path."""
    settings = get_settings()
    if settings.firebase_credentials_json:
        info = json.loads(base64.b64decode(settings.firebase_credentials_json))
        cred = credentials.Certificate(info)
    else:
        path = Path(settings.firebase_credentials_path)
        if not path.is_absolute():
            path = BACKEND_DIR / path
        cred = credentials.Certificate(str(path))
    return firebase_admin.initialize_app(cred)
