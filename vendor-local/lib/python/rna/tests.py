# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.test.utils import override_settings
from mock import Mock, patch
from nose.tools import eq_, ok_

from . import clients, fields, filters, models, serializers, views
from .management.commands import rnasync


class AdminTest(TestCase):
    @patch('django.contrib.admin.site.register')
    def test_register(self, mock_register):
        import rna.rna.admin  # NOQA
        mock_register.assert_any_call(models.Channel)
        mock_register.assert_any_call(models.Product)
        mock_register.assert_any_call(models.Tag)
        mock_register.assert_any_call(models.Note)


class TimeStampedModelTest(TestCase):
    @patch('rna.rna.models.models.Model.save')
    def test_default_modified(self, mock_super_save):
        start = datetime.now()
        model = models.TimeStampedModel()
        model.save(db='test')
        ok_(model.modified > start)
        mock_super_save.assert_called_once_with(db='test')

    @patch('rna.rna.models.models.Model.save')
    def test_unmodified(self, mock_super_save):
        model = models.TimeStampedModel()
        model.modified = space_odyssey = datetime(2001, 1, 1)
        model.save(modified=False, db='test')
        eq_(model.modified, space_odyssey)
        mock_super_save.assert_called_once_with(db='test')


class ChannelTest(TestCase):
    def test_unicode(self):
        """
        Should equal name
        """
        channel = models.Channel(name='test')
        eq_(unicode(channel), 'test')


class ProductTest(TestCase):
    def test_unicode(self):
        """
        Should equal name
        """
        product = models.Product(name='test')
        eq_(unicode(product), 'test')


class NoteTest(TestCase):
    def test_unicode(self):
        """
        Should equal description
        """
        note = models.Note(html='test')
        eq_(unicode(note), 'test')


class TagTest(TestCase):
    def test_unicode(self):
        """
        Should equal text
        """
        tag = models.Tag(text='test')
        eq_(unicode(tag), 'test')


class ReleaseTest(TestCase):
    def test_unicode(self):
        """
        Should equal name
        """
        release = models.Release(text='test')
        eq_(unicode(release), 'test')


class ISO8601DateTimeFieldTest(TestCase):
    @patch('rna.rna.fields.parse_datetime')
    def test_strptime(self, mock_parse_datetime):
        """
        Should equal expected_date returned by mock_parse_datetime
        """
        expected_date = datetime(2001, 1, 1)
        mock_parse_datetime.return_value = expected_date
        field = fields.ISO8601DateTimeField()
        eq_(field.strptime('value', 'format'), expected_date)


class TimeStampedModelSubclass(models.TimeStampedModel):
    test = models.models.BooleanField(default=True)


