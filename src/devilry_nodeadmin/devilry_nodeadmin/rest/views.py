# -*- coding: utf-8 -*-

from devilry.apps.core.models import Node
from djangorestframework.views import ListModelView, InstanceModelView
from djangorestframework.permissions import IsAuthenticated

from devilry_nodeadmin.rest.resources import *

from devilry_subjectadmin.rest.auth import BaseIsAdmin, nodeadmin_required



class IsNodeAdmin( BaseIsAdmin ):
    ID_KWARG = 'pk'

    def check_permission( self, user ):
        nodeid = self.get_id()
        nodeadmin_required( user, nodeid )


class RelatedNodes( ListModelView ):
    """
    All nodes where the user is either admin or superadmin
    """
    
    resource = NodeResource
    permissions = (IsAuthenticated, IsNodeAdmin, ) # [+] restrict to Admin

    def get_queryset( self ):
        nodes = Node.where_is_admin_or_superadmin( self.request.user )
        nodes = nodes.exclude( parentnode__in=nodes )
        return nodes


class RelatedNodeChildren( ListModelView ):
    resource = ChildNodeResource
    permissions = (IsAuthenticated, IsNodeAdmin, ) # [+] restrict to Admin
    allowed_methods = ('get' ,)

    def get_queryset( self ):
        nodes = Node.where_is_admin_or_superadmin( self.request.user ).filter(
            parentnode__pk=self.kwargs['parentnode__pk']
        )
        return nodes


class RelatedNodeDetails( InstanceModelView ):
    resource = NodeDetailsResource
    permissions = ( IsAuthenticated, IsNodeAdmin, )
    allowed_methods = ('get' ,)

    def get_instance_data( self, instance ):
        return instance


class Path( InstanceModelView ):
    resource = PathResource
    permissions = ( IsAuthenticated, IsNodeAdmin, )
    allowed_methods = ('get' ,)