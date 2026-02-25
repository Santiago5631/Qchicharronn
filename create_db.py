import MySQLdb
from decouple import config

try:
    db = MySQLdb.connect(
        host=config('DB_HOST', default='localhost'),
        user=config('DB_USER', default='root'),
        passwd=config('DB_PASSWORD', default=''),
        port=int(config('DB_PORT', default=3306))
    )
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS qchicharron")
    print("Base de datos 'qchicharron' verificada/creada exitosamente.")
    db.close()
except Exception as e:
    print(f"Error al crear la base de datos: {e}")
