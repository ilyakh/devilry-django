# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.i18n import javascript_catalog
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

from devilry_settings.i18n import get_javascript_catalog_packages

from devilry_nodeadmin.util import emptyview, Out
from devilry_nodeadmin.views import AppView

i18n_packages = get_javascript_catalog_packages(
    'devilry_nodeadmin',
    'devilry_header', 
    'devilry_extjsextras', 
    'devilry.apps.core'
)

urlpatterns = patterns('devilry_nodeadmin',

    url('^$',
        login_required(csrf_protect(ensure_csrf_cookie(AppView.as_view()))),
            name='devilry_nodeadmin'),
    url('^i18n.js$', javascript_catalog, 
        kwargs={'packages': i18n_packages}, 
        name='devilry_nodeadmin_i18n'),
    url('^emptyview$', Out() ),
    url('^rest/', include('devilry_nodeadmin.rest.urls') )
)
