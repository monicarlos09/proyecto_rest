import datetime
from canciones.serializers import AutorSerializer
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from .models import Artista, Disquera, Album, Autor, Cancion


class TestDisqueraView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(
            username="testuser1", password="1X<ISRUkw+tuK"
        )

        cls.autor = Autor.objects.create(
            nombre="Autor 1",
            nacionalidad="Mexicano"
        )

        cls.album = Album.objects.create(
            nombre="Album 1",
            anio_lanzamiento="2000-11-11"
        )

        cls.disquera = Disquera.objects.create(
            nombre="Disquera prueba 1",
            direccion="Direccion prueba 1",
            telefono="111-111-111",
            usuario=cls.test_user1,
        )

        cls.disquera_2 = Disquera.objects.create(
            nombre="Disquera prueba 2",
            direccion="Direccion prueba 2",
            telefono="222-222-222",
            usuario=cls.test_user1,
        )

        cls.artista = Artista.objects.create(
            nombre="Artista prueba",
            nacionalidad="Mexicano",
            fecha_nacimiento="1990-12-27",
            genero="POP",
            usuario=cls.test_user1
        )
        cls.artista.disquera.set([cls.disquera, cls.disquera_2])

        cls.cancion = Cancion.objects.create(
            nombre="Cancion 1",
            anio_lanzamiento=datetime.date(2021, 11, 12),
            precio="100",
            autor=cls.autor,
            usuario=cls.test_user1
        )
        cls.cancion.album.set([cls.album])
        cls.cancion.artista.set([cls.artista])
        cls.cancion.disquera.set([cls. disquera])

        cls.url_respuesta = reverse("canciones:lista")
        cls.client = APIClient()

    def test_lista_canciones(self):
        """
        Comprobar el despliegue correcto del listado de todos las canciones
        """
        respuesta = self.client.get(self.url_respuesta)
        self.assertEqual(200, respuesta.status_code)

    def test_contar_num_registros_en_BD(self):
        """
        Comprobar que el numero de registros en la BD sea igual al listado de la petición
        """
        respuesta = self.client.get(self.url_respuesta)
        num_registros = Cancion.objects.all().count()
        self.assertEqual(num_registros, len(respuesta.data))

    def test_comparar_info_lista_vs_info_BD(self):
        """
        Comprobar que la información que se despliega es igual a la contenida en la BD
        """
        respuesta_get = self.client.get(self.url_respuesta)

        for x in respuesta_get.data:
            cancion = Cancion.objects.get(id=x["id"])
            self.assertEqual(x["nombre"], cancion.nombre)
            self.assertEqual(x["anio_lanzamiento"], str(cancion.anio_lanzamiento))
            self.assertEqual(x["precio"], str(cancion.precio))
            self.assertEqual(x["usuario"], cancion.usuario.id)
            self.assertEqual(x["nombre_autor"], str(cancion.autor))
            # print(x["album"]) --> OrderedDict([('id', 1), ('nombre', 'Album 1'), ('anio_lanzamiento', '2000-11-11')])
            for i in x["album"]:
                # print(i) --> OrderedDict([('id', 1), ('nombre', 'Album 1'), ('anio_lanzamiento', '2000-11-11')])
                album = Album.objects.get(id=i["id"])
                # print(album) --> Album 1
                # print(album.pk) --> 1
                j = cancion.album.get(id=album.pk)
                # print(j) --> Album 1
                # print(j.id) --> 1
                self.assertEqual(j.id, album.pk)

            # print(x["artista"])
            for i in x["artista"]:
                artista = Artista.objects.get(id=i["id"])
                # print(artista)  # --> Artista prueba
                # print(artista.id)  # --> 4
                j = cancion.artista.get(id=artista.pk)
                # print(j)  # --> Artista prueba
                # print(j.pk)  # --> 4
                self.assertEqual(j.pk, artista.id)

            for i in x["disquera"]:
                disquera = Disquera.objects.get(id=i["id"])
                j = cancion.disquera.get(id=disquera.id)
                self.assertEqual(j.pk, disquera.pk)

    def test_confirmar_nuevo_registro_en_BD(self):
        """
        Comprobar que el numero de elementos despues del insert sea igual al numero de elementos inicial
        en la BD + 1
        """
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")

        data_info = {
            "usuario": self.test_user1.pk,
            "nombre": "Nueva Cancion",
            "anio_lanzamiento": "2005-05-15",
            "precio": "200.00",
            "autor": self.autor.id,
            "album_entrada": [self.album.id],
            "artista_entrada": [self.artista.id],
            "disquera_entrada": [self.disquera.id],
        }

        num_elementos_pre_post = Cancion.objects.count()
        respuesta_post = self.client.post(self.url_respuesta, data_info)
        num_elementos_post_post = Cancion.objects.count()
        self.assertEqual(num_elementos_pre_post + 1, num_elementos_post_post)
        self.assertEqual(201, respuesta_post.status_code)

    def test_comparar_info_registrada_vs_info_en_BD(self):
        """
        Comprobar que la información que se envió a guardar sea igual a la almacenada en la BD
        """
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")

        data_info = {
            "usuario": self.test_user1.pk,
            "nombre": "Nueva Cancion",
            "anio_lanzamiento": "2005-05-15",
            "precio": "200.00",
            "autor": self.autor.id,
            "album_entrada": [self.album.id],
            "artista_entrada": [self.artista.id],
            "disquera_entrada": [self.disquera.id],
        }

        respuesta_post = self.client.post(self.url_respuesta, data_info)
        self.assertEqual(201, respuesta_post.status_code)
        respuesta_consulta = Cancion.objects.get(id=respuesta_post.data["id"])

        self.assertEqual(data_info["usuario"], respuesta_consulta.usuario.id)
        self.assertEqual(data_info["nombre"], respuesta_consulta.nombre)
        self.assertEqual(data_info["anio_lanzamiento"],
                         str(respuesta_consulta.anio_lanzamiento))
        self.assertEqual(data_info["precio"], str(respuesta_consulta.precio))
        self.assertEqual(data_info["autor"], respuesta_consulta.autor.id)

        # print(respuesta_post.data["album"]) --> [OrderedDict([('id', 1), ('nombre', 'Album 1'), ('anio_lanzamiento', '2000-11-11')])]
        for i in respuesta_post.data["album"]:
            cancion = Cancion.objects.get(id=i["id"])
            # print(cancion) --> Cancion 1
            for j in data_info["album_entrada"]:
                # print(j) --> 1
                self.assertEqual(cancion.pk, j)

        for i in respuesta_post.data["artista"]:
            artista = Artista.objects.get(id=i["id"])
            for j in data_info["artista_entrada"]:
                self.assertEqual(artista.pk, j)

        for i in respuesta_post.data["disquera"]:
            disquera = Disquera.objects.get(id=i["id"])
            for j in data_info["disquera_entrada"]:
                self.assertEqual(disquera.pk, j)

    def test_recuperar_info_por_ID(self):
        """
        Comprobar que la información solicitada sea igual a la información enviada en la petición
        """
        detalle = reverse("canciones:detalle", kwargs={"pk": self.cancion.id})
        respuesta_get = self.client.get(detalle)
        self.assertEqual(200, respuesta_get.status_code)
        resultado = Cancion.objects.get(id=respuesta_get.data["id"])
        self.assertEqual(resultado.nombre, respuesta_get.data["nombre"])
        self.assertEqual(str(resultado.anio_lanzamiento),
                         respuesta_get.data["anio_lanzamiento"])
        self.assertEqual(str(resultado.precio), respuesta_get.data["precio"])
        self.assertEqual(resultado.autor.nombre, respuesta_get.data["nombre_autor"])

        for i in respuesta_get.data["album"]:
            album = Album.objects.get(id=i["id"])
            j = resultado.album.get(id=album.pk)
            self.assertEqual(j.id, album.pk)

        for i in respuesta_get.data["artista"]:
            artista = Artista.objects.get(id=i["id"])
            j = resultado.artista.get(id=artista.pk)
            self.assertEqual(j.id, artista.pk)

        for i in respuesta_get.data["disquera"]:
            disquera = Disquera.objects.get(id=i["id"])
            j = resultado.disquera.get(id=disquera.pk)
            self.assertEqual(j.id, disquera.pk)

    def test_actualizacion_info_vs_info_en_BD(self):
        """
        Comprobar que la información actualizada sea igual a la información almacenada en la BD
        """
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        actualizacion = reverse("canciones:detalle", kwargs={"pk": self.cancion.id})

        data_update = {
            "usuario": self.test_user1.pk,
            "nombre": "Nuevo Cancion",
            "anio_lanzamiento": "2005-05-15",
            "precio": "200.00",
            "autor": self.autor.id,
            "album_entrada": [self.album.id],
            "artista_entrada": [self.artista.id],
            "disquera_entrada": [self.disquera.id],
        }

        respuesta_put = self.client.put(actualizacion, data_update)
        self.assertEqual(200, respuesta_put.status_code)
        resultado = Cancion.objects.get(id=respuesta_put.data["id"])
        self.assertEqual(respuesta_put.data["nombre"], resultado.nombre)
        self.assertEqual(
            respuesta_put.data["anio_lanzamiento"], str(resultado.anio_lanzamiento))
        self.assertEqual(respuesta_put.data["precio"], str(resultado.precio))
        self.assertEqual(respuesta_put.data["nombre_autor"], resultado.autor.nombre)

        for i in respuesta_put.data["album"]:
            album = Album.objects.get(id=i["id"])
            j = resultado.album.get(id=album.pk)
            self.assertEqual(j.id, album.pk)

        for i in respuesta_put.data["artista"]:
            artista = Artista.objects.get(id=i["id"])
            j = resultado.artista.get(id=artista.pk)
            self.assertEqual(j.id, artista.pk)

        for i in respuesta_put.data["disquera"]:
            disquera = Disquera.objects.get(id=i["id"])
            j = resultado.disquera.get(id=disquera.pk)
            self.assertEqual(j.id, disquera.pk)

    def test_actualizacion_parcial_info_vs_info_en_BD(self):
        """
        Comprobar que la actualizada parcial de la información sea igual a la información almacenada en la BD
        """
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")

        data_update = {
            "usuario": self.test_user1.pk,
            "nombre": "Nuevo Cancion update",
            "autor": self.autor.id,
            "album_entrada": [self.album.id],
            "artista_entrada": [self.artista.id],
            "disquera_entrada": [self.disquera.id],
        }
        actualizacion = reverse("canciones:detalle", kwargs={"pk": self.cancion.id})

        respuesta_patch = self.client.patch(actualizacion, data_update)
        self.assertEqual(200, respuesta_patch.status_code)
        resultado = Cancion.objects.get(id=respuesta_patch.data["id"])
        self.assertEqual(respuesta_patch.data["nombre"], resultado.nombre)
        self.assertEqual(
            respuesta_patch.data["nombre_autor"], resultado.autor.nombre)

        for i in respuesta_patch.data["album"]:
            album = Album.objects.get(id=i["id"])
            j = resultado.album.get(id=album.pk)
            self.assertEqual(j.id, album.pk)

        for i in respuesta_patch.data["artista"]:
            artista = Artista.objects.get(id=i["id"])
            j = resultado.artista.get(id=artista.pk)
            self.assertEqual(j.id, artista.pk)

        for i in respuesta_patch.data["disquera"]:
            disquera = Disquera.objects.get(id=i["id"])
            j = resultado.disquera.get(id=disquera.pk)
            self.assertEqual(j.id, disquera.pk)

    def test_eliminar_registro(self):
        """
        Comprobar que la información eliminada no se encuentre en la BD
        """
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        url_delete = reverse("canciones:detalle", kwargs={"pk": self.cancion.id})
        num_actual_registros = Cancion.objects.all().count()
        respuesta_delete = self.client.delete(url_delete)
        self.assertEqual(204, respuesta_delete.status_code)
        num_registos_actual = Cancion.objects.all().count()
        self.assertEqual(num_actual_registros - 1, num_registos_actual)
        recuperar_registro = Cancion.objects.filter(pk=self.cancion.id).exists()
        self.assertFalse(recuperar_registro)

    def test_no_listar_info_con_usuario_no_logueado(self):
        """
        Comprobar que la información no se despliega si el usuario no esta logueado
        """
        respuesta = self.client.post(self.url_respuesta)
        self.assertEqual(401, respuesta.status_code)
