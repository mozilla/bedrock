# coding: utf8


class BedrockRouter(object):
    """A database router to use a single non-default db"""
    db_for_read = db_for_write = lambda *a, **kw: 'bedrock'
    allow_relation = allow_migrate = lambda *a, **kw: True
