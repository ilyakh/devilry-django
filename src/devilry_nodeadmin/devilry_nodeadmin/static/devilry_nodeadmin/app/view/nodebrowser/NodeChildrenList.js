Ext.define('devilry_nodeadmin.view.nodebrowser.NodeChildrenList', {
    extend: 'Ext.view.View',
    alias: 'widget.nodechildrenlist',
    cls: 'devilry_nodeadmin_nodechildrenlist bootstrap',

    store: 'NodeChildren',

    tpl: [
        '<div class="bootstrap">',
        '<tpl if="length">',
        '<h3>', gettext("Node contains"), '</h3>',
        '<tpl for=".">',
            '<div style="padding-bottom: 10px;">',
                '<a href="/devilry_nodeadmin/#/node/{ id }"><h3>',
                '<tpl for="predecessor">{ short_name }</tpl>',
                ' / { long_name }</h3>',
                '<tpl if="most_recent_start_time != null">',
                    '<div>', gettext( 'Earliest start time' ), ': ',
                        '{[this.formatDatetime(values.most_recent_start_time)]}',
                    '</div>',
                    '<tpl else>',
                    '<div>', gettext( 'Earliest start time' ), ':', gettext('none'), '</div>',
                '</tpl>',
                '</a>',
            '</div>',
        '</tpl>',
        '<tpl else>',
            '<h2><small>', gettext( 'no nodes on this level' ), '</small></h2>',
        '</tpl>',
        '</div>',
        {
            formatDatetime: function(datetime) {
                return devilry_extjsextras.DatetimeHelpers.formatDateTimeShort(datetime);
            }
        }
    ],

    itemSelector: 'div.node'
});