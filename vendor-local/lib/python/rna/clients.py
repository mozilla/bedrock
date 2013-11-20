# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import requests

from . import models, serializers


class RestClient(object):
    full_url_regex = re.compile('^https?://.*')

    def __init__(self, base_url='', token='', cache=None):
        """Initialize a RestClient instance.

        Args:
            base_url (str): The full URL which all requests will
                be relative to.
                Defaults to settings.RNA['BASE_URL']
            token (str): Token to add to Authorization HTTP header.
                Defaults to settings.RNA.get('TOKEN', '')
            cache (dict): Defaults to empty dict
        """
        self.base_url = base_url or settings.RNA['BASE_URL']
        self.cache = cache or {}
        self.token = token or settings.RNA.get('TOKEN', '')

    def request(self, method, url, **kwargs):
        if self.base_url and not self.full_url_regex.match(url):
            url = self.base_url + url
        if self.token:
            kwargs.setdefault('headers', {})
            kwargs['headers'].setdefault(
                'Authorization', 'Token ' + self.token)
        return requests.request(method, url, **kwargs)

    def delete(self, url='', **kwargs):
        self.cache.pop(url, None)
        return self.request('delete', url, **kwargs)

    def get(self, url='', **kwargs):
        if kwargs.get('params', None):
            return self.request('get', url, **kwargs)
        response = self.cache.get(url)
        if not response:
            response = self.request('get', url, **kwargs)
            if response.status_code == 200:
                self.cache[url] = response
        return response

    def options(self, url='', **kwargs):
        self.cache.setdefault('OPTIONS', {})
        if url not in self.cache['OPTIONS']:
            self.cache['OPTIONS'][url] = self.request('options', url, **kwargs)
        return self.cache['OPTIONS'][url]

    def post(self, url='', data=None, **kwargs):
        self.cache.pop(url, None)
        return self.request('post', url, data=data, **kwargs)

    def put(self, url='', data=None, **kwargs):
        self.cache.pop(url, None)
        return self.request('put', url, data=data, **kwargs)


class RestModelClient(RestClient):
    model_map = {}

    def __init__(self, base_url='', token='', cache=None, model_class=None):
        self.model_class = model_class
        super(RestModelClient, self).__init__(base_url=base_url, token=token,
                                              cache=cache)

    def model(self, model_class=None, save=False, modified=False, **kwargs):
        data = self.get(**kwargs).json()
        serializer = self.serializer(model_class or self.model_class)
        if isinstance(data, list):
            return [self.restore(serializer, d, save, modified) for d in data]
        else:
            return self.restore(serializer, data, save, modified)

    def restore(self, serializer, data, save=False, modified=False):
        data.pop('url', None)
        for field in serializer.Meta.model._meta.fields:
            if isinstance(field, models.models.ForeignKey):
                url = data.pop(field.name, None)
                if url:
                    data[field.name] = self.hypermodel(url, field.rel.to, save)
        instance = serializer.restore_object(data)
        if save:
            serializer.save_object(instance, modified=modified)
        return instance

    def model_client(self, url_name='', model_class=None, **kwargs):
        #TODO: decide appropriate level of error handling for this method
        if url_name and not model_class:
            kwargs.setdefault('base_url', self.get().json()[url_name])
            model_class = self.model_map[url_name]
        model_class = model_class or self.model_class
        self.model_map.setdefault(
            model_class,
            self.__class__(model_class=model_class, **kwargs))
        return self.model_map[model_class]

    def post_instance(self, instance, url='', **kwargs):
        return self.post(url, self.serialize(instance), **kwargs)

    def put_instance(self, instance, url='', data=None, **kwargs):
        return self.put(url, self.serialize(instance), **kwargs)

    def serialize(self, instance):
        return self.serializer(instance=instance).data

    def serializer(self, model_class=None, instance=None):
        model_class = model_class or self.model_class
        return serializers.get_client_serializer_class(model_class)(
            instance=instance)

    def hypermodel(self, url, model_class, save):
        # assumes url ends in / -- probably want to make this more robust
        base_url, pk, _ = url.rsplit('/', 2)
        try:
            instance = model_class.objects.get(pk=pk)
        except ObjectDoesNotExist:
            instance = self.model_client(
                base_url=base_url + '/', model_class=model_class,
                token=self.token).model(url='%s/' % pk, save=save)
        return instance


class RNAModelClient(RestModelClient):
    model_map = {
        'channels': models.Channel,
        'notes': models.Note,
        'products': models.Product,
        'releases': models.Release,
        'tags': models.Tag}


class LegacyRNAModelClient(RNAModelClient):
    field_map = {models.Note: {'bug_num': 'bug', 'description': 'html'}}

    def restore(self, serializer, data, save=False, modified=True):
        for legacy, f in self.field_map.get(serializer.Meta.model, {}).items():
            data[f] = data.pop(legacy, None)
        return super(LegacyRNAModelClient, self).restore(
            serializer, data, save=save, modified=True)
