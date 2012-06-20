/**
 * Model for the items in the array in the ``students``-attribute of
 * {@link devilry_subjectadmin.model.Group}.
 */
Ext.define('devilry_subjectadmin.model.Candidate', {
    extend: 'Ext.data.Model',
    idProperty: 'student__username',
    fields: [
        {name: 'student__username',  type: 'string'},
        {name: 'candidate_id',  type: 'string'},
        {name: 'student__devilryuserprofile__full_name',  type: 'string'},
        {name: 'student__email',  type: 'string'}
    ]
});