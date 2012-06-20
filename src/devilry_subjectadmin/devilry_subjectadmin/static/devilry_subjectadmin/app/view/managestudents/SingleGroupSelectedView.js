/**
 * A panel that displays information about a single group.
 */
Ext.define('devilry_subjectadmin.view.managestudents.SingleGroupSelectedView' ,{
    extend: 'Ext.panel.Panel',
    alias: 'widget.singlegroupview',
    cls: 'singlegroupview',
    ui: 'transparentpanel',

    requires: [
        'devilry_subjectadmin.view.managestudents.StudentsInGroupGrid',
        'devilry_subjectadmin.view.managestudents.ExaminersInGroupGrid',
        'devilry_subjectadmin.view.managestudents.TagsInGroupGrid'
    ],

    /**
     * @cfg {string} multiselectHowto (required)
     */

    /**
     * @cfg {devilry_subjectadmin.model.Group} groupRecord (required)
     */

    /**
     * @cfg {Ext.data.Store} studentsStore (required)
     */

    /**
     * @cfg {Ext.data.Store} examinersStore (required)
     */

    /**
     * @cfg {Ext.data.Store} tagsStore (required)
     */

    metaInfoTpl: [
        '<dl>',
            '<dt>', dtranslate('devilry_extjsextras.grade') ,':</dt> ',
            '<dd>',
                '<tpl if="hasFeedback">',
                    '{feedback__grade} ',
                    '<tpl if="feedback__is_passing_grade"><span class="label label-success">',
                        dtranslate('devilry_extjsextras.passing_grade'),
                    '</span></tpl>',
                    '<tpl if="!feedback__is_passing_grade"><span class="label label-warning">',
                        dtranslate('devilry_extjsextras.not_passing_grade'),
                    '</span></tpl>',
                    ' <span class="label">',
                        dtranslate('devilry_extjsextras.points'), ': {feedback__points}',
                    '</span>',
                '</tpl>',
                '<tpl if="!hasFeedback"><span class="label label-info">',
                    dtranslate('devilry_extjsextras.no_feedback'),
                '</span></tpl>',
            '</dd>',

            '<dt>', Ext.String.capitalize(dtranslate('devilry_extjsextras.deliveries')) ,':</dt> ',
            '<dd>{num_deliveries}</dd>',

            '<dt>', dtranslate('devilry_extjsextras.status'), ':</dt>',
            '<dd>',
                '<tpl if="is_open">',
                    '<span class="label label-success">', dtranslate('devilry_extjsextras.open'), '</span> ',
                    dtranslate('devilry_extjsextras.open.explained'),
                '</tpl>',
                '<tpl if="!is_open">',
                    '<span class="label label-warning">', dtranslate('devilry_extjsextras.closed'), '</span> ',
                    dtranslate('devilry_extjsextras.closed.explained'),
                '</tpl>',
                ' ', dtranslate('devilry_subjectadmin.managestudents.open_close_explained_extra'),
            '</dd>',
        '</dl>'
    ],

    initComponent: function() {
        Ext.apply(this, {
            items: [{
                xtype: 'alertmessage',
                type: 'info',
                message: [this.multiselectHowto, this.multiselectWhy].join(' ')
            }, {
                xtype: 'container',
                layout: 'column',
                items: [{
                    xtype: 'container',
                    columnWidth: .63,
                    items: [{
                        xtype: 'box',
                        cls: 'bootstrap',
                        html: this._getMetaInfo()
                    }, {
                        xtype: 'box',
                        cls: 'bootstrap',
                        html: '<strong>NOTE:</strong> This view is incomplete. Please see <a href="http://heim.ifi.uio.no/espeak/devilry-figures/managestudents-singleselect.png" target="_blank">this image mockup</a> of the planned interface.'
                    }]
                }, {
                    xtype: 'container',
                    columnWidth: .37,
                    padding: {left: 20},
                    defaults: {
                        margin: {top: 20}
                    },
                    items: [{
                        xtype: 'studentsingroupgrid',
                        margin: {top: 0},
                        store: this.studentsStore
                    }, {
                        xtype: 'examinersingroupgrid',
                        store: this.examinersStore
                    }, {
                        xtype: 'tagsingroupgrid',
                        store: this.tagsStore
                    }]
                }]
            }]
        });
        this.callParent(arguments);
    },

    _getMetaInfo: function() {
        var tpl = Ext.create('Ext.XTemplate', this.metaInfoTpl);
        var data = Ext.apply({
            hasFeedback: this.groupRecord.get('feedback__save_timestamp') != null,
            passing_grade_i18n: dtranslate('devilry_extjsextras.passing_grade'),
            not_passing_grade_i18n: dtranslate('devilry_extjsextras.not_passing_grade'),
            points_i18n: dtranslate('devilry_extjsextras.points')
        }, this.groupRecord.data);
        return tpl.apply(data);
    }
});