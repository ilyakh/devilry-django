Ext.define('devilry_nodeadmin.view.nodebrowser.NodeDetailsOverview', {
    extend: 'Ext.view.View',
    alias: 'widget.nodedetailsoverview',
    cls: 'devilry_nodeadmin_nodedetailsoverview bootstrap',
    tpl: [
        '<tpl for=".">',
            '<h1>', gettext( 'About' ), ' <i>{ short_name }</i></h1>',
            '<h3>{ long_name }</h3>',
            '<div>{ subject_count } ', gettext( 'courses' ), '</div>',
            '<div>{ assignment_count } ', gettext( 'assignments' ), '</div>',
            '<hr />',
            '<tpl if="subjects.length">',
                '<h4>', gettext( "Subjects" ), ' <small>', gettext( 'on this level' ), '</small></h4>',
                '<div class="footer">',
                gettext( 'Follow these subject links to extend deadlines, alter group membership, and to get detailed summaries of particular students.' ),
                '</div>',
                    '<tpl for="subjects">',
                        '<div class="subject">',
                            '<div class="subject-name"><a href="/devilry_subjectadmin/#/subject/{ id }">{ long_name }</a></div>',
                            '<hr />',
                            '<div class="active">',
                                '<a class="period period-active" href="">', '{[this.findActive(parent.subjects.periods)]}', '</a>',
                            '</div>',
                            '<div class="inactive">',
                            '<tpl for="periods">',
                                '<a class="period  ',
                                '<tpl if="is_active">',
                                    'emphasized',
                                '</tpl>',
                                '" href="/devilry_subjectadmin/#/period/{ id }/">{ short_name }</a>',
                            '</tpl>',
                            '<a class="period period-ellipsis" href="">...</a>',
                            '</div>',
                        '</div>',
                    '</tpl>',
            '</tpl>',
        '</tpl>',
        {
            findActive: function( periods ) {
                Ext.Array.each( periods, function(e) {
                    console.log( e )
                } )
            }
        }

    ],

    itemSelector: 'li .course',

    store: 'NodeDetails'
});