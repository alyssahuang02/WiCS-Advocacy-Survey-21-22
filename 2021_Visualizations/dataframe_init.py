# initializing dataframes

import constants as C

import pandas as pd
from datetime import datetime

from pie_charts import filter_df


RAW_DF = pd.read_csv('surveyresponses2021UPDATED.csv')
pd.options.mode.chained_assignment = None

# Data cleaning
CLEAN_DF = RAW_DF.drop(columns=C.DROP_COLUMNS)
QUESTION_KEY = CLEAN_DF.drop(range(1, CLEAN_DF.shape[0])).to_dict()
CLEAN_DF = CLEAN_DF.drop([0, 1])
DATETIME_COL = pd.to_datetime(CLEAN_DF['Q2'], errors='coerce')
DATETIME_COL[DATETIME_COL.isna()] = pd.to_datetime(CLEAN_DF['Q2'][DATETIME_COL.isna()], format='%M/%y')
CLEAN_DF['Q2_DT'] = DATETIME_COL
CLEAN_DF = CLEAN_DF[(datetime(2021, 9, 1) <= CLEAN_DF['Q2_DT']) & (CLEAN_DF['Q2_DT'] <= datetime(2026, 8, 31))]

# Filter methods

def filter_gender(df, c):
    if c == 'Male':
        return filter_male(df)
    if c == 'Non-male':
        return filter_non_male(df)
    return df

def filter_male(df):
    return df[df['Q30'].isin(C.MALE)]

def filter_non_male(df):
    return df[df['Q30'].isin(C.NONMALE)]

def filter_race_ethnicity(df, c):
    if c == 'Asian':
        return filter_asian(df)
    if c == 'Black or African American':
        return filter_black(df)
    if c == 'Hispanic or Latinx':
        return filter_hispanic(df)
    if c == 'White':
        return filter_white(df)
    return df

def filter_asian(df):
    return df[df['Q33'].str.contains('Asian', na=False)]

def filter_black(df):
    return df[df['Q33'].str.contains('Black or African American', na=False)]

def filter_hispanic(df):
    return df[df['Q34'] == 'Yes, of Hispanic or Latinx origin']

def filter_white(df):
    return df[df['Q33'].str.contains('White', na=False)]

def filter_urm(df):
    return df[(df['Q33'].str.contains('Black or African American', na=False)) | (df['Q34'] == 'Yes, of Hispanic or Latinx origin')]

def filter_non_urm(df):
    return df[(df['Q33'].str.contains('White', na=False)) | (df['Q33'].str.contains('Asian', na=False))]

def filter_bgltq(df, c):
    if c == 'BGLTQ+':
        return filter_is_bgltq(df)
    if c == 'Non-BGLTQ+':
        return filter_is_non_bgltq(df)
    return df

def filter_is_bgltq(df):
    return df[df['Q32'].isin(C.NONSTRAIGHT)]

def filter_is_non_bgltq(df):
    return df[df['Q32'].isin(C.STRAIGHT)]

def filter_fgli(df, c):
    if c == 'FGLI':
        return filter_is_fgli(df)
    if c == 'Non-FGLI':
        return filter_is_non_fgli(df)
    return df

def filter_is_fgli(df):
    return df[(df['Q35'] == 'Yes') | (df['Q35'] == 'Yes')]

def filter_is_non_fgli(df):
    return df[(df['Q35'] == 'No') & (df['Q35'] == 'No')]

def filter_diagnosed(df, c):
    if c == 'Diagnosed':
        return filter_is_diagnosed(df)
    if c == 'Non-Diagnosed':
        return filter_is_non_diagnosed(df)
    return df

def filter_is_diagnosed(df):
    return df[df['Q37'].isin(C.DIAGNOSED)]

def filter_is_non_diagnosed(df):
    return df[df['Q37'].isin(C.NONDIAGNOSED)]

def filter_class_year(df, c):
    if c == 'First-year':
        return filter_firstyear(df)
    if c == 'Sophomore':
        return filter_sophomore(df)
    if c == 'Junior':
        return filter_junior(df)
    if c == 'Senior':
        return filter_senior(df)
    return df

def filter_firstyear(df):
    return df[(datetime(2024, 9, 1) <= CLEAN_DF['Q2_DT']) & (CLEAN_DF['Q2_DT'] <= datetime(2025, 8, 31))]

