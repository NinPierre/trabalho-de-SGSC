import os
import sys
import threading
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import app as app_module
import adm as adm_module
from database import Base, engine


class AppIntegrationTests(unittest.TestCase):
    def setUp(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    def test_login_with_threaded_database_access(self):
        adm_module.criar_usuario("Admin", "11111111111", "123", "professor")

        result = {}

        def buscar_usuario_em_thread():
            try:
                usuario = adm_module.buscar_usuario("11111111111", "123")
                result["usuario"] = usuario
            except Exception as exc:
                result["erro"] = str(exc)

        thread = threading.Thread(target=buscar_usuario_em_thread)
        thread.start()
        thread.join(5)

        self.assertFalse("erro" in result, f"Falha ao acessar o banco em thread: {result.get('erro')}")
        self.assertIsNotNone(result.get("usuario"))

        client = app_module.app.test_client()
        response = client.post(
            "/login",
            data={"cpf": "11111111111", "senha": "123"},
            follow_redirects=False,
        )
        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