class TimestampedFilterBackendTest(TestCase):
    @patch('rna.rna.filters.DjangoFilterBackend.get_filter_class',
           return_value='The Dude')
    def test_filter_class(self, mock_super_get_filter_class):
        """
        Should return super call if view has filter_class attr
        """
        mock_view = Mock(filter_class='abides')
        filter_backend = filters.TimestampedFilterBackend()
        eq_(filter_backend.get_filter_class(mock_view), 'The Dude')

    @patch('rna.rna.filters.DjangoFilterBackend.get_filter_class',
           return_value='The Dude')
    def test_filter_fields(self, mock_super_get_filter_class):
        """
        Should return super call if view has filter_fields attr
        """
        mock_view = Mock(filter_fields='abides')
        filter_backend = filters.TimestampedFilterBackend()
        eq_(filter_backend.get_filter_class(mock_view), 'The Dude')

    @patch('rna.rna.filters.DjangoFilterBackend.get_filter_class')
    def test_no_queryset(self, mock_super_get_filter_class):
        """
        Should return None if queryset is None (the default)
        """
        view = 'nice'
        filter_backend = filters.TimestampedFilterBackend()
        eq_(filter_backend.get_filter_class(view), None)
        ok_(not mock_super_get_filter_class.called)

    @patch('rna.rna.filters.DjangoFilterBackend.get_filter_class')
    def test_non_timestampedmodel(self, mock_super_get_filter_class):
        """
        Should return None if queryset.model is not a subclass of
        models.TimeStampedModel
        """
        view = 'nice'
        queryset = Mock(model=models.models.Model)  # model
        filter_backend = filters.TimestampedFilterBackend()
        eq_(filter_backend.get_filter_class(view, queryset=queryset), None)
        ok_(not mock_super_get_filter_class.called)

    @patch('rna.rna.filters.DjangoFilterBackend.get_filter_class')
    def test_default(self, mock_super_get_filter_class):
        """
        Should return a subclass of the default_filter_set instance
        attr with the inner Meta class model attr equal to the queryset
        model and fields equal to all of the model fields except
        created and modified, and in addition the created_before,
        created_after, modified_before, and modified_after fields
        """
        view = 'nice'
        queryset = Mock(model=TimeStampedModelSubclass)
        filter_backend = filters.TimestampedFilterBackend()
        filter_class = filter_backend.get_filter_class(view, queryset=queryset)
        eq_(filter_class.Meta.model, TimeStampedModelSubclass)
        eq_(filter_class.Meta.fields,
            ['created_before', 'created_after', 'modified_before',
             'modified_after', 'id', 'test'])
        ok_(not mock_super_get_filter_class.called)

    @patch('rna.rna.filters.DjangoFilterBackend.get_filter_class')
    def test_exclude_fields(self, mock_super_get_filter_class):
        """
        Should not include fields named in the view.
        """
        mock_view = Mock(
            filter_class=None, filter_fields=None,
            filter_fields_exclude=('created_before', 'id'))
        queryset = Mock(model=TimeStampedModelSubclass)
        filter_backend = filters.TimestampedFilterBackend()
        filter_class = filter_backend.get_filter_class(
            mock_view, queryset=queryset)
        eq_(filter_class.Meta.model, TimeStampedModelSubclass)
        eq_(filter_class.Meta.fields,
            ['created_after', 'modified_before', 'modified_after', 'test'])
        eq_(mock_super_get_filter_class.called, 0)


