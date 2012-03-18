/**
 * Subject overview (overview of an subject).
 */
Ext.define('subjectadmin.view.subject.Overview' ,{
    extend: 'Ext.panel.Panel',
    alias: 'widget.subjectoverview',
    cls: 'subjectoverview',
    requires: [
        'Ext.layout.container.Column',
        'themebase.EditableSidebarBox',
        'subjectadmin.view.ActionList',
        'themebase.AlertMessageList'
    ],


    /**
     * @cfg {String} subject_shortname (required)
     */


    initComponent: function() {
        var deleteLabel = Ext.create('Ext.XTemplate', dtranslate('themebase.delete_something')).apply({
            what: this.subject_shortname
        });
        var renameLabel = Ext.create('Ext.XTemplate', dtranslate('themebase.rename_something')).apply({
            what: this.subject_shortname
        });


        Ext.apply(this, {
            frame: false,
            border: 0,
            bodyPadding: 40,
            autoScroll: true,

            items: [{
                xtype: 'alertmessagelist'
            }, {
                xtype: 'panel',
                ui: 'transparentpanel-overflowvisible',
                layout: 'column',
                items: [{
                    xtype: 'container',
                    columnWidth: .65,
                    items: [{
                        xtype: 'panel',
                        itemId: 'actions',
                        ui: 'inset-header-strong-panel',
                        layout: 'fit',
                        items: {
                            xtype: 'listofperiods'
                        }
                    }]
                }, {
                    xtype: 'container',
                    border: false,
                    columnWidth: .35,
                    margin: {left: 40},
                    defaults: {
                        margin: {top: 20},
                    },
                    items: [{
                        xtype: 'editablesidebarbox',
                        margin: {top: 0},
                        title: dtranslate('subjectadmin.administrators')
                    }]
                }],
            }],
            dockedItems: [{
                xtype: 'toolbar',
                dock: 'top',
                padding: {left: 40, top: 1, bottom: 1, right: 40},
                items: [{
                    xtype: 'button',
                    text: 'Advanced',
                    scale: 'medium',
                    menu: [{
                        text: renameLabel,
                        listeners: {
                            scope: this,
                            click: this._notImplemented
                        }
                    }, {
                        text: deleteLabel,
                        listeners: {
                            scope: this,
                            click: this._notImplemented
                        }
                    }]
                }]
            }]
        });
        this.callParent(arguments);
    },

    _notImplemented: function() {
        Ext.MessageBox.alert('Unavailable', 'Not implemented yet');
    }
});