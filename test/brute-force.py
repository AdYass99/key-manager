import unittest
import json
import requests
import time

class TestBruteForceLogin(unittest.TestCase):
    def setUp(self):
        self.url = 'https://localhost:5000/login'
        self.user = 'user'  # Usa un usuario válido o inventado
        self.passwords = ['123456', 'password', 'admin', 'letmein', 'qwerty',
                          '123123', 'abc123', 'qwerty123', 'monkey', '111111',
                          '123456789', '12345678', '12345', '1234567', '1234567890',
                          '123456789', '1234567890', '12345678901', 'user']
        self.expected_failure_message = 'Búsqueda de Contraseña'
        self.results = []  # Lista para almacenar los resultados de todos los intentos

    def test_brute_force(self):
        for pw in self.passwords:
            with self.subTest(password=pw):
                start_time = time.time()
                response = requests.post(self.url, data={'username': self.user, 'password': pw}, verify=False)
                elapsed_time = time.time() - start_time

                # Hacer el texto más legible
                response_text = response.text.strip()

                # Determinar si la contraseña es correcta basándose en la respuesta del servidor
                if self.expected_failure_message in response_text:
                    self.results.append({"password": pw, "status": "success", "response_time": elapsed_time})
                    print(f"[SUCCESS] Password found: '{pw}' | Response Time: {elapsed_time:.3f}s")
                    break  # Detener el ataque si se encuentra la contraseña correcta
                else:
                    self.results.append({"password": pw, "status": "failure", "response_time": elapsed_time})
                    print(f"[FAILURE] Password: '{pw}' | Response Time: {elapsed_time:.3f}s")

                # Comentar sobre el tiempo de respuesta
                if elapsed_time < 0.3:  # 300 ms
                    print(f"WARNING: Hashing or delay too fast for password '{pw}' ({elapsed_time:.3f}s)")

    def tearDown(self):
        # Guardar los resultados en un archivo JSON al finalizar las pruebas
        if self.results:  # Asegurarse de que la lista no esté vacía
            save_test_results_to_file(self.results, "test_results_brute_force.json")

def save_test_results_to_file(results, filename="test_results_brute_force.json"):
    """Guardar los resultados de los tests en un archivo JSON."""
    try:
        with open(filename, "w") as file:
            json.dump(results, file, indent=4)
        print(f"Resultados guardados en {filename}")
    except Exception as e:
        print(f"Error al guardar los resultados: {e}")

if __name__ == '__main__':
    # Ejecutar los tests
    unittest.main()