class RestClientTest(TestCase):
    def test_init_kwargs(self):
        """
        Should set base_url and token attr from kwargs
        """
        rc = clients.RestClient(base_url='http://thedu.de', token='midnight')
        eq_(rc.base_url, 'http://thedu.de')
        eq_(rc.token, 'midnight')

    @override_settings(RNA={'TOKEN': 'midnight',
                            'BASE_URL': 'http://thedu.de'})
    def test_init_settings(self):
        """
        Should set base_url and token attrs from settings
        """
        rc = clients.RestClient()
        eq_(rc.base_url, 'http://thedu.de')
        eq_(rc.token, 'midnight')

    @patch('rna.rna.clients.requests.request')
    def test_request_base_url_concat(self, mock_request):
        """
        Should concatenate base_url and url
        """

        rc = clients.RestClient(base_url='http://thedu.de')
        mock_request.return_value = 'response'
        response = rc.request('get', '/abides')
        mock_request.assert_called_once_with('get', 'http://thedu.de/abides')
        eq_(response, 'response')

    @patch('rna.rna.clients.requests.request')
    def test_request_redundant_url(self, mock_request):
        """
        Should not concatenate base_url if url starts with it
        """

        rc = clients.RestClient(base_url='http://thedu.de')
        mock_request.return_value = Mock(content='{"aggression": "not stand"}')
        response = rc.request('get', 'http://thedu.de/abides')
        eq_(response.content, '{"aggression": "not stand"}')
        mock_request.assert_called_once_with('get', 'http://thedu.de/abides')

    @patch('rna.rna.clients.requests.request')
    def test_request_token(self, mock_request):
        """
        Should set Authorization header to expected format
        """
        mock_request.return_value = 'this aggression will not stand!'
        rc = clients.RestClient(base_url='http://thedu.de', token='midnight')
        response = rc.request('get', '')
        mock_request.assert_called_once_with(
            'get', 'http://thedu.de',
            headers={'Authorization': 'Token midnight'})
        eq_(response, 'this aggression will not stand!')

    @patch('rna.rna.clients.requests.request')
    def test_request_token_preserves_headers(self, mock_request):
        """
        Should set Authorization header to expected format without removing
        other headers
        """

        mock_request.return_value = 'this aggression will not stand!'
        rc = clients.RestClient(base_url='http://thedu.de', token='midnight')

        response = rc.request('get', '', headers={'White': 'Russian'})
        mock_request.assert_called_once_with(
            'get', 'http://thedu.de',
            headers={'Authorization': 'Token midnight', 'White': 'Russian'})
        eq_(response, 'this aggression will not stand!')

    @patch('rna.rna.clients.requests.request')
    def test_request_delete(self, mock_request):
        """
        Should return unmodified response from requests.request
        """
        rc = clients.RestClient(base_url='http://th.is')
        mock_request.return_value = Mock(status_code=204)
        response = rc.request('delete', '/aggression')
        mock_request.assert_called_once_with(
            'delete', 'http://th.is/aggression')
        eq_(response.status_code, 204)

    @patch('rna.rna.clients.RestClient.request')
    def test_delete(self, mock_request):
        """
        Should pass through kwargs and return unmodified response from
        self.request
        """
        rc = clients.RestClient(base_url='http://th.is')
        mock_request.return_value = Mock(status_code=204)
        response = rc.delete('/aggression', params={'will': 'not stand'})
        mock_request.assert_called_once_with(
            'delete', '/aggression', params={'will': 'not stand'})
        eq_(response.status_code, 204)

    @patch('rna.rna.clients.RestClient.request')
    def test_get_params(self, mock_request):
        """
        Should pass through kwargs and return unmodified response from
        self.request
        """
        rc = clients.RestClient(base_url='http://thedu.de')
        mock_request.return_value = 'abides'
        response = rc.get('', params={'white': 'russian'})
        mock_request.assert_called_once_with(
            'get', '', params={'white': 'russian'})
        eq_(response, 'abides')

    @patch('rna.rna.clients.RestClient.request')
    def test_get_cached(self, mock_request):
        """
        Should return cached response without calling self.request
        """
        rc = clients.RestClient(base_url='http://thedu.de')
        rc.cache = {'': 'abides'}
        response = rc.get()
        eq_(response, 'abides')
        ok_(not mock_request.called)

    @patch('rna.rna.clients.RestClient.request')
    def test_get_cache_miss_200(self, mock_request):
        """
        Should cache and return response
        """
        mock_request.return_value = Mock(status_code=200)
        rc = clients.RestClient()
        response = rc.get()
        mock_request.assert_called_once_with('get', '')
        eq_(response.status_code, 200)
        eq_(rc.cache[''].status_code, 200)

    @patch('rna.rna.clients.RestClient.request')
    def test_get_cache_miss_500(self, mock_request):
        """
        Should return response without caching
        """
        mock_request.return_value = Mock(status_code=500)
        rc = clients.RestClient()
        response = rc.get()
        eq_(response.status_code, 500)
        mock_request.assert_called_once_with('get', '')
        eq_(rc.cache, {})

    @patch('rna.rna.clients.RestClient.request')
    def test_options(self, mock_request):
        """
        Should pass through kwargs and return unmodified response from
        self.request
        """
        rc = clients.RestClient(base_url='http://thedu.de')
        mock_request.return_value = {'white': 'russians'}
        response = rc.options('/drinks')
        mock_request.assert_called_once_with('options', '/drinks')
        eq_(response, {'white': 'russians'})

    @patch('rna.rna.clients.RestClient.request')
    def test_options_cached(self, mock_request):
        """
        Should return cached value without calling self.request
        """
        rc = clients.RestClient(base_url='http://thedu.de')
        rc.cache['OPTIONS'] = {'/drinks': {'white': 'russians'}}
        response = rc.options('/drinks')
        eq_(mock_request.called, 0)
        eq_(response, {'white': 'russians'})

    @patch('rna.rna.clients.RestClient.request')
    def test_post(self, mock_request):
        """
        Should pass through data to, and return unmodified response
        from, self.request
        """
        rc = clients.RestClient(base_url='http://walt.er')
        mock_request.return_value = Mock(
            content='Is this your homework, Larry?')
        response = rc.post('/larry', data={'world': 'of pain'})
        mock_request.assert_called_once_with(
            'post', '/larry', data={'world': 'of pain'})
        eq_(response.content, 'Is this your homework, Larry?')

    @patch('rna.rna.clients.RestClient.request')
    def test_put(self, mock_request):
        """
        Should pass through data to, and return unmodified response
        from, self.request
        """
        rc = clients.RestClient(base_url='http://walt.er')
        mock_request.return_value = Mock(
            content='Is this your homework, Larry?')
        response = rc.put('/larry', data={'world': 'of pain'})
        mock_request.assert_called_once_with(
            'put', '/larry', data={'world': 'of pain'})
        eq_(response.content, 'Is this your homework, Larry?')


