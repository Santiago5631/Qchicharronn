import os
import pickle
import subprocess
import zipfile
from datetime import date
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.http import StreamingHttpResponse

from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from .models import RegistroBackup

if settings.DEBUG:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# ─────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────
SCOPES = ['https://www.googleapis.com/auth/drive.file']
TOKEN_PATH = settings.GOOGLE_DRIVE_TOKEN_PATH
CREDS_PATH = settings.GOOGLE_OAUTH_CREDS_PATH


def _get_credentials():
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
    return _get_credentials() is not None


# ─────────────────────────────────────────────
# VISTA: GENERAR COPIA (BACKUP)
# ─────────────────────────────────────────────
def realizar_copia_seguridad(request):
    autenticado = _esta_autenticado()

    # Backups del día actual para mostrar en la tabla
    backups_hoy = RegistroBackup.objects.filter(
        fecha_creacion__date=date.today()
    )

    if request.method == "POST":
        creds = _get_credentials()
        if not creds:
            return redirect(reverse('apl:backups:google_auth'))

        db_config = settings.DATABASES['default']
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        nombre_base = f"backup_qchicharron_{timestamp}"

        CARPETA_TEMP = os.path.join(settings.BASE_DIR, 'backups', 'temp')
        os.makedirs(CARPETA_TEMP, exist_ok=True)

        ruta_sql = os.path.join(CARPETA_TEMP, f"{nombre_base}.sql")
        ruta_zip = os.path.join(CARPETA_TEMP, f"{nombre_base}.zip")

        try:
            # 1. GENERAR SQL
            env = os.environ.copy()
            env['MYSQL_PWD'] = str(db_config['PASSWORD'])

            cmd_dump = (
                f"mysqldump -u {db_config['USER']} "
                f"-h {db_config.get('HOST', 'db')} "
                f"--skip-ssl "
                f"--add-drop-table --quick "
                f"{db_config['NAME']} > {ruta_sql}"
            )
            res = subprocess.run(cmd_dump, shell=True, capture_output=True, text=True, env=env)
            if res.returncode != 0:
                raise Exception(f"mysqldump falló: {res.stderr}")

            # 2. COMPRIMIR
            with zipfile.ZipFile(ruta_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(ruta_sql, arcname=f"{nombre_base}.sql")

            tamanio_kb = os.path.getsize(ruta_zip) // 1024

            # 3. SUBIR A DRIVE
            service = build('drive', 'v3', credentials=creds)
            file_metadata = {
                'name': os.path.basename(ruta_zip),
                'parents': [settings.GOOGLE_DRIVE_FOLDER_ID]
            }
            media = MediaFileUpload(ruta_zip, mimetype='application/zip')
            archivo_drive = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

            drive_file_id = archivo_drive.get('id', '')

            # 4. GUARDAR REGISTRO EN BASE DE DATOS
            RegistroBackup.objects.create(
                nombre_archivo=os.path.basename(ruta_zip),
                tamanio_kb=tamanio_kb,
                drive_file_id=drive_file_id,
                exitoso=True,
            )

            messages.success(request, "¡Copia de seguridad enviada a Google Drive con éxito!")

        except Exception as e:
            # Guardar registro del fallo también
            RegistroBackup.objects.create(
                nombre_archivo=f"{nombre_base}.zip",
                tamanio_kb=0,
                drive_file_id='',
                exitoso=False,
            )
            messages.error(request, f"Error al generar backup: {str(e)}")

        finally:
            for ruta in [ruta_sql, ruta_zip]:
                if os.path.exists(ruta):
                    try:
                        os.remove(ruta)
                    except Exception:
                        pass

        return redirect('apl:backups:generar_backup')

    return render(request, 'modulos/backups.html', {
        'autenticado': autenticado,
        'backups_hoy': backups_hoy,
    })


# ─────────────────────────────────────────────
# VISTA: DESCARGAR BACKUP DESDE DRIVE
# ─────────────────────────────────────────────
def descargar_backup(request, backup_id):
    try:
        registro = RegistroBackup.objects.get(id=backup_id)
        creds = _get_credentials()
        if not creds:
            messages.error(request, "No hay sesión de Google activa.")
            return redirect('apl:backups:generar_backup')

        service = build('drive', 'v3', credentials=creds)

        # Descargar el archivo desde Drive en memoria
        solicitud = service.files().get_media(fileId=registro.drive_file_id)

        import io
        buffer = io.BytesIO()
        descargador = MediaIoBaseDownload(buffer, solicitud)
        listo = False
        while not listo:
            _, listo = descargador.next_chunk()

        buffer.seek(0)

        response = StreamingHttpResponse(
            buffer,
            content_type='application/zip'
        )
        response['Content-Disposition'] = f'attachment; filename="{registro.nombre_archivo}"'
        return response

    except RegistroBackup.DoesNotExist:
        messages.error(request, "Backup no encontrado.")
        return redirect('apl:backups:generar_backup')
    except Exception as e:
        messages.error(request, f"Error al descargar: {str(e)}")
        return redirect('apl:backups:generar_backup')


# ─────────────────────────────────────────────
# VISTA: RESTAURAR COPIA (RESTORE)
# ─────────────────────────────────────────────
def restaurar_backup(request):
    if request.method == "POST" and request.FILES.get('archivo_backup'):
        archivo_subido = request.FILES['archivo_backup']
        db_config = settings.DATABASES['default']

        CARPETA_TEMP = os.path.join(settings.BASE_DIR, 'backups', 'temp')
        os.makedirs(CARPETA_TEMP, exist_ok=True)

        ruta_zip = os.path.join(CARPETA_TEMP, "restore_temp.zip")
        ruta_sql = os.path.join(CARPETA_TEMP, "restore_temp.sql")

        try:
            # 1. GUARDAR el ZIP subido
            with open(ruta_zip, 'wb') as f:
                for chunk in archivo_subido.chunks():
                    f.write(chunk)

            # 2. DESCOMPRIMIR con Python puro
            with zipfile.ZipFile(ruta_zip, 'r') as zipf:
                nombres = zipf.namelist()
                sql_dentro = next((n for n in nombres if n.endswith('.sql')), None)
                if not sql_dentro:
                    raise Exception("El ZIP no contiene ningún archivo .sql válido.")
                with zipf.open(sql_dentro) as origen, open(ruta_sql, 'wb') as destino:
                    destino.write(origen.read())

            # 3. RESTAURAR con mysql
            env = os.environ.copy()
            env['MYSQL_PWD'] = str(db_config['PASSWORD'])

            cmd_restore = (
                f"mysql -u {db_config['USER']} "
                f"-h {db_config.get('HOST', 'db')} "
                f"--skip-ssl "
                f"--protocol=tcp {db_config['NAME']} "
                f"< {ruta_sql}"
            )
            res = subprocess.run(cmd_restore, shell=True, capture_output=True, text=True, env=env)
            if res.returncode != 0:
                raise Exception(f"mysql falló: {res.stderr}")

            messages.success(request, "¡Base de datos restaurada correctamente!")

        except zipfile.BadZipFile:
            messages.error(request, "El archivo no es un ZIP válido. Descarga el backup desde la tabla e intenta de nuevo.")
        except Exception as e:
            messages.error(request, f"Error al restaurar: {str(e)}")

        finally:
            for ruta in [ruta_zip, ruta_sql]:
                if os.path.exists(ruta):
                    try:
                        os.remove(ruta)
                    except Exception:
                        pass

    return redirect('apl:backups:generar_backup')


# ─────────────────────────────────────────────
# VISTAS OAUTH2
# ─────────────────────────────────────────────
def google_auth(request):
    flow = Flow.from_client_secrets_file(
        CREDS_PATH, scopes=SCOPES,
        redirect_uri=request.build_absolute_uri(reverse('apl:backups:google_callback'))
    )
    auth_url, state = flow.authorization_url(access_type='offline', prompt='consent')
    request.session['oauth_state'] = state
    return redirect(auth_url)


def google_callback(request):
    state = request.session.get('oauth_state')
    flow = Flow.from_client_secrets_file(
        CREDS_PATH, scopes=SCOPES, state=state,
        redirect_uri=request.build_absolute_uri(reverse('apl:backups:google_callback'))
    )
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    with open(TOKEN_PATH, 'wb') as f:
        pickle.dump(flow.credentials, f)
    messages.success(request, "✅ Google Drive vinculado correctamente.")
    return redirect('apl:backups:generar_backup')