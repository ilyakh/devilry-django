Ext.application({
    name: 'subjectadmin',
    appFolder: DevilrySettings.DEVILRY_STATIC_URL + '/subjectadmin/app',

    requires: [
        'guibase.Router',
        'guibase.RouteNotFound',
        'Ext.container.Viewport'
    ],

    controllers: [
        'Shortcuts',
        'Dashboard'
    ],

    launch: function() {
        this.viewport = Ext.create('Ext.container.Viewport', {
            layout: 'fit'
        });
        this.route = Ext.create('guibase.Router', this);
        this.route.add("", 'shortcutlist');
        this.route.add("/@@dashboard/shortcutlist", 'shortcutlist');
        this.route.add("/:subject/:period", 'period_show');
        this.route.add("/:subject/:period/@@edit", 'period_edit');
        this.route.add("/:subject/:period/:assignment", 'assignment_show');
        this.route.start();
    },

    dashboard: function() {
        this.setView({xtype: 'component', html: 'dashboard'});
    },

    shortcutlist: function() {
        this.setView({xtype: 'shortcutlist'});
    },

    period_show: function(route, subject, period) {
        console.log('PE', route, subject, period);
    },
    period_edit: function(route, subject, period) {
        console.log(route, subject, period);
    },

    assignment_show: function(route, subject, period, assignment) {
        console.log('Assignment', subject, period, assignment);
    },

    routeNotFound: function(route) {
        this.setView({
            xtype: 'routenotfound',
            data: {
                route: route.token
            }
        });
    },

    setView: function(component) {
        this.viewport.removeAll();
        this.viewport.add(component);
    }
});