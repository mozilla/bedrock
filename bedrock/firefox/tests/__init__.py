# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from datetime import datetime

import rna.models
from factory import DjangoModelFactory, LazyAttribute, Sequence, SubFactory
from factory.fuzzy import FuzzyNaiveDateTime, FuzzyInteger


class ChannelFactory(DjangoModelFactory):
    FACTORY_FOR = rna.models.Channel
    name = Sequence(lambda n: 'Channel {0}'.format(n))


class ProductFactory(DjangoModelFactory):
    FACTORY_FOR = rna.models.Product
    name = Sequence(lambda n: 'Product {0}'.format(n))
    text = Sequence(lambda n: 'Text {0}'.format(n))


class ReleaseFactory(DjangoModelFactory):
    FACTORY_FOR = rna.models.Release
    product = SubFactory(ProductFactory)
    channel = SubFactory(ChannelFactory)
    version = FuzzyInteger(0)
    sub_version = 0
    release_date = FuzzyNaiveDateTime(datetime(2013, 12, 2))
    text = ''


class TagFactory(DjangoModelFactory):
    FACTORY_FOR = rna.models.Tag
    text = Sequence(lambda n: 'Tag {0}'.format(n))
    sort_num = Sequence(lambda n: n)


class NoteFactory(DjangoModelFactory):
    FACTORY_FOR = rna.models.Note
    bug = None
    html = '<p>Note!</p>'
    first_version = Sequence(lambda n: n)
    first_channel = SubFactory(ChannelFactory)
    fixed_in_version = LazyAttribute(lambda n: n.first_version + 2)
    fixed_in_channel = SubFactory(ChannelFactory)
    tag = SubFactory(TagFactory)
    product = SubFactory(ProductFactory)
    sort_num = Sequence(lambda n: n)
    fixed_in_subversion = None
