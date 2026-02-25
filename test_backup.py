import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuracion.settings')
django.setup()

from django.core.management import call_command

try:
    print("--- Iniciando prueba forzada ---")
    call_command('dbbackup', skip_checks=True, verbosity=3)
    print("--- Proceso terminado ---")
except Exception as e:
    print(f"EL ERROR OCULTO ES: {e}")