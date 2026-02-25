# backups/views.py
import os
import pickle
import subprocess
import zipfile
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.urls import reverse

from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from usuario.permisos import rol_requerido, SOLO_ADMIN


# ─────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────
SCOPES     = ['https://www.googleapis.com/auth/drive.file']
TOKEN_PATH = settings.GOOGLE_DRIVE_TOKEN_PATH
CREDS_PATH = settings.GOOGLE_OAUTH_CREDS_PATH


def _get_credentials():
    """Retorna las credenciales guardadas si existen y son válidas."""
    if not os.path.exists(TOKEN_PATH):
        return None
    with open(TOKEN_PATH, 'rb') as f:
        creds = pickle.load(f)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_PATH, 'wb') as f:
            pickle.dump(creds, f)
    return creds if creds.valid else None


def _esta_autenticado():
    """Comprueba si ya hay un token válido guardado."""
    return _get_credentials() is not None


# ─────────────────────────────────────────────
# VISTA PRINCIPAL — Página de backups
# Solo accesible para Administradores
# ─────────────────────────────────────────────
@rol_requerido(*SOLO_ADMIN)
def realizar_copia_seguridad(request):
    autenticado = _esta_autenticado()

    if request.method == "POST":
        creds = _get_credentials()

        if not creds:
            return redirect(reverse('apl:backups:google_auth'))

        db_config      = settings.DATABASES['default']
        MYSQLDUMP_EXE  = settings.MYSQLDUMP_PATH
        PARENT_FOLDER_ID = settings.GOOGLE_DRIVE_FOLDER_ID

        timestamp   = datetime.now().strftime("%Y-%m-%d_%H-%M")
        nombre_base = f"backup_db_{timestamp}"
        CARPETA_TEMP = os.path.join(settings.BASE_DIR, 'backups', 'temp')
        os.makedirs(CARPETA_TEMP, exist_ok=True)

        ruta_sql = os.path.join(CARPETA_TEMP, f"{nombre_base}.sql")
        ruta_zip = os.path.join(CARPETA_TEMP, f"{nombre_base}.zip")

        try:
            os.environ['MYSQL_PWD'] = str(db_config['PASSWORD'])
            comando = [
                MYSQLDUMP_EXE,
                '-u', db_config['USER'],
                '-h', db_config.get('HOST', 'localhost'),
                db_config['NAME'],
                '--result-file=' + ruta_sql
            ]
            subprocess.run(comando, check=True, shell=True)

            with zipfile.ZipFile(ruta_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(ruta_sql, arcname=os.path.basename(ruta_sql))

            service = build('drive', 'v3', credentials=creds)
            file_metadata = {
                'name': os.path.basename(ruta_zip),
                'parents': [PARENT_FOLDER_ID]
            }
            media = MediaFileUpload(ruta_zip, mimetype='application/zip')
            service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

            messages.success(request, "¡Copia de seguridad enviada con éxito a Google Drive!")

        except Exception as e:
            messages.error(request, f"Error detallado: {str(e)}")

        finally:
            if os.path.exists(ruta_sql):
                try:
                    os.remove(ruta_sql)
                except Exception:
                    pass
            if os.path.exists(ruta_zip):
                try:
                    os.remove(ruta_zip)
                except Exception:
                    pass

        return redirect('apl:backups:generar_backup')

    return render(request, 'modulos/backups.html', {'autenticado': autenticado})


# ─────────────────────────────────────────────
# VISTA — Inicia el flujo OAuth2 con Google
# Solo accesible para Administradores
# ─────────────────────────────────────────────
@rol_requerido(*SOLO_ADMIN)
def google_auth(request):
    flow = Flow.from_client_secrets_file(
        CREDS_PATH,
        scopes=SCOPES,
        redirect_uri=request.build_absolute_uri(reverse('apl:backups:google_callback'))
    )
    auth_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    request.session['oauth_state'] = state
    return redirect(auth_url)


# ─────────────────────────────────────────────
# VISTA — Callback que Google llama tras autenticarse
# Solo accesible para Administradores
# ─────────────────────────────────────────────
@rol_requerido(*SOLO_ADMIN)
def google_callback(request):
    state = request.session.get('oauth_state')

    flow = Flow.from_client_secrets_file(
        CREDS_PATH,
        scopes=SCOPES,
        state=state,
        redirect_uri=request.build_absolute_uri(reverse('apl:backups:google_callback'))
    )

    flow.fetch_token(authorization_response=request.build_absolute_uri())
    creds = flow.credentials

    with open(TOKEN_PATH, 'wb') as f:
        pickle.dump(creds, f)

    messages.success(request, "✅ Cuenta de Google vinculada correctamente.")
    return redirect('apl:backups:generar_backup')


# ── SOLO PARA DESARROLLO LOCAL (HTTP) ──
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'