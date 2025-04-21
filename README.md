# Key Manager

**Key Manager** es una aplicación Flask diseñada para gestionar contraseñas de forma segura. Permite a múltiples usuarios registrarse, iniciar sesión y gestionar sus contraseñas personales. Las contraseñas se almacenan cifradas y protegidas mediante una clave maestra única para cada usuario.

---

## 🚀 Funcionalidades principales

1. **Registro de usuarios**: Los usuarios pueden registrarse con un nombre de usuario y una contraseña maestra.
2. **Inicio de sesión**: Los usuarios deben iniciar sesión para acceder a sus contraseñas.
3. **Gestión de contraseñas**:
   - Agregar nuevas contraseñas.
   - Buscar contraseñas por nombre de cuenta.
   - Copiar contraseñas al portapapeles.
   - Eliminar contraseñas.
   - Generar contraseñas aleatorias.
4. **Seguridad**:
   - Las contraseñas se cifran utilizando AES-GCM.
   - La clave maestra se protege mediante hashing con Argon2.
   - Protección contra ataques de fuerza bruta con bloqueos temporales.
5. **Sesiones independientes**: Cada usuario tiene su propia sesión activa.
6. **Soporte para HTTPS**: La aplicación puede ejecutarse con HTTPS para mayor seguridad.

---

## 📂 Estructura del proyecto

```plaintext
key-manager
├── app
│   ├── __init__.py               # Inicialización de la aplicación Flask
│   ├── db                        # Gestión de la base de datos SQLite
│   │   └── database.py
│   ├── routes                    # Rutas de la aplicación
│   │   ├── authentication.py     # Rutas para login, registro y logout
│   │   ├── main.py               # Ruta principal (home)
│   │   ├── passwords.py          # Rutas para gestionar contraseñas
│   ├── security                  # Funciones relacionadas con la seguridad
│   │   └── criptography.py       # Funciones de cifrado y descifrado
│   ├── templates                 # Plantillas HTML
│   │   ├── base.html             # Plantilla base
│   │   ├── index.html            # Página de inicio (login)
│   │   ├── register.html         # Página de registro
│   │   ├── config.html           # Página de configuración de contraseñas
│   │   ├── search.html           # Página de búsqueda de contraseñas
│   ├── static
│   │   └── styles.css            # Estilos CSS
│   └── utils.py                  # Funciones auxiliares (decoradores, etc.)
├── instance
│   └── passwords.db              # Base de datos SQLite
├── requirements.txt              # Dependencias del proyecto
├── run.py                        # Punto de entrada de la aplicación
├── generate_cert.py              # Generación de certificados (HTTPS)
├── Dockerfile                    # Configuración para Docker
├── docker-compose.yaml           # Configuración para Docker Compose
├── .gitignore                    # Archivos ignorados por Git
├── .dockerignore                 # Archivos ignorados por Docker
├── cert.pem                      # Certificado SSL autogenerado
├── key.pem                       # Clave privada SSL autogenerada
└── README.md                     # Documentación del proyecto
```

---

## 🛠️ Configuración del proyecto

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd key-manager
```

### 2. Crear un entorno virtual
```bash
python -m venv venv
```

### 3. Activar el entorno virtual
- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 4. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 5. Generar certificados SSL (opcional para HTTPS)
Si necesitas HTTPS, ejecuta el siguiente comando para generar un certificado SSL autogenerado:
```bash
python generate_cert.py
```

Esto generará los archivos `cert.pem` y `key.pem`.

### 6. Ejecutar la aplicación
```bash
python run.py
```

### 7. Acceder a la aplicación
- **HTTP**: `http://127.0.0.1:5000/`
- **HTTPS** (si configuraste certificados): `https://127.0.0.1:5000/`

---

## 🌐 Rutas principales

### **Autenticación**
- **`/login`**: Página de inicio de sesión.
- **`/register`**: Página de registro de nuevos usuarios.
- **`/logout`**: Cierra la sesión del usuario actual.

### **Gestión de contraseñas**
- **`/config`**: Página principal para agregar, eliminar y generar contraseñas.
- **`/view`**: Página para buscar y ver contraseñas.
- **`/copy`**: Copia una contraseña al portapapeles.
- **`/delete`**: Elimina una contraseña específica.
- **`/generate`**: Genera una contraseña aleatoria.
- **`/decrypt`**: Desencripta una contraseña (usada internamente por el frontend).

---

## 🛡️ Seguridad

1. **Cifrado de contraseñas**:
   - Las contraseñas se cifran utilizando AES-GCM.
   - Cada contraseña se cifra con una clave derivada de la contraseña maestra del usuario.

2. **Hashing de claves maestras**:
   - Las claves maestras se almacenan como hashes seguros utilizando Argon2.

3. **Sesiones protegidas**:
   - Cada usuario tiene su propia sesión activa.
   - Las rutas están protegidas con un decorador `@login_required`.

4. **Soporte para HTTPS**:
   - La aplicación puede ejecutarse con HTTPS utilizando certificados autogenerados.

5. **Recomendaciones**:
   - Cambia la clave secreta (`SECRET_KEY`) en producción.
   - Usa HTTPS para proteger la comunicación entre el cliente y el servidor.

---

## 🐳 Uso con Docker

### Construir la imagen
```bash
docker build -t key-manager .
```

### Ejecutar el contenedor
```bash
docker-compose up
```

### Acceder a la aplicación
- **HTTP**: `http://127.0.0.1:5000/`
- **HTTPS**: Configura los certificados en el contenedor si es necesario.

---

## 📋 Dependencias

- **Flask**: Framework web.
- **pycryptodomex**: Para cifrado y descifrado de contraseñas.
- **argon2-cffi**: Para hashing seguro de contraseñas.
- **pyperclip**: Para copiar contraseñas al portapapeles.
- **pyopenssl**: Para habilitar HTTPS.
- **cryptography**: Para generar certificados SSL.

---

## 📌 Notas adicionales

- La base de datos SQLite se encuentra en el directorio `instance/passwords.db`.
- Asegúrate de que el directorio `instance` exista antes de ejecutar la aplicación.
- Para restablecer la base de datos, elimina el archivo `passwords.db` y reinicia la aplicación.
- Si usas Docker, el directorio `instance` se crea automáticamente.

---

## 👨‍💻 Contribuciones

Si deseas contribuir al proyecto, por favor:
1. Haz un fork del repositorio.
2. Crea una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza un pull request.

---

## 📞 Soporte

Si tienes preguntas o problemas, no dudes en abrir un issue en el repositorio.

---

¡Gracias por usar **Key Manager**! 🔐