from django.conf import settings


_registry = {}

def register(view, model_cls, label, description,
        admin_url_callback=None, xmlrpc_gradeconf=None):
    r = RegistryItem(view, model_cls, label, description,
            admin_url_callback, xmlrpc_gradeconf)
    _registry[r.get_key()] = r

def getitem(key):
    return _registry[key]

def getdefaultkey():
    return settings.DEVILRY_DEFAULT_GRADEPLUGIN


class RegistryItem(object):
    """ Information about a grade plugin.
    
    .. attribute:: model_cls::

        A class for storing grades.
    """
    def __init__(self, view, model_cls, label, description,
            admin_url_callback, xmlrpc_gradeconf=None):
        self.view = view
        self.xmlrpc_gradeconf = xmlrpc_gradeconf
        self.model_cls = model_cls
        self.label = label
        self.description = description
        self.admin_url_callback = admin_url_callback

    def get_key(self):
        meta = self.model_cls._meta
        return '%s:%s' % (meta.app_label, meta.module_name)

    def __str__(self):
        return self.label


class RegistryIterator(object):
    """ Iterator over the gradeplugin-registry yielding (key, RegistryItem).
    The iterator is sorted by :attr:`RegistryItem.label`. """
    def __iter__(self):
        values = _registry.values()
        values.sort(key=lambda i: i.label)
        for v in values:
            yield (v.get_key(), v)