def filter_sophomore(df):
    return df[(datetime(2023, 9, 1) <= CLEAN_DF['Q2_DT']) & (CLEAN_DF['Q2_DT'] <= datetime(2024, 8, 31))]

def filter_junior(df):
    return df[(datetime(2022, 9, 1) <= CLEAN_DF['Q2_DT']) & (CLEAN_DF['Q2_DT'] <= datetime(2023, 8, 31))]

def filter_senior(df):
    return df[(datetime(2021, 9, 1) <= CLEAN_DF['Q2_DT']) & (CLEAN_DF['Q2_DT'] <= datetime(2022, 8, 31))]

def filter_school(df, c):
    if c == 'SEAS':
        return df[df['Q1'].isin(C.SEAS)]
    elif c == 'All':
        return df
    return df[(df['Q1'].isin(C.ARTS_HUMANITIES)) | (df['Q1'].isin(C.SOCIAL_SCIENCES)) | (df['Q1'].isin(C.PURE_SCIENCES))]

# def filter_school(df, c):
#     if c == 'Arts and Humanities':
#         return filter_arts_humanitites(df)
#     if c == 'Social Sciences':
#         return filter_social_sciences(df)
#     if c == 'Pure Sciences':
#         return filter_pure_sciences(df)
#     if c == 'Engineering and Applied Sciences':
#         return filter_seas(df)
#     return df

# def filter_arts_humanitites(df):
#     return df[df['Q1'].isin(C.ARTS_HUMANITIES)]

# def filter_social_sciences(df):
#     return df[df['Q1'].isin(C.SOCIAL_SCIENCES)]

# def filter_pure_sciences(df):
#     return df[df['Q1'].isin(C.PURE_SCIENCES)]

# def filter_seas(df):
#     return df[df['Q1'].isin(C.SEAS)]

def filter_conc(df, c):
    if c == 'Computer Science':
        return filter_cs_conc(df)
    return df

def filter_cs_conc(df):
    return df[df['Q1'] == 'Computer Science']


# Create dataframe per axis

# Gender
MALE_DF = filter_male(CLEAN_DF)
MALE_DF['Gender'] = 'Male'
NON_MALE_DF = filter_non_male(CLEAN_DF)
NON_MALE_DF['Gender'] = 'Non-male'
GENDER_DF = pd.concat([MALE_DF, NON_MALE_DF], ignore_index=True, sort=False)
GENDER_DF = GENDER_DF[GENDER_DF['Gender'].isin(C.GENDER_CATEGORIES)]

# Race/Ethnicity
# ASIAN_DF = filter_asian(CLEAN_DF)
# ASIAN_DF['Race/Ethnicity'] = 'Asian'
# BLACK_DF = filter_black(CLEAN_DF)
# BLACK_DF['Race/Ethnicity'] = 'Black or African American'
# HISPANIC_DF = filter_hispanic(CLEAN_DF)
# HISPANIC_DF['Race/Ethnicity'] = 'Hispanic or Latinx'
# WHITE_DF = filter_white(CLEAN_DF)
# WHITE_DF['Race/Ethnicity'] = 'White'
# RACE_ETHNICITY_DF = pd.concat([ASIAN_DF, BLACK_DF, HISPANIC_DF, WHITE_DF], ignore_index=True, sort=False)

URM_DF = filter_urm(CLEAN_DF)
URM_DF['Race/Ethnicity'] = 'URM'
NON_URM_DF = filter_non_urm(CLEAN_DF)
NON_URM_DF['Race/Ethnicity'] = 'Non-URM'
RACE_ETHNICITY_DF = pd.concat([URM_DF, NON_URM_DF], ignore_index=True, sort=False)
RACE_ETHNICITY_DF = RACE_ETHNICITY_DF[RACE_ETHNICITY_DF['Race/Ethnicity'].isin(C.RACE_ETHNICITY_CATEGORIES)]

# BGLTQ+
IS_BGLTQ_DF = filter_is_bgltq(CLEAN_DF)
IS_BGLTQ_DF['BGLTQ+'] = 'BGLTQ+'
IS_NOT_BGLTQ_DF = filter_is_non_bgltq(CLEAN_DF)
IS_NOT_BGLTQ_DF['BGLTQ+'] = 'Non-BGLTQ+'
BGLTQ_DF = pd.concat([IS_BGLTQ_DF, IS_NOT_BGLTQ_DF], ignore_index=True, sort=False)
BGLTQ_DF = BGLTQ_DF[BGLTQ_DF['BGLTQ+'].isin(C.BGLTQ_CATEGORIES)]

