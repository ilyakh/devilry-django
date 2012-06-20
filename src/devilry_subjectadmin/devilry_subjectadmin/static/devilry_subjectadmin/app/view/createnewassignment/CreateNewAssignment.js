Ext.define('devilry_subjectadmin.view.createnewassignment.CreateNewAssignment' ,{
    extend: 'Ext.panel.Panel',
    alias: 'widget.createnewassignment',
    requires: [
        'devilry_extjsextras.PrimaryButton'
    ],

    /**
     * @cfg period_id
     */

    border: 0,
    bodyPadding: 40,
    autoScroll: true,

    items: [{
        xtype: 'panel',
        ui: 'inset-header-strong-panel',
        title: gettext('Create new assignment'),
        items: { // Note: We wrap this in an extra container to avoid that the create button ends up at the bottom of the screen
            xtype: 'createnewassignmentform'
        }
    }]
});