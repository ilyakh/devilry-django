Ext.define('devilry.gradeeditors.EditManyDraftEditorWindow', {
    extend: 'devilry.gradeeditors.DraftEditorWindow',

    config: {
        /**
         * @cfg
         * Use the administrator RESTful interface to store drafts? If this is
         * ``false``, we use the examiner RESTful interface.
         */
        isAdministrator: false,

        /**
         * @cfg
         * The data attribute of the record returned when loading the
         * grade-editor config. (Required).
         */
        gradeeditor_config: undefined,

        /**
         * @cfg
         * The data attribute of the record returned when loading the
         * grade-editor registry item. (Required).
         */
        registryitem: undefined,

        buttonText: 'Publish this feedback to all selected groups',
        buttonIcon: 'icon-add-32'
    },

    constructor: function(config) {
        this.callParent([config]);
        this.addEvents('createNewDraft');
    },

    initComponentExtra: function() {
        this.publishButton = Ext.widget('button', {
            text: this.buttonText,
            scale: 'medium',
//            iconCls: this.buttonIcon,
            listeners: {
                scope: this,
                click: this.onPublish
            }
        });
        Ext.apply(this, {
            dockedItems: [{
                xtype: 'toolbar',
                dock: 'bottom',
                ui: 'footer',
                items: ['->', this.publishButton]
            }]
        });
    },

    /**
     * @private
     *
     * Skip loading of current draft.
     */
    onLoadDraftEditorSuccess: function() {
        this.initializeDraftEditor();
    },

    /**
     * Not allowed in EditManyDraftEditorWindow.
     */
    saveDraft: function(draftstring, onFailure) {
        throw "Save draft is not allowed in EditManyDraftEditorWindow.";
    },

    /**
     * Fire createNewDraft event with the draft string as argument.
     *
     * @param draftstring The draftstring.
     */
    saveDraftAndPublish: function(draftstring, onFailure) {
        this.fireEvent('createNewDraft', this.getSimplifiedFeedbackDraftModelName(), draftstring);
        this.exit();
    }
});
