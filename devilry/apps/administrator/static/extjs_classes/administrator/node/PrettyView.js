Ext.define('devilry.administrator.node.PrettyView', {
    extend: 'devilry.administrator.PrettyView',
    alias: 'widget.administrator_nodeprettyview',

    requires: [
        'devilry.administrator.activeperiods.Overview'
    ],

    bodyTpl: Ext.create('Ext.XTemplate',
        '<div class="section help">',
        '    <h1>What is a node?</h1>',
        '    <p>',
        '        A Node is a place to organise top-level administrators (administrators responsible for more than one subject).',
        '        Nodes are organised in a tree. This is very flexible, and can be used to emulate most administrative hierarchies.',
        '    </p>',
        '</div>'
    ),

    initComponent: function() {
        Ext.apply(this, {
            relatedButtons: [{
                xtype: 'button',
                scale: 'large',
                text: 'Overview of active periods/semesters',
                listeners: {
                    scope: this,
                    click: this._onActivePeriods
                }
            }]
        });
        this.callParent(arguments);
    },

    _onActivePeriods: function() {
        var node = this.record;
        var win = Ext.widget('window', {
            title: Ext.String.format('Overview of active periods/semesters on {0}', node.get('long_name')),
            modal: true,
            width: 400,
            height: 500,
            maximizable: true,
            layout: 'fit',
            items: {
                xtype: 'activeperiods-overview',
                node: node
            }
        });
        win.show();
    }
});
