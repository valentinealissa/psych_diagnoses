import sys
import _scproxy  # do this ALWAYS
import pymssql
from config import config
import pandas as pd

# Connect to MSDW2
conn = pymssql.connect(server=config['caboodle']['host'], user=config['caboodle']['username'],
                       password=config['caboodle']['password'],
                       database=config['caboodle']['database'],
                       port=config['caboodle']['port'])
cursor = conn.cursor(as_dict=True)

# Psych departments
psych_SNOMED_codes = pd.read_csv('../psych_diagnoses/SNOMED_psych_codes.csv', header=0)

# creating table with the concept codes
sql_createtable = """
CREATE TABLE 
    #psych_SNOMED_codes
    (concept_code VARCHAR(256))
"""
cursor.execute(sql_createtable)

sql_insert = """
INSERT INTO
        #psych_SNOMED_codes (concept_code)
VALUES (%s);
"""
cursor.executemany(sql_insert, list(psych_SNOMED_codes['concept_code']))

# Find patient id/mrns from condition_occurrence table
MRNs_sql = """
SELECT DISTINCT c.person_id,
                p.xtn_patient_epic_mrn
FROM omop.cdm_phi.condition_occurrence_version_xtn as c
INNER JOIN omop.cdm_phi.person_version_xtn AS p ON p.person_id = c.person_id
INNER JOIN #psych_SNOMED_codes ON c.condition_concept_code=#psych_SNOMED_codes.concept_code
;
"""

# Find patient id/mrns from visit_occurrence table
# MRNs_sql = """
# SELECT DISTINCT vo.person_id, p.xtn_patient_epic_mrn
# FROM omop.cdm_phi.visit_occurrence_version_xtn AS vo
# INNER JOIN omop.cdm_phi.person_version_xtn AS p ON p.person_id = vo.person_id
# INNER JOIN omop.cdm_phi.condition_occurrence_version_xtn as c ON c.visit_occurrence_id = vo.visit_occurrence_id
# INNER JOIN #psych_SNOMED_codes ON c.condition_concept_code=#psych_SNOMED_codes.concept_code;
# """
cursor.execute(MRNs_sql)
MRNs = cursor.fetchall()
MRNs = pd.DataFrame(MRNs)
MRNs.to_csv('../output/SNOMED_sample_psych_MRNs.csv', index=False, index_label=None, header=True)

# condition occurrence (patient n = 3425187) as base:
# n = 318975 for joining by SNOMED concept code
# visit occurrence (patient n = 4282954) as base:
# n = 310087 for joining by SNOMED concept code


# # Find more info on those patients
# full_info_sql = """
# SELECT DISTINCT c.person_id,
#                 c.visit_occurrence_id,
#                 cs.xtn_department_name,
#                 vo.xtn_visit_type_source_concept_id,
#                 vo.xtn_visit_type_source_concept_code,
#                 p.xtn_patient_epic_mrn,
#                 p.xtn_birth_date,
#                 p.xtn_race_ethnicity_source_concept_code,
#                 p.xtn_race_ethnicity_source_concept_name,
#                 p.gender_source_concept_code,
#                 p.gender_source_concept_name,
#                 p.xtn_gender_identity_source_concept_code,
#                 p.xtn_gender_identity_source_concept_name,
#                 p.xtn_sexual_orientation_source_concept_code,
#                 p.xtn_sexual_orientation_source_concept_name,
#                 c.xtn_condition_status_source_concept_code,
#                 c.condition_source_concept_id,
#                 c.condition_source_concept_code,
#                 c.condition_source_concept_name,
#                 c.xtn_epic_diagnosis_id,
#                 c.condition_concept_id,
#                 c.condition_concept_code,
#                 c.condition_concept_name,
#                 c.condition_start_date,
#                 l.address_1,
#                 l.zip
# FROM omop.cdm_phi.condition_occurrence_version_xtn as c
# INNER JOIN omop.cdm_phi.person_version_xtn AS p ON p.person_id = c.person_id
# INNER JOIN omop.cdm_phi.location AS l ON l.location_id = p.location_id
# INNER JOIN omop.cdm_phi.visit_occurrence_version_xtn as vo ON vo.visit_occurrence_id = c.visit_occurrence_id
# INNER JOIN omop.cdm_phi.care_site_version_xtn AS cs ON cs.care_site_id = vo.care_site_id
# INNER JOIN #psych_SNOMED_codes ON c.condition_concept_code=#psych_SNOMED_codes.concept_code
# WHERE LOWER(c.xtn_condition_status_source_concept_code) LIKE '%Diagnosis%';
# """
# cursor.execute(full_info_sql)
# full_info = cursor.fetchall()
# full_info = pd.DataFrame(full_info)
# full_info.to_csv('../output/SNOMED_psych_patients.csv', index=False, index_label=None, header=True)

