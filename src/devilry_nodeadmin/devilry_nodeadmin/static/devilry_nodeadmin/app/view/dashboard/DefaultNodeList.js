Ext.define('devilry_nodeadmin.view.dashboard.DefaultNodeList', {
    extend: 'Ext.view.View',
    alias: 'widget.defaultnodelist',
    cls: 'devilry_nodeadmin_defaultnodelist bootstrap',

    store: 'RelatedNodes',

    tpl: [
        '<h1>',
        gettext( 'Navigate' ),
        '<a class="to-frontpage" href="/devilry_frontpage/">',
            '<i class="icon-chevron-left"></i>',
            gettext( 'Or return (to the front-page)' ),
        '</a>',
        '</h1>',
        '<hr />',
        '<tpl for=".">',
            '<a class="node" href="/devilry_nodeadmin/#/node/{ id }">{ long_name }</a>',
        '</tpl>',
        '<div class="footer">',
            '<div>',
                interpolate(gettext( 'These are only the nodes you control. Select an element to see the child levels, its %(subjects_term)s and %(periods_term)s. The menu in the upper right corner of the page will always let you navigate back and to the top of the structure.' ), {
                    subjects_term: gettext('subjects'),
                    periods_term: gettext('periods')
                 }, true),
            '</div>',
        '</div>'
    ],

    itemSelector: 'a.node'

});