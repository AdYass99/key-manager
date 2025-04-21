import unittest
import json
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import sqlite3
import os

class TestPasswordHashing(unittest.TestCase):
    def setUp(self):
        # Usar la misma base de datos que la aplicación
        self.database_path = os.path.join('instance', 'passwords.db')
        self.password = 'secure_password'
        self.wrong_password = 'wrong_password'
        self.ph = PasswordHasher()
        self.hashed_password = self.ph.hash(self.password)

    def test_hash_generation(self):
        # Verificar que el hash generado no es igual a la contraseña original
        self.assertNotEqual(self.password, self.hashed_password)
        # Verificar que el hash generado tiene el prefijo estándar de Argon2
        self.assertTrue(self.hashed_password.startswith('$argon2'))

    def test_hash_validation(self):
        # Verificar que la contraseña correcta pasa la validación
        self.assertTrue(self.ph.verify(self.hashed_password, self.password))
        # Verificar que una contraseña incorrecta no pasa la validación
        with self.assertRaises(VerifyMismatchError):
            self.ph.verify(self.hashed_password, self.wrong_password)

    def test_database_hash_format(self):
        # Conectar a la base de datos de la aplicación
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT master_password_hash FROM users WHERE username = 'user'")
        result = cursor.fetchone()
        conn.close()

        if result:
            db_hash = result[0]
            self.assertTrue(db_hash.startswith('$argon2'))
            print(f"Hash encontrado en la base de datos: {db_hash[:20]}... (ocultado por seguridad)")
        else:
            self.fail("No se encontró el usuario en la base de datos.")

def save_test_results_to_file(results, filename="test_results_hashing.json"):
    """Guardar los resultados de los tests en un archivo JSON."""
    with open(filename, "w") as file:
        json.dump(results, file, indent=4)

if __name__ == '__main__':
    # Ejecutar los tests y capturar los resultados
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestPasswordHashing)
    runner = unittest.TextTestRunner(resultclass=unittest.TextTestResult)
    result = runner.run(suite)

    # Estructurar los resultados
    test_results = {
        "testsRun": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "successful": result.wasSuccessful(),
        "details": {
            "failures": [{"test": str(f[0]), "reason": str(f[1])} for f in result.failures],
            "errors": [{"test": str(e[0]), "reason": str(e[1])} for e in result.errors],
        },
    }

    # Guardar los resultados en un archivo
    save_test_results_to_file(test_results)