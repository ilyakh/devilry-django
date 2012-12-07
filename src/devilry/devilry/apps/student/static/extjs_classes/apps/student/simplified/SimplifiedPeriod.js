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
Ext.define('devilry.apps.student.simplified.SimplifiedPeriod', {
    extend: 'Ext.data.Model',
    requires: ['devilry.extjshelpers.RestProxy'],
    fields: [
        {
            "type": "int", 
            "name": "id"
        }, 
        {
            "type": "auto", 
            "name": "parentnode"
        }, 
        {
            "type": "auto", 
            "name": "short_name"
        }, 
        {
            "type": "auto", 
            "name": "long_name"
        }, 
        {
            "type": "date", 
            "name": "start_time", 
            "dateFormat": "Y-m-d\\TH:i:s"
        }, 
        {
            "type": "date", 
            "name": "end_time", 
            "dateFormat": "Y-m-d\\TH:i:s"
        }, 
        {
            "type": "auto", 
            "name": "parentnode__short_name"
        }, 
        {
            "type": "auto", 
            "name": "parentnode__long_name"
        }
    ],
    idProperty: 'id',
    proxy: {
        type: 'devilryrestproxy',
        url: '/student/restfulsimplifiedperiod/',
        headers: {
            'X_DEVILRY_USE_EXTJS': true
        },
        extraParams: {
            getdata_in_qrystring: true,
            result_fieldgroups: '["subject"]'
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