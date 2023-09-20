{
    'name': 'Airport Medical Visit',
    'version': '1.0.1',
    'category': 'Industries',
    'summary': 'Manage airport medical visit',
    'description': 'A module for airport medical visit.',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/hospital_groups.xml',
        'views/airport_medical_identity_views.xml',
        'views/airport_medical_sex_views.xml',
        'views/airport_medical_come_views.xml',
        'views/airport_medical_comment_views.xml',
        'views/airport_medical_nationality_views.xml',
        'views/airport_medical_race_views.xml',
        'views/airport_medical_company_views.xml',
        'views/airport_medical_departure_views.xml',
        'views/airport_medical_arrival_views.xml',
        'views/airport_medical_incident_place_views.xml',
        'views/airport_medical_incident_time_views.xml',
        'views/airport_medical_chief_complaint_views.xml',
        'views/airport_medical_diagnosis_views.xml',
        'views/airport_medical_treatment_views.xml',
        'views/airport_medical_result_views.xml',
        'views/airport_medical_treatment_hospital_views.xml',
        'views/airport_medical_attending_physician_views.xml',
        'views/airport_medical_attending_nurse_views.xml',
        'views/airport_medical_views.xml',
        'views/airport_medical_reporting_views.xml',
        'views/airport_menus.xml',
        'views/airport_medical_passing_views.xml',
        'views/airport_medical_exit_views.xml',
        'views/airport_medical_icd10_category_views.xml',
        'views/airport_medical_icd10_category1_views.xml',
        'views/airport_medical_icd10_category2_views.xml',
        'views/airport_medical_icd10_category3_views.xml',
        'views/airport_medical_icd10_category4_views.xml',
        'views/airport_medical_icd10_category5_views.xml',
        'views/airport_medical_icd10_category6_views.xml',
        'views/airport_medical_icd10_category7_views.xml',
        'views/airport_medical_icd10_category8_views.xml',
        'views/airport_medical_icd10_category9_views.xml',
        'views/airport_medical_icd10_category10_views.xml',
        'views/airport_medical_icd10_category11_views.xml',
        'views/airport_medical_icd10_category12_views.xml',
        'views/airport_medical_icd10_category13_views.xml',
        'views/airport_medical_icd10_category18_views.xml',
        'wizard/image_capture_views.xml',
        'report/airport_medical_reports.xml',
        'report/airport_medical_templates.xml',
        'data/airport.medical.identity.csv',
        'data/airport.medical.sex.csv',
        'data/airport.medical.come.csv',
        'data/airport.medical.comment.csv',
        'data/airport.medical.nationality.csv',
        'data/airport.medical.race.csv',
        'data/airport.medical.company.csv',
        'data/airport.medical.departure.csv',
        'data/airport.medical.arrival.csv',
        'data/airport.medical.incident.place.csv',
        'data/airport.medical.incident.time.csv',
        'data/airport.medical.chief.complaint.csv',
        'data/airport.medical.diagnosis.csv',
        'data/airport.medical.treatment.csv',
        'data/airport.medical.result.csv',
        'data/airport.medical.treatment.hospital.csv',
        'data/airport.medical.attending.physician.csv',
        'data/airport.medical.attending.nurse.csv',
        'data/airport.medical.passing.csv',
        'data/airport.medical.exit.csv',
        'data/airport.medical.icd10.category.csv',
        'data/airport.medical.icd10.category1.csv',
        'data/airport.medical.icd10.csv',
        'data/airport.medical.icd10.category3.csv',
        'data/airport.medical.icd10.category4.csv',
        'data/airport.medical.icd10.category5.csv',
        'data/airport.medical.icd10.category6.csv',
        'data/airport.medical.icd10.category7.csv',
        'data/airport.medical.icd10.category8.csv',
        'data/airport.medical.icd10.category9.csv',
        'data/airport.medical.icd10.category10.csv',
        'data/airport.medical.icd10.category18.csv',
       
    ],
    'assets': {
        'web.assets_backend': [
            '/airport/static/src/scss/image_capture.scss',
            '/airport/static/src/js/image_capture.js',
            '/airport/static/src/js/image_upload.js',
            '/airport/static/src/xml/image_capture_templates.xml',
        ],
    },
    'application': True,
}