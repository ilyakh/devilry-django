from django.conf.urls.defaults import patterns, url

from .rest import ListHelpLinks

urlpatterns = patterns('devilry_usersearch',
                       url(r'^helplinks/$', ListHelpLinks.as_view()),
                      )