class RestModelClientTest(TestCase):
    @patch('rna.rna.clients.RestClient.__init__')
    def test_init_kwargs(self, mock_super_init):
        """
        Should set model_class from model_class kwarg
        """
        rc = clients.RestModelClient(
            base_url='http://thedu.de', token='midnight', model_class='super')
        eq_(rc.model_class, 'super')
        mock_super_init.assert_called_once_with(
            base_url='http://thedu.de', cache=None, token='midnight')

    @patch('rna.rna.clients.RestModelClient.serializer')
    @patch('rna.rna.clients.RestModelClient.restore')
    @patch('rna.rna.clients.RestModelClient.get')
    def test_model(self, mock_get, mock_restore, mock_serializer):
        """
        Should pass data from super get to restore method and return instance
        """
        data = {'rank': 'lieutenant commander'}
        mock_get.return_value = Mock(json=lambda: data)
        mock_serializer.return_value = 'mock serializer'
        mock_restore.return_value = 'instance'
        rc = clients.RestModelClient()
        instance = rc.model(model_class='super')
        eq_(instance, 'instance')
        mock_serializer.assert_called_once_with('super')
        mock_restore.assert_called_once_with(
            'mock serializer', data, False, False)

    @patch('rna.rna.clients.RestModelClient.serializer')
    @patch('rna.rna.clients.RestModelClient.restore')
    @patch('rna.rna.clients.RestModelClient.get')
    def test_models(self, mock_get, mock_restore, mock_serializer):
        """
        Should return list of model instances if data from get is a list
        """
        data = [{'rank': 'lieutenant commander'}, {'eyes': 'yellow'}]
        mock_get.return_value = Mock(json=lambda: data)
        mock_serializer.return_value = 'mock serializer'
        rc = clients.RestModelClient()
        rc.model(model_class='super')
        mock_serializer.assert_called_once_with('super')
        mock_restore.assert_any_call(
            'mock serializer', data[0], False, False)
        mock_restore.assert_any_call(
            'mock serializer', data[1], False, False)

    @patch('rna.rna.clients.RestModelClient.hypermodel')
    def test_restore(self, mock_hypermodel):
        """
        Should return instance from serializer.restore_object
        Should remove url field from data
        Should use hypermodel method on FK fields
        """
        mock_fk_field = Mock(spec=models.models.ForeignKey)
        mock_fk_field.name = 'fk'
        mock_fk_field.rel = Mock(to='to')
        mock_fk_field_not_in_data = Mock(spec=models.models.ForeignKey)
        mock_fk_field_not_in_data.name = 'no data'
        fields = [mock_fk_field, 'non_fk_field', mock_fk_field_not_in_data]
        mock_serializer = Mock()
        mock_serializer.Meta.model._meta.fields = fields
        data = {'url': 'http://remove.me', 'fk': 'http://thedu.de'}

        rc = clients.RestModelClient()
        instance = rc.restore(mock_serializer, data)
        eq_(instance, mock_serializer.restore_object.return_value)
        mock_hypermodel.assert_called_once_with('http://thedu.de', 'to', False)
        mock_serializer.restore_object.assert_called_once_with(
            {'fk': mock_hypermodel.return_value})
        eq_(mock_serializer.save_object.called, 0)

    @patch('rna.rna.clients.RestModelClient.hypermodel')
    def test_restore_save_modified(self, mock_hypermodel):
        """
        Should pass instance to serializer.save_object
        """
        mock_serializer = Mock()
        mock_serializer.Meta.model._meta.fields = []

        rc = clients.RestModelClient()
        instance = rc.restore(mock_serializer, {}, save=True, modified=True)
        eq_(instance, mock_serializer.restore_object.return_value)
        mock_serializer.restore_object.assert_called_once_with({})
        mock_serializer.save_object.assert_called_once_with(instance, modified=True)
        eq_(mock_hypermodel.called, 0)

    @patch('rna.rna.clients.RestModelClient.serialize')
    @patch('rna.rna.clients.RestModelClient.post')
    def test_post_instance(self, mock_post, mock_serialize):
        """
        Should pass serialized data to post method
        """
        instance = 'instance'
        rc = clients.RestModelClient()
        response = rc.post_instance(instance, 'http://positronic.net')
        eq_(response, mock_post.return_value)
        mock_post.assert_called_once_with(
            'http://positronic.net', mock_serialize.return_value)
        mock_serialize.assert_called_once_with(instance)

    @patch('rna.rna.clients.RestModelClient.serialize')
    @patch('rna.rna.clients.RestModelClient.put')
    def test_put_instance(self, mock_put, mock_serialize):
        """
        Should pass serialized data to put method
        """
        instance = 'instance'
        rc = clients.RestModelClient()
        response = rc.put_instance(instance, 'http://positronic.net')
        eq_(response, mock_put.return_value)
        mock_put.assert_called_once_with(
            'http://positronic.net', mock_serialize.return_value)
        mock_serialize.assert_called_once_with(instance)

    @patch('rna.rna.clients.RestClient.__init__')
    @patch('rna.rna.clients.RestModelClient.serializer')
    def test_serialize(self, mock_serializer, mock_super_init):
        """
        Should pass instance through to serializer and return data attr
        """
        serialized_data = '{"eyes": "yellow"}'
        mock_serializer.return_value = Mock(data=serialized_data)
        mock_instance = Mock(eyes='yellow')
        rc = clients.RestModelClient()
        serialized = rc.serialize(instance=mock_instance)
        eq_(serialized, serialized_data)
        mock_serializer.assert_called_once_with(instance=mock_instance)

    def test_model_client_default(self):
        rc = clients.RestModelClient(model_class='super')
        model_client = rc.model_client(model_class='amateur')
        ok_(isinstance(model_client, clients.RestModelClient))
        eq_(model_client.model_class, 'amateur')
        eq_(rc.model_map['amateur'], model_client)

    @patch('rna.rna.clients.RestModelClient.get',
           return_value=Mock(json=lambda: {'the_dude': 'http://abid.es'}))
    def test_model_client_url_name(self, mock_get):
        rc = clients.RestModelClient()
        rc.model_map['the_dude'] = 'abides'
        model_client = rc.model_client(url_name='the_dude')
        eq_(model_client.base_url, 'http://abid.es')
        eq_(model_client.model_class, 'abides')
        eq_(rc.model_map['abides'], model_client)
        mock_get.assert_called_once_with()

    @patch('rna.rna.serializers.get_client_serializer_class')
    def test_serializer(self, mock_get_client_serializer_class):
        mock_serializer_class = Mock(return_value='mock serializer')
        mock_get_client_serializer_class.return_value = mock_serializer_class
        rc = clients.RestModelClient()
        serializer = rc.serializer(model_class='super', instance='this')
        eq_(serializer, 'mock serializer')
        mock_get_client_serializer_class.assert_called_once_with('super')
        mock_serializer_class.assert_called_once_with(instance='this')

    def test_hypermodel_exists(self):
        mock_model_class = Mock()

        rc = clients.RestModelClient()
        instance = rc.hypermodel('http://the.answ.er/is/42/', mock_model_class,
                                 False)
        eq_(instance, mock_model_class.objects.get.return_value)
        mock_model_class.objects.get.assert_called_once_with(pk='42')

    @patch('rna.rna.clients.RestModelClient.model_client')
    def test_hypermodel_does_not_exist(self, mock_model_client):
        mock_model_class = Mock()
        mock_model_class.objects.get.side_effect = ObjectDoesNotExist

        mock_model = Mock(return_value='what was the question?')
        mock_model_client.return_value = Mock(model=mock_model)

        rc = clients.RestModelClient(token='midnight')
        instance = rc.hypermodel('http://the.answ.er/is/42/', mock_model_class,
                                 False)

        eq_(instance, 'what was the question?')
        mock_model_class.objects.get.assert_called_once_with(pk='42')
        mock_model_client.assert_called_once_with(
            base_url='http://the.answ.er/is/', model_class=mock_model_class,
            token='midnight')
        mock_model.assert_called_once_with(url='42/', save=False)


