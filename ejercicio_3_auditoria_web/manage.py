# mypy: ignore-errors
"""
NOTA TÉCNICA DE ARQUITECTURA (Micro-servidor Django Autónomo):
Además de los módulos solicitados (auditoria_emisiones.py, test_emisiones.py,
views.py y templates/sustentabilidad/panel.html), se incluye este script para
permitir visualizar el panel web en http://127.0.0.1:8000/ con un solo comando.
"""

import os
import sys
from pathlib import Path
from django.conf import settings
from django.core.management import execute_from_command_line
from django.urls import path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="ecotech-evaluacion-tecnica-secret-key",
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=["*"],
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [BASE_DIR / "templates"],
                "APP_DIRS": True,
            }
        ],
    )

from views import vista_panel_sustentabilidad  # noqa: E402

urlpatterns = [
    path("", vista_panel_sustentabilidad, name="panel_sustentabilidad"),
]

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "__main__")
    execute_from_command_line(sys.argv)