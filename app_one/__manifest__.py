{
    "name":"App One",
    "summary":"nooooooooooo",
    "author":"yousef abdelati",
    "category":"",
    "version":"17.0.0.1.0",
    "depends":["base","sale_management","account","mail","contacts"],
    "data":[
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "views/base.xml",
        "views/property_view.xml",
        "views/owner_view.xml",
        "views/tag_view.xml",
        "views/product_template_view.xml",
        "views/res_partner_view.xml",
        "views/building_view.xml",
        "views/property_history_view.xml",
        "views/account_move_view.xml",
        "wizard/change_state_view.xml",
        "reports/property_report.xml",
        ],
    "application":True,
    "assets":{
        "web.assets_backend":["app_one/static/src/css/property.css"]
    },
}