class RNASyncCommandTest(TestCase):
    @patch('rna.rna.clients.LegacyRNAModelClient.__init__')
    def test_rna_client_legacy_api(self, mock_init):
        """
        Should return a LegacyRNAModelClient instance
        """
        mock_init.return_value = None
        instance = rnasync.Command().rna_client(True)
        ok_(isinstance(instance, clients.LegacyRNAModelClient))
        mock_init.assert_called_once_with()

    @patch('rna.rna.clients.RNAModelClient.__init__')
    def test_rna_client_non_legacy_api(self, mock_init):
        """
        Should return an RNAModelClient instance
        """
        mock_init.return_value = None
        instance = rnasync.Command().rna_client(False)
        ok_(isinstance(instance, clients.RNAModelClient))
        mock_init.assert_called_once_with()

    def test_model_params_legacy_api(self):
        """
        Should return mapping of models to empty dicts
        """
        models = ['model1', 'model2']
        params = rnasync.Command().model_params(models, legacy_api=True)
        eq_(params, {'model1': {}, 'model2': {}})

    def test_model_params_non_legacy_api_no_latest(self):
        """
        Should return mapping of mock_model to empty dict
        """
        legacy_api = False
        latest = Mock(side_effect=ObjectDoesNotExist)
        mock_model = Mock(objects=Mock(latest=latest))

        params = rnasync.Command().model_params([mock_model], legacy_api)

        eq_(params, {mock_model: {}})
        latest.assert_called_once_with('modified')

    def test_model_params_non_legacy_api_with_latest(self):
        """
        Should return mapping of model to query params dict with a
        'modified_after' key and a value of the latest modified datetime
        in ISO 8601 format
        """
        legacy_api = False
        mock_isoformat = lambda: '2013-10-22T22:29:03.718815'
        mock_instance = Mock(modified=Mock(isoformat=mock_isoformat))
        latest = Mock(return_value=mock_instance)
        mock_model = Mock(objects=Mock(latest=latest))

        params = rnasync.Command().model_params([mock_model], legacy_api)

        eq_(params, {mock_model: {'modified_after': mock_isoformat()}})
        latest.assert_called_once_with('modified')

    @override_settings(RNA={'LEGACY_API': True})
    @patch('rna.rna.management.commands.rnasync.Command.rna_client')
    @patch('rna.rna.management.commands.rnasync.Command.model_params')
    def test_handle(self, mock_model_params, mock_rna_client):
        mock_model = Mock()
        mock_model_client = Mock(return_value=Mock(model=mock_model))
        mock_rna_client.return_value = Mock(
            model_map={'mock_url_name': 'mock_model'},
            model_client=mock_model_client)
        params = {'modified_after': '2013-10-22T22:29:03.718815'}
        mock_model_params.return_value = {'mock_model': params}

        rnasync.Command().handle()

        mock_rna_client.assert_called_once_with(True)
        mock_model_params.assert_called_once_with(['mock_model'], True)
        mock_model_client.assert_called_once_with('mock_url_name')
        mock_model.assert_called_once_with(save=True, params=params)


