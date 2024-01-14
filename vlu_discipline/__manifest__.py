{
    'name': 'Văn Lang University',
    'version': '1.0',
    'description': 'Current does\'n DNS',
    'summary': 'Research Science Of Faculty Technical',
    'author': 'Bùi Đức Tuấn',
    'website': '103.79.143.198:8069',
    'license': 'LGPL-3',
    'category': 'Văn Lang/Văn Lang',
    'depends': [
        'base', 'mail', 'sign',
    ],
    'data': [
        # ============================================================
        # DATA
        # ============================================================
        'data/vlu_discipline_template.xml',
        # ============================================================
        # SECURITY SETTING - GROUP - PROFILE
        # ============================================================
        'security/vlu_discipline_group.xml',
        'security/vlu_discipline_rule.xml',
        'security/ir.model.access.csv',
        # ============================================================
        # WIZARDS
        # ============================================================

        # ============================================================
        # VIEWS
        # ============================================================
        'views/tags_views.xml',
        'views/majors_views.xml',
        'views/classes_views.xml',
        'views/discipline_type_views.xml',
        'views/semester_views.xml',
        'views/res_partner_views.xml',
        'views/discipline_views.xml',
        'views/discipline_line_views.xml',
        'views/res_config_settings_views.xml',
        'views/res_users_views.xml',
        #'views/discipline_study_plan_views.xml',
        # ============================================================
        # REPORT
        # ============================================================
        'report/template.xml',
        'report/format.xml',
        'report/report.xml',
        # ============================================================
        # MENU
        # ============================================================
        'data/vlu_discipline_action.xml',
        'data/vlu_discipline_menu.xml',
        'data/vlu_discipline_sequence.xml',
        # ============================================================
        # FUNCTION USED TO UPDATE DATA LIKE POST OBJECT
        # ============================================================
    ],
    'assets': {
        'web.assets_backend': [
            #'vlu_discipline/static/src/js/action_manager.js',
        ],
    }
    ,
    'demo': [
    ],
    'auto_install': False,
    'application': True,
}
