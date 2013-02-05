# -*- coding: utf-8 -*-

from devilry.apps.core.models import Node, Subject, Period

from djangorestframework.resources import ModelResource
from django.db.models import Count, Max


class NodeResource( ModelResource ):
    model = Node
    fields = (  'id', 'short_name', 'long_name',
                'etag', 'predecessor', 'children', 'most_recent_start_time', )
    allowed_methods = ('get' ,)

    def most_recent_start_time( self, instance ):
        # [/] strftime
        # [!] needs a good way of collecting the most recent period
        # that on a later stage can be developed into an ordering operator
        result = Period.objects.filter( parentnode__parentnode=instance ).\
        aggregate( Max( 'start_time' )  )
        return result['start_time__max']

    # Hierarchy data

    def predecessor( self, instance ):
        parent_serializer = ParentNodeResource()
        return parent_serializer.serialize( instance.parentnode )

    def children( self, instance ):
        child_serializer = ChildNodeResource()
        candidates = Node.objects.filter( parentnode=instance )
        return child_serializer.serialize_iter( candidates )


class ChildNodeResource( NodeResource ):
    model = Node
    fields = (  'id', 'short_name', 'long_name', 'predecessor', 'most_recent_start_time', )


class ParentNodeResource( NodeResource ):
    model = Node
    fields = (  'id', 'short_name', 'long_name',  )


class PeriodResource( ModelResource ):
    model = Period
    fields = ( 'id', 'short_name', 'is_active', )

    def is_active( self, instance ):
        return ( instance in Period.objects.filter( Period.q_is_active() ) )

class NodeSubjectResource( ModelResource ):
    model = Subject
    fields = ( 'id', 'short_name', 'long_name', 'periods', )

    def periods( self, instance ):
        # [+] reverse the order
        # [+] mark as active/inactive

        resource = PeriodResource()
        periods = Period.objects.filter( parentnode=instance )
        return resource.serialize_iter( periods )


class NodeDetailsResource( NodeResource ):
    model = Node
    fields = (  'id', 'short_name', 'long_name', 'predecessor', 'etag',
                'subject_count', 'assignment_count', 'period_count', 'subjects', 'breadcrumbs', 'path', )

    def subjects( self, instance ):
        resource = NodeSubjectResource()
        subjects = Subject.objects.filter( parentnode=instance )
        return resource.serialize_iter( subjects )

    # stats
    def subject_count( self, instance ):
        # [?] does it make recursive calls to the top of the hierarchy? accumulates the sum of all subjects?
        return instance.subjects.count()

    def assignment_count( self, instance ):
        # [?] same problem as the previous method? does it make recursive calls downward the tree?
        result = Period.objects.filter( parentnode__parentnode=instance ).\
        aggregate( Count('assignments')  )
        return result['assignments__count']

    def period_count( self, instance ):
        # [?] downward-recursive?
        result = instance.subjects.all().aggregate( Count('periods') )
        return result['periods__count']

    def path( self, instance ):
        PATH_MAX_LENGTH = 8

        path = []
        counter = 1
        candidate = instance
        candidates = Node.where_is_admin_or_superadmin( self.view.request.user )

        while candidate in candidates and counter < PATH_MAX_LENGTH:
            path.append( candidate )
            candidate = candidate.parentnode
            counter += 1

        path.reverse()

        serializer = PathElementResource()

        return serializer.serialize_iter( path )


# Paths for breadcrumbs

class PathResource( ModelResource ):
    model = Node
    fields = ( 'id', 'path', )

    def path( self, instance ):
        PATH_MAX_LENGTH = 8

        path = []
        counter = 1
        candidate = instance
        candidates = Node.where_is_admin_or_superadmin( self.view.request.user )

        while candidate in candidates and counter < PATH_MAX_LENGTH:
            path.append( candidate )
            candidate = candidate.parentnode
            counter += 1

        path.reverse()

        serializer = PathElementResource()

        return serializer.serialize_iter( path )


class PathElementResource( ModelResource ):
    model = Node
    fields = ( 'id', 'short_name', )