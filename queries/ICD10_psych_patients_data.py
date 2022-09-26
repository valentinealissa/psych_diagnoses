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
ICD10_Fcodes = pd.read_csv('../psych_diagnoses/ICD10_Fcodes.csv', header=0)

# create table with the concept codes
sql_createtable = """
CREATE TABLE 
    #ICD10_Fcodes
    (concept_code VARCHAR(50))
"""
cursor.execute(sql_createtable)

sql_insert = """
INSERT INTO
        #ICD10_Fcodes (concept_code)
VALUES (%s);
"""
cursor.executemany(sql_insert, list(ICD10_Fcodes['concept_code']))

# Find patient id/mrns
MRNs_sql = """
SELECT DISTINCT vo.person_id,
                p.xtn_patient_epic_mrn,
                c.condition_concept_code
FROM omop.cdm_phi.visit_occurrence_version_xtn AS vo
INNER JOIN omop.cdm_phi.person_version_xtn AS p ON p.person_id = vo.person_id
INNER JOIN omop.cdm_phi.condition_occurrence_version_xtn as c ON c.visit_occurrence_id = vo.visit_occurrence_id
WHERE c.condition_concept_code LIKE '%F%';
"""
# INNER JOIN #ICD10_Fcodes ON c.condition_concept_code=#ICD10_Fcodes.concept_code
cursor.execute(MRNs_sql)
MRNs = cursor.fetchall()
MRNs = pd.DataFrame(MRNs)
MRNs.to_csv('../output/ICD10_sample_psych_MRNs.csv', index=False, index_label=None, header=True)

