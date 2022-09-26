# Prevalence of Psychiatric Diagnoses & Sociodemographic Correlates
Contains scripts to query MSDW2 and obtain EHR data for psychiatric patients
## Query scripts
1. `SNOMED_psych_patients_data.py`: creates csv with unique patient_ids/MRNs for those that have >= 1 diagnosis in SNOMED mental disorder concept codes 
* Input = `SNOMED_psych_codes.csv`
* Output = `SNOMED_sample_psych_MRNs.csv`
2. `ICD10_psych_patients_data.py`: creates csv with unique patient_ids/MRNs for those that have >= 1 diagnosis in ICD10 psychiatric disorder concept codes
* Input = `ICD10_Fcodes.csv`
* Output = `ICD10_sample_psych_MRNs.csv`
## Prereq files
1. `ICD10_Fcodes.csv`: queried ICD10 F0-99 values from MSDW2 containing concept id, code, and name
2. `SNOMED_psych_codes.csv`: queried mental disorder SNOMED values from MSDW2 containing concept id, code, and name