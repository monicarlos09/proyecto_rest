import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from .models import Artista, Disquera


class TestArtistaView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(
            username="testuser1", password="1X<ISRUkw+tuK"
        )

        cls.test_user2 = User.objects.create_user(
            username="testuser2", password="fn34ninwefoi"
        )

        cls.disquera = Disquera.objects.create(
            nombre="Disquera prueba",
            direccion="direccion prueba",
            telefono="555-555-555",
            usuario=cls.test_user1,
        )

        cls.disquera_2 = Disquera.objects.create(
            nombre="Disquera prueba 2",
            direccion="direccion prueba 2",
            telefono="111-111-111",
            usuario=cls.test_user1,
        )

        cls.artista = Artista.objects.create(
            nombre="Artista prueba",
            nacionalidad="Mexicano",
            fecha_nacimiento="1990-12-27",
            genero="POP",
            usuario=cls.test_user2
        )
        cls.artista.disquera.set([cls.disquera, cls.disquera_2])

        cls.url_respuesta = reverse("artista:lista")
        cls.client = APIClient()

    def test_lista_artistas(self):
        """
        Comprobar que el despliegue correctamente el listado de todos los artistas
        """
        respuesta = self.client.get(self.url_respuesta)
        self.assertEqual(200, respuesta.status_code)

    def test_contar_num_registros_en_BD(self):
        """
        Comprobar que el numero de registros en la BD sea igual al listado de la petición
        """
        respuesta = self.client.get(self.url_respuesta)
        num_registros = Artista.objects.all().count()
        self.assertEqual(num_registros, len(respuesta.data))

    def test_comparar_info_lista_vs_info_BD(self):
        """
        Comprobar que la información que se despliega es igual a la contenida en la BD
        """
        respuesta_get = self.client.get(self.url_respuesta)

        for x in respuesta_get.data:
            artista = Artista.objects.get(id=x["id"])
            self.assertEqual(x["nombre"], artista.nombre)
            self.assertEqual(x["nacionalidad"], artista.nacionalidad)
            self.assertEqual(x["genero"], artista.genero)

            for i in x["disquera"]:
                disquera = Disquera.objects.get(id=i["id"])
                j = artista.disquera.get(id=disquera.pk)
                self.assertEqual(j.id, disquera.pk)

    def test_confirmar_nuevo_registro_en_BD(self):
        """
        Comprobar que el numero de elementos despues del insert sea igual al numero de elementos inicial
        en la BD + 1
        """
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")

        data_info = {
            "usuario": self.test_user1.pk,
            "nombre": "Nuevo artista",
            "nacionalidad": "Español",
            "fecha_nacimiento": "2005-05-15",
            "disquera_entrada": [self.disquera.id],
            "genero": "ROCK",
        }

        num_elementos_pre_post = Artista.objects.count()
        respuesta = self.client.post(self.url_respuesta, data_info)
        num_elementos_post_post = Artista.objects.count()
        self.assertEqual(num_elementos_pre_post + 1, num_elementos_post_post)
        self.assertEqual(201, respuesta.status_code)

    def test_comparar_info_registrada_vs_info_en_BD(self):
        """
        Comprobar que la información que se envió a guardar sea igual a la almacenada en la BD
        """
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")

        data_info = {
            "usuario": self.test_user1.pk,
            "nombre": "Nuevo artista",
            "nacionalidad": "Español",
            "fecha_nacimiento": datetime.date(2010, 1, 1),
            "disquera_entrada": [self.disquera.id],
            "genero": "ROCK",
        }

        respuesta_post = self.client.post(self.url_respuesta, data_info)
        self.assertEqual(201, respuesta_post.status_code)
        respuesta_consulta = Artista.objects.get(id=respuesta_post.data["id"])
        self.assertEqual(data_info["nombre"], respuesta_consulta.nombre)
        self.assertEqual(data_info["nacionalidad"], respuesta_consulta.nacionalidad)
        self.assertEqual(data_info["fecha_nacimiento"],
                         respuesta_consulta.fecha_nacimiento)
        self.assertEqual(data_info["genero"], respuesta_consulta.genero)

        for i in respuesta_post.data["disquera"]:
            disquera = Disquera.objects.get(id=i["id"])
            for j in data_info["disquera_entrada"]:
                self.assertEqual(disquera.pk, j)

    def test_recuperar_info_por_ID(self):
        """
        Comprobar que la información solicitada sea igual a la información enviada en la petición
        """
        detalle = reverse("artista:detalle", kwargs={"pk": self.artista.id})
        respuesta_get = self.client.get(detalle)
        self.assertEqual(200, respuesta_get.status_code)
        resultado = Artista.objects.get(id=respuesta_get.data["id"])
        self.assertEqual(resultado.nombre, respuesta_get.data["nombre"])
        self.assertEqual(resultado.nacionalidad, respuesta_get.data["nacionalidad"])
        self.assertEqual(resultado.genero, respuesta_get.data["genero"])

        for i in respuesta_get.data["disquera"]:
            disquera = Disquera.objects.get(id=i["id"])
            j = resultado.disquera.get(id=disquera.pk)
            self.assertEqual(j.id, disquera.pk)

    def test_actualizacion_info_vs_info_en_BD(self):
        """
        Comprobar que la información actualizada sea igual a la información almacenada en la BD
        """
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        actualizacion = reverse("artista:detalle", kwargs={"pk": self.artista.id})

        data_update = {
            "usuario": self.test_user1.pk,
            "nombre": "Nuevo artista",
            "nacionalidad": "Español",
            "fecha_nacimiento": datetime.date(2010, 1, 1),
            "disquera_entrada": [self.disquera.id],
            "genero": "ROCK",
        }

        respuesta_put = self.client.put(actualizacion, data_update)
        self.assertEqual(200, respuesta_put.status_code)
        resultado = Artista.objects.get(id=respuesta_put.data["id"])
        self.assertEqual(respuesta_put.data["nombre"], resultado.nombre)
        self.assertEqual(
            respuesta_put.data["nacionalidad"], resultado.nacionalidad)
        self.assertEqual(respuesta_put.data["genero"], resultado.genero)

        for i in respuesta_put.data["disquera"]:
            disquera = Disquera.objects.get(id=i["id"])
            j = resultado.disquera.get(id=disquera.pk)
            self.assertEqual(j.id, disquera.pk)

    def test_actualizacion_parcial_info_vs_info_en_BD(self):
        """
        Comprobar que la actualizada parcial de la información sea igual a la información almacenada en la BD
        """
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        actualizacion = reverse("artista:detalle", kwargs={"pk": self.artista.id})
        data_update = {"nombre": "Nuevo Artista update PASH"}
        respuesta_actualizacion = self.client.patch(actualizacion, data_update)
        self.assertEqual(200, respuesta_actualizacion.status_code)
        resultado = Artista.objects.get(id=respuesta_actualizacion.data["id"])
        self.assertEqual(respuesta_actualizacion.data["nombre"], resultado.nombre)

    def test_eliminar_registro(self):
        """
        Comprobar que la información eliminada no se encuentre en la BD
        """
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        url_delete = reverse("artista:detalle", kwargs={"pk": self.artista.id})
        num_actual_registros = Artista.objects.all().count()
        respuesta_delete = self.client.delete(url_delete)
        self.assertEqual(204, respuesta_delete.status_code)
        num_registos_actual = Artista.objects.all().count()
        self.assertEqual(num_actual_registros - 1, num_registos_actual)
        recuperar_registro = Artista.objects.filter(pk=self.artista.id).exists()
        self.assertFalse(recuperar_registro)

    def test_no_listar_info_con_usuario_no_logueado(self):
        """
        Comprobar que información no se despliega si el usuario no esta logueado
        """
        respuesta = self.client.post(self.url_respuesta)
        self.assertEqual(401, respuesta.status_code)