# FGLI
IS_FGLI_DF = filter_is_fgli(CLEAN_DF)
IS_FGLI_DF['FGLI'] = 'FGLI'
IS_NOT_FGLI_DF = filter_is_non_fgli(CLEAN_DF)
IS_NOT_FGLI_DF['FGLI'] = 'Non-FGLI'
FGLI_DF = pd.concat([IS_FGLI_DF, IS_NOT_FGLI_DF], ignore_index=True, sort=False)
FGLI_DF = FGLI_DF[FGLI_DF['FGLI'].isin(C.FGLI_CATEGORIES)]

# Class Year
FIRSTYEAR_DF = filter_firstyear(CLEAN_DF)
FIRSTYEAR_DF['Class Year'] = 'First-year'
SOPHOMORE_DF = filter_sophomore(CLEAN_DF)
SOPHOMORE_DF['Class Year'] = 'Sophomore'
JUNIOR_DF = filter_junior(CLEAN_DF)
JUNIOR_DF['Class Year'] = 'Junior'
SENIOR_DF = filter_senior(CLEAN_DF)
SENIOR_DF['Class Year'] = 'Senior'
CLASS_YEAR_DF = pd.concat([FIRSTYEAR_DF, SOPHOMORE_DF, JUNIOR_DF, SENIOR_DF], ignore_index=True, sort=False)
CLASS_YEAR_DF = CLASS_YEAR_DF[CLASS_YEAR_DF['Class Year'].isin(C.CLASS_YEAR_CATEGORIES)]

# School
# ARTS_HUMANITIES_DF = filter_arts_humanitites(CLEAN_DF)
# ARTS_HUMANITIES_DF['School'] = 'Arts and Humanities'
# SOCIAL_SCIENCES_DF = filter_social_sciences(CLEAN_DF)
# SOCIAL_SCIENCES_DF['School'] = 'Social Sciences'
# PURE_SCIENCES_DF = filter_pure_sciences(CLEAN_DF)
# PURE_SCIENCES_DF['School'] = 'Pure Sciences'
# SEAS_DF = filter_seas(CLEAN_DF)
# SEAS_DF['School'] = 'Engineering and Applied Sciences'
# SCHOOL_DF = pd.concat([ARTS_HUMANITIES_DF, SOCIAL_SCIENCES_DF, PURE_SCIENCES_DF, SEAS_DF], ignore_index=True, sort=False)
# SCHOOL_DF = SCHOOL_DF[SCHOOL_DF['School'].isin(C.SCHOOL_CATEGORIES)]

SEAS_DF = filter_school(CLEAN_DF, 'SEAS')
SEAS_DF['School'] = 'SEAS'
NON_SEAS_DF = filter_school(CLEAN_DF, 'Other')
NON_SEAS_DF['School'] = 'Non-SEAS'
SCHOOL_DF = pd.concat([SEAS_DF, NON_SEAS_DF], ignore_index=True, sort=False)
SCHOOL_DF = SCHOOL_DF[SCHOOL_DF['School'].isin(C.SCHOOL_CATEGORIES)]

# Disability
IS_DIAGNOSED_DF = filter_is_diagnosed(CLEAN_DF)
IS_DIAGNOSED_DF['Disability'] = 'Disability'
IS_NOT_DIAGNOSED_DF = filter_is_non_diagnosed(CLEAN_DF)
IS_NOT_DIAGNOSED_DF['Disability'] = 'Non-Disability'
DISABILITY_DF = pd.concat([IS_DIAGNOSED_DF, IS_NOT_DIAGNOSED_DF], ignore_index=True, sort=False)
DISABILITY_DF = DISABILITY_DF[DISABILITY_DF['Disability'].isin(C.DISABILITY_CATEGORIES)]

#print(SCHOOL_DF)
AXIS_DF = {
    'Gender' : GENDER_DF,
    'Race/Ethnicity' : RACE_ETHNICITY_DF,
    'BGLTQ+' : BGLTQ_DF,
    'FGLI' : FGLI_DF,
    'Class Year' : CLASS_YEAR_DF,
    'School' : SCHOOL_DF,
    'Disability': DISABILITY_DF
}