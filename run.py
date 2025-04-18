"""
Este archivo es el punto de entrada para ejecutar la aplicación Flask.
Se encarga de crear la instancia de la aplicación y ejecutarla en el puerto 5000.
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