class GetClientSerializerClassTest(TestCase):
    @override_settings(RNA={'LEGACY_API': False})
    def test_get_client_serializer_class(self):
        ClientSerializer = serializers.get_client_serializer_class(
            'mock_model_class')
        ok_(issubclass(ClientSerializer,
                       serializers.UnmodifiedTimestampSerializer))
        eq_(ClientSerializer.Meta.model, 'mock_model_class')

    @override_settings(RNA={'LEGACY_API': True})
    def test_get_legacy_client_serializer_class(self):
        ClientSerializer = serializers.get_client_serializer_class(
            'mock_model_class')
        ok_(issubclass(ClientSerializer,
                       serializers.serializers.ModelSerializer))
        eq_(ClientSerializer.Meta.model, 'mock_model_class')


class HyperlinkedModelSerializerWithPkFieldTest(TestCase):
    @patch('rna.rna.serializers.HyperlinkedModelSerializerWithPkField'
           '.get_field', return_value='mock field')
    @patch('rna.rna.serializers.HyperlinkedModelSerializerWithPkField'
           '.__init__', return_value=None)
    def test_get_pk_field(self, mock_init, mock_get_field):
        serializer = serializers.HyperlinkedModelSerializerWithPkField()
        eq_(serializer.get_pk_field('model_field'), 'mock field')
        mock_get_field.assert_called_once_with('model_field')


