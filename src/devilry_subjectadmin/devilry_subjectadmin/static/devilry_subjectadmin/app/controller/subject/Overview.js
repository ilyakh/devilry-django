/**
 * Controller for the subject overview.
 */
Ext.define('devilry_subjectadmin.controller.subject.Overview', {
    extend: 'Ext.app.Controller',
    mixins: {
        'setBreadcrumb': 'devilry_subjectadmin.utils.BasenodeBreadcrumbMixin',
        'onLoadFailure': 'devilry_subjectadmin.utils.DjangoRestframeworkLoadFailureMixin'
    },

    views: [
        'subject.Overview',
        'subject.ListOfPeriods',
        'ActionList',
        'RenameBasenodeWindow'
    ],

    stores: ['Periods'],
    models: ['Subject'],

    refs: [{
        ref: 'globalAlertmessagelist',
        selector: 'subjectoverview>alertmessagelist'
    }, {
        ref: 'deleteButton',
        selector: 'subjectoverview #deleteButton'
    }, {
        ref: 'renameButton',
        selector: 'subjectoverview #renameButton'
    }, {
        ref: 'actions',
        selector: 'subjectoverview #actions'
    }, {
        ref: 'subjectOverview',
        selector: 'subjectoverview'
    }, {
        ref: 'adminsbox',
        selector: 'subjectoverview adminsbox'
    }, {
        ref: 'basenodehierlocation',
        selector: 'subjectoverview basenodehierlocation'
    }],

    init: function() {
        this.control({
            'viewport subjectoverview': {
                render: this._onSubjectViewRender
            },
            'viewport subjectoverview editablesidebarbox[itemId=gradeeditor] button': {
                click: this._onEditGradeEditor
            },
            'viewport subjectoverview #deleteButton': {
                click: this._onNotImplemented
            },
            'viewport subjectoverview #renameButton': {
                click: this._onRenameButton
            }
        });
    },

    _onNotImplemented: function() {
        Ext.MessageBox.alert('Unavailable', 'Not implemented yet');
    },

    _onSubjectViewRender: function() {
        this.setLoadingBreadcrumb();
        this.subject_id = this.getSubjectOverview().subject_id;
        this._loadSubject(this.subject_id);
        this._loadPeriods();
    },

    _setMenuLabels: function() {
        var deleteLabel = Ext.create('Ext.XTemplate', gettext('Delete {something}')).apply({
            something: this.subjectRecord.get('short_name')
        });
        var renameLabel = Ext.create('Ext.XTemplate', gettext('Rename {something}')).apply({
            something: this.subjectRecord.get('short_name')
        });
        this.getDeleteButton().setText(deleteLabel);
        this.getRenameButton().setText(renameLabel);
    },

    _loadPeriods: function() {
        this.getPeriodsStore().loadPeriodsInSubject(this.subject_id, this._onLoadPeriods, this);
    },

    _onLoadPeriods: function(records, operation) {
        if(operation.success) {
            
        } else {
            this.onLoadFailure(operation);
        }
    },

    _loadSubject: function(subject_id) {
        this.getSubjectModel().load(subject_id, {
            scope: this,
            callback: function(record, operation) {
                if(operation.success) {
                    this._onLoadSubjectSuccess(record);
                } else {
                    this.onLoadFailure(operation);
                }
            }
        });
    },
    _onLoadSubjectSuccess: function(record) {
        this.subjectRecord = record;
        this.getActions().setTitle(record.get('long_name'));
        this.setBreadcrumb(this.subjectRecord);
        this.getAdminsbox().setBasenodeRecord(this.subjectRecord, this.subjectRecord.get('short_name'));
        this.getBasenodehierlocation().setLocation(this.subjectRecord);
        this._setMenuLabels();
    },

    _onRenameButton: function() {
        Ext.create('devilry_subjectadmin.view.RenameBasenodeWindow', {
            basenodeRecord: this.subjectRecord
        }).show();
    },
});
