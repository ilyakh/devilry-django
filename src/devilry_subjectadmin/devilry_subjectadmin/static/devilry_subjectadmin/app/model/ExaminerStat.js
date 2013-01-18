Ext.define('devilry_subjectadmin.model.ExaminerStat', {
    extend: 'Ext.data.Model',

    idProperty: 'id',
    fields: [
        {name: 'id', type: 'int'},
        {name: 'examiner', type: 'auto'},
        
        {name: 'waitingfordeliveries_count', type: 'int'},
        {name: 'waitingforfeedback_count', type: 'int'},
        {name: 'nodeadlines_count', type: 'int'},
        {name: 'closedwithoutfeedback_count', type: 'int'},
        {name: 'failed_count', type: 'int'},
        {name: 'passed_count', type: 'int'},
        {name: 'corrected_count', type: 'int'},
        
        {name: 'waitingfordeliveries_percent', type: 'int'},
        {name: 'waitingforfeedback_percent', type: 'int'},
        {name: 'nodeadlines_percent', type: 'int'},
        {name: 'closedwithoutfeedback_percent', type: 'int'},
        {name: 'failed_percent', type: 'int'},
        {name: 'passed_percent', type: 'int'},
        {name: 'corrected_percent', type: 'int'},
        
        {name: 'points_best', type: 'int'},
        {name: 'points_worst', type: 'int'},
        {name: 'points_avg', type: 'int'},
        {name: 'feedback_words_avg', type: 'int'},
        {name: 'groups', type: 'auto'}
    ],

    proxy: {
        type: 'rest',
        urlpatt: DevilrySettings.DEVILRY_URLPATH_PREFIX + '/devilry_subjectadmin/rest/examinerstats/{0}',
        url: null,
        extraParams: {
            format: 'json'
        },
        reader: {
            type: 'json'
        },

        setUrl: function(assignment_id) {
            this.url = Ext.String.format(this.urlpatt, assignment_id);
        }
    }
});