class UnmodifiedTimestampSerializerTest(TestCase):
    @patch('rna.rna.serializers.serializers.ModelSerializer.restore_object',
           return_value=Mock(created='mock datetime str'))
    @patch('rna.rna.serializers.parse_datetime',
           return_value='mock parsed datetime')
    @patch('rna.rna.serializers.UnmodifiedTimestampSerializer.__init__',
           return_value=None)
    def test_restore_object(self, mock_init, mock_parse_datetime,
                            mock_super_restore_object):
        serializer = serializers.UnmodifiedTimestampSerializer()
        obj = serializer.restore_object('attrs')
        eq_(obj.created, 'mock parsed datetime')
        mock_super_restore_object.assert_called_once_with(
            'attrs', instance=None)
        mock_parse_datetime.assert_called_once_with('mock datetime str')

    @patch('rna.rna.serializers.serializers.ModelSerializer.save_object',
           return_value='abides')
    @patch('rna.rna.serializers.UnmodifiedTimestampSerializer.__init__',
           return_value=None)
    def test_save_object(self, mock_init, mock_super_save_object):
        serializer = serializers.UnmodifiedTimestampSerializer()
        the_dude = serializer.save_object('the dude', modified=True)
        eq_(the_dude, 'abides')
        mock_super_save_object.assert_called_once_with(
            'the dude', modified=False)


class URLsTest(TestCase):
    @patch('rest_framework.routers.DefaultRouter.register')
    @patch('rest_framework.routers.DefaultRouter.urls')
    def test_urls(self, mock_urls, mock_register):
        from . import urls
        mock_register.assert_any_call('channels', views.ChannelViewSet)
        mock_register.assert_any_call('notes', views.NoteViewSet)
        mock_register.assert_any_call('products', views.ProductViewSet)
        mock_register.assert_any_call('releases', views.ReleaseViewSet)
        mock_register.assert_any_call('tags', views.TagViewSet)
        eq_(urls.urlpatterns, mock_urls)


class LegacyRNAModelTest(TestCase):
    @patch('rna.rna.clients.RNAModelClient.restore',
           return_value='restored')
    def test_restore(self, mock_super_restore):
        data = {'bug_num': 42, 'description': 'arthur dent'}
        lc = clients.LegacyRNAModelClient()
        serializer = Mock(Meta=Mock(model=models.Note))
        restored = lc.restore(serializer, data=data)
        eq_(restored, 'restored')
        mock_super_restore.assert_called_once_with(
            serializer, {'bug': 42, 'html': 'arthur dent'}, save=False,
            modified=True)
