from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from .models import Disquera
from django.urls import reverse
from django.contrib.auth.models import User


class TestDisqueraView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')

        test_user2 = User.objects.create_user(
            username='testuser2', password='fn34ninwefoi')

        cls.disquera = Disquera.objects.create(nombre='Disquera prueba', direccion='direccion prueba',
                                               telefono='555-555-555', usuario=cls.test_user1)

        cls.disquera_2 = Disquera.objects.create(nombre='Disquera prueba 2', direccion='otra direccion',
                                                 telefono='333-333-333', usuario=test_user2)

        # URL donde esta disquera
        cls.url_respuesta = reverse('disquera:lista')
        cls.client = APIClient()  # Se construye objeto de APIClient vacio

    def test_listado_disqueras(self):
        """
        Comprobar que el despliegue del listado de todas las disqueras se ejecute correctamente
        """
        respuesta = self.client.get(self.url_respuesta)
        self.assertEqual(200, respuesta.status_code)

    def test_num_registros_en_BD(self):
        """
        Comprobar que el numero de registros en la BD sea igual al listado de respuesta
        """
        respuesta = self.client.get(self.url_respuesta)
        num_registros = Disquera.objects.all().count()
        self.assertEqual(num_registros, len(respuesta.data))

    def test_elementos_lista_vs_BD(self):
        respuesta = self.client.get(self.url_respuesta)
        # print(respuesta.data)
        for i in respuesta.data:
            nombre_disquera = Disquera.objects.get(id=i['id'])
            self.assertEqual(i['nombre'], nombre_disquera.nombre)
           # self.assertEqual(i['usuario'], nombre_disquera.username)
            self.assertEqual(i['usuario'], str(nombre_disquera.usuario))

    def test_POST_nuevo_num_registros_en_BD(self):
        """
        Comprobar que el numero de elementos despues del insert sea igual al numero de elementos inicial
        en la BD + 1
        """
        self.client.login(
            username='testuser1', password='1X<ISRUkw+tuK')

        data_info = {'usuario': self.test_user1.pk, 'nombre': 'nueva disquera',
                     'direccion': 'nueva direccion', 'telefono': '111-111-111'}

        num_elementos_pre_post = Disquera.objects.count()
        respuesta = self.client.post(self.url_respuesta, data_info)
        num_elementos_post_post = Disquera.objects.count()
        self.assertEqual(num_elementos_pre_post + 1, num_elementos_post_post)

    def test_POST_comparar_respuesta_post_vs_BD(self):

        self.client.login(
            username='testuser1', password='1X<ISRUkw+tuK')

        data_info = {'usuario': self.test_user1.pk, 'nombre': 'nueva disquera',
                     'direccion': 'nueva direccion', 'telefono': '111-111-111'}

        respuesta_post = self.client.post(self.url_respuesta, data_info)
        self.assertEqual(201, respuesta_post.status_code)
        valor_consulta = Disquera.objects.get(id=respuesta_post.data['id'])
        self.assertEqual(data_info['nombre'], valor_consulta.nombre)
        self.assertEqual(data_info['direccion'], valor_consulta.direccion)
        self.assertEqual(data_info['telefono'], valor_consulta.telefono)

    def test_recuperar_registro_por_ID(self):
        """
        Comprobar que el registro solicitado sea igual a la respuesta
        """
        detalle = reverse('disquera:detalle', kwargs={
            'pk': self.disquera.id})

        respuesta = self.client.get(detalle)
        self.assertEqual(200, respuesta.status_code)
        resultado = Disquera.objects.get(id=respuesta.data['id'])
        self.assertEqual(respuesta.data['nombre'], resultado.nombre)
        self.assertEqual(respuesta.data['direccion'], resultado.direccion)
        self.assertEqual(respuesta.data['telefono'], resultado.telefono)

    def test_PUT_vs_BD(self):
        self.client.login(
            username='testuser1', password='1X<ISRUkw+tuK')

        actualizacion = reverse('disquera:detalle', kwargs={
                                'pk': self.disquera.id})

        data_update = {'usuario': self.test_user1.pk, 'nombre': 'nueva disquera update',
                       'direccion': 'nueva direccion update', 'telefono': '111-111-0000'}

        respuesta_actualizacion = self.client.put(actualizacion, data_update)
        self.assertEqual(200, respuesta_actualizacion.status_code)
        resultado = Disquera.objects.get(id=respuesta_actualizacion.data['id'])
        self.assertEqual(
            respuesta_actualizacion.data['nombre'], resultado.nombre)
        self.assertEqual(
            respuesta_actualizacion.data['direccion'], resultado.direccion)
        self.assertEqual(
            respuesta_actualizacion.data['telefono'], resultado.telefono)

    def test_PASH_vs_BD(self):
        self.client.login(
            username='testuser1', password='1X<ISRUkw+tuK')

        actualizacion = reverse('disquera:detalle', kwargs={
                                'pk': self.disquera.id})

        data_update = {'nombre': 'nueva disquera update PASH'}

        respuesta_actualizacion = self.client.patch(actualizacion, data_update)
        self.assertEqual(200, respuesta_actualizacion.status_code)
        resultado = Disquera.objects.get(id=respuesta_actualizacion.data['id'])
        self.assertEqual(
            respuesta_actualizacion.data['nombre'], resultado.nombre)

    def test_DELETE(self):
        self.client.login(
            username='testuser1', password='1X<ISRUkw+tuK')

        url_delete = reverse('disquera:detalle', kwargs={
            'pk': self.disquera.id})

        num_actual_registros = Disquera.objects.all().count()
        respuesta_delete = self.client.delete(url_delete)
        self.assertEqual(204, respuesta_delete.status_code)
        num_registos_actual = Disquera.objects.all().count()
        self.assertEqual(num_actual_registros - 1, num_registos_actual)

        #recuperar_registro = Disquera.objects.get(pk=self.disquera.id)
        recuperar_registro = Disquera.objects.filter(
            pk=self.disquera.id).exists()
        self.assertFalse(recuperar_registro)

        # print(recuperar_registro)

    def test_post_con_usuario_no_logueado(self):

        data_info = {'nombre': 'nueva disquera',
                     'direccion': 'nueva direccion', 'telefono': '111-111-111'}

        respuesta = self.client.post(self.url_respuesta, data_info)
        print(respuesta)
        self.assertEqual(400, respuesta.status_code)
