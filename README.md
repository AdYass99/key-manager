# Key Manager

This project is a simple Flask application for managing user passwords. It allows users to add and view passwords securely.

## Project Structure

```
key-manager
├── app
│   ├── __init__.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── home.py
│   │   └── passwords.py
│   ├── templates
│   │   └── index.html
│   └── database.py
├── instance
│   └── passwords.db
├── requirements.txt
├── run.py
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd key-manager
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```
   python run.py
   ```

## Usage

- Navigate to `http://127.0.0.1:5000/` in your web browser to access the application.
- Use the home page to add new passwords and view existing ones.

## Security Note

Ensure that you handle user passwords securely and consider implementing additional security measures such as password hashing and HTTPS for production environments.