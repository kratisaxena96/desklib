# app/context_processor.py

from typing import Dict, Any

from django.conf import settings

def from_settings(request) -> Dict[str, Any]:
    return {
        attr: getattr(settings, attr, None)
        for attr in (
            'LANGUAGE_CODE',
        )
    }