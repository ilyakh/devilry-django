// Autogenerated by the dev_coreextjsmodels script. DO NOT CHANGE MANUALLY

/*******************************************************************************
 * NOTE: You will need to add the following before your application code:
 *
 *    Ext.Loader.setConfig({
 *        enabled: true,
 *        paths: {
 *            'devilry': DevilrySettings.DEVILRY_STATIC_URL + '/extjs_classes'
 *        }
 *    });
 *    Ext.syncRequire('devilry.extjshelpers.RestProxy');
 ******************************************************************************/
Ext.define('devilry.apps.examiner.simplified.SimplifiedStaticFeedback', {
    extend: 'Ext.data.Model',
    requires: ['devilry.extjshelpers.RestProxy'],
    fields: [
        {
            "type": "int", 
            "name": "id"
        }, 
        {
            "type": "auto", 
            "name": "grade"
        }, 
        {
            "type": "bool", 
            "name": "is_passing_grade"
        }, 
        {
            "type": "auto", 
            "name": "saved_by"
        }, 
        {
            "type": "date", 
            "name": "save_timestamp", 
            "dateFormat": "Y-m-d\\TH:i:s"
        }, 
        {
            "type": "auto", 
            "name": "delivery"
        }, 
        {
            "type": "auto", 
            "name": "rendered_view"
        }, 
        {
            "type": "int", 
            "name": "points"
        }, 
        {
            "type": "int", 
            "name": "delivery__deadline__assignment_group__parentnode__id"
        }, 
        {
            "type": "auto", 
            "name": "delivery__deadline__assignment_group__parentnode__short_name"
        }, 
        {
            "type": "auto", 
            "name": "delivery__deadline__assignment_group__parentnode__long_name"
        }, 
        {
            "type": "int", 
            "name": "delivery__deadline__assignment_group__parentnode__parentnode__id"
        }, 
        {
            "type": "auto", 
            "name": "delivery__deadline__assignment_group__parentnode__parentnode__short_name"
        }, 
        {
            "type": "auto", 
            "name": "delivery__deadline__assignment_group__parentnode__parentnode__long_name"
        }, 
        {
            "type": "date", 
            "name": "delivery__time_of_delivery", 
            "dateFormat": "Y-m-d\\TH:i:s"
        }, 
        {
            "type": "int", 
            "name": "delivery__number"
        }, 
        {
            "type": "auto", 
            "name": "delivery__delivered_by"
        }, 
        {
            "type": "auto", 
            "name": "delivery__deadline__assignment_group__candidates__identifier"
        }, 
        {
            "type": "auto", 
            "name": "delivery__deadline__assignment_group"
        }, 
        {
            "type": "auto", 
            "name": "delivery__deadline__assignment_group__name"
        }, 
        {
            "type": "int", 
            "name": "delivery__deadline__assignment_group__parentnode__parentnode__parentnode__id"
        }, 
        {
            "type": "auto", 
            "name": "delivery__deadline__assignment_group__parentnode__parentnode__parentnode__short_name"
        }, 
        {
            "type": "auto", 
            "name": "delivery__deadline__assignment_group__parentnode__parentnode__parentnode__long_name"
        }
    ],
    idProperty: 'id',
    proxy: {
        type: 'devilryrestproxy',
        url: '/examiner/restfulsimplifiedstaticfeedback/',
        headers: {
            'X_DEVILRY_USE_EXTJS': true
        },
        extraParams: {
            getdata_in_qrystring: true,
            result_fieldgroups: '["assignment", "period", "delivery", "candidates", "assignment_group", "subject"]'
        },
        reader: {
            type: 'json',
            root: 'items',
            totalProperty: 'total'
        },
        writer: {
            type: 'json'
        }
    }
});