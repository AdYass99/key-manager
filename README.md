# Key Manager

Este proyecto es una aplicación Flask para gestionar contraseñas de forma segura. Permite a los usuarios agregar, ver, copiar y eliminar contraseñas, además de generar contraseñas aleatorias.

## Project Structure

```
key-manager
├── app
│   ├── __init__.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── home.py
│   │   ├── passwords.py
│   │   └── autentification.py
│   ├── templates
│   │   ├── index.html
│   │   ├── config.html
│   │   ├── search.html
│   │   └── skeleton.html
│   ├── static
│   │   └── styles.css
│   └── database.py
├── instance
│   └── passwords.db
├── requirements.txt
├── run.py
├── Dockerfile
├── docker-compose.yaml
├── .gitignore
└── README.md
```

## Setup Instructions

### 1. Clonar el repositorio:
```bash
git clone <repository-url>
cd key-manager
```

### 2. Crear un entorno virtual:
```bash
python -m venv venv
```

### 3. Activar el entorno virtual:
- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 4. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

### 5. Ejecutar la aplicación:
```bash
python run.py
```

### 6. Acceder a la aplicación:
Abre tu navegador y navega a `http://127.0.0.1:5000/`.

---

## Funcionalidades

### Rutas principales:
- **`/`**: Página de inicio para autenticación.
- **`/view`**: Página para buscar y ver contraseñas.
- **`/config`**: Página para agregar, eliminar y generar contraseñas.
- **`/copy`**: Copia una contraseña al portapapeles.
- **`/delete`**: Elimina una contraseña específica.
- **`/generate`**: Genera una contraseña aleatoria.

### Operaciones:
1. **Agregar una contraseña**:
   - Navega a `/config`.
   - Ingresa un nombre de usuario y una contraseña.
   - Haz clic en el botón `➕`.

2. **Buscar una contraseña**:
   - Navega a `/view`.
   - Usa el campo de búsqueda para filtrar por nombre de usuario.

3. **Copiar una contraseña**:
   - Haz clic en el botón `📋` junto a la contraseña que deseas copiar.

4. **Eliminar una contraseña**:
   - Haz clic en el botón `🗑️` junto a la contraseña que deseas eliminar.

5. **Generar una contraseña aleatoria**:
   - Navega a `/config` y haz clic en el botón `⚙️`.

---

## Uso con Docker

### Construir la imagen:
```bash
docker build -t key-manager .
```

### Ejecutar el contenedor:
```bash
docker-compose up
```

### Acceder a la aplicación:
Abre tu navegador y navega a `http://127.0.0.1:5000/`.

---

## Seguridad

- Las contraseñas se almacenan cifradas utilizando AES-GCM.
- La clave maestra se protege mediante hashing con Argon2.
- Asegúrate de cambiar la clave secreta (`SECRET_KEY`) en producción.
- Usa HTTPS para proteger la comunicación entre el cliente y el servidor.

---

## Dependencias

- **Flask**: Framework web.
- **pycryptodomex**: Para cifrado y descifrado de contraseñas.
- **argon2-cffi**: Para hashing seguro de contraseñas.
- **pyperclip**: Para copiar contraseñas al portapapeles.

---

## Notas adicionales

- La base de datos SQLite se encuentra en el directorio `instance/passwords.db`.
- Asegúrate de que el directorio `instance` exista antes de ejecutar la aplicación.
- Para restablecer la base de datos, elimina el archivo `passwords.db` y reinicia la aplicación.