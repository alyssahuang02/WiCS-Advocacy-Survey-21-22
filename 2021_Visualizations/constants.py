# CONSTANTS

# Minimum sample size
MIN_SAMPLE_SIZE = 5

# Drop columns
DROP_COLUMNS = ['StartDate', 'EndDate', 'Status', 'Progress', 'Duration (in seconds)', 'Finished', 'RecordedDate', 'ResponseId', 'DistributionChannel', 'UserLanguage']

# Schools
ARTS_HUMANITIES = ['Art, Film, and Visual Studies', 'Classics', 'Comparative Literature', 'East Asian Studies', 'English', 'Folklore and Mythology', 'Germanic Languages and Literatures', 'History and Literature', 'History of Art and Architecture', 'Linguistics', 'Music', 'Near Eastern Languages and Civilizations', 'Philosophy', 'Religion, Comparative Study of', 'Romance Languages and Literatures', 'Slavic Languages and Literatures', 'South Asian Studies', 'Theater, Dance, & Media']
SOCIAL_SCIENCES = ['African and African American Studies', 'Anthropology', 'Economics', 'Environmental Science and Public Policy', 'Government', 'History', 'History and Science', 'Psychology', 'Social Studies', 'Sociology', 'Women, Gender, and Sexuality, Study of']
PURE_SCIENCES = ['Astrophysics', 'Chemical and Physical Biology', 'Chemistry', 'Chemistry and Physics', 'Earth and Planetary Sciences', 'Human Developmental and Regenerative Biology', 'Human Evolutionary Biology', 'Integrative Biology', 'Mathematics', 'Molecular and Cellular Biology', 'Neuroscience', 'Physics', 'Statistics']
SEAS = ['Applied Mathematics', 'Biomedical Engineering', 'Computer Science', 'Electrical Engineering', 'Engineering Sciences', 'Environmental Science and Engineering', 'Mechanical Engineering']
UNDECIDED = ['Undecided']
NONE = ['None']

# Gender identity
MALE = ['Man']
NONMALE = ['Woman', 'Non-binary']

# Sexual orientation
STRAIGHT = ['Straight/Heterosexual']
NONSTRAIGHT = ['Queer', 'Questioning or unsure']

# Diagnosed with disability/impairment
DIAGNOSED = ['Yes, I have been diagnosed with a disability or impairment']
NONDIAGNOSED = ['No, I have not been diagnosed with a disability or impairment']

# Likert scales
LIKERT_KNOWLEDGE_KEY = {
    'Significantly less knowledgeable' : 1,
    'Less knowledgeable' : 2,
    'Slightly less knowledgeable' : 3,
    'Similarly knowledgeable' : 4,
    'Slightly more knowledgeable' : 5,
    'More knowledgeable' : 6,
    'Significantly more knowledgeable' : 7
}

LIKERT_AGREEMENT_KEY = {
    'Strongly disagree' : 1,
    'Disagree' : 2,
    'Somewhat disagree' : 3,
    'Neither agree nor disagree' : 4,
    'Somewhat agree' : 5,
    'Agree' : 6,
    'Strongly agree' : 7
}

# Axes
VIZ_AXES = ['Gender', 'Race/Ethnicity', 'BGLTQ+', 'FGLI', 'Class Year', 'School', 'Disability']

# Axes categories
GENDER_CATEGORIES = ['Male', 'Non-male']
#RACE_ETHNICITY_CATEGORIES = ['Asian', 'Black or African American', 'Hispanic or Latinx', 'White']
RACE_ETHNICITY_CATEGORIES = ['URM', 'Non-URM']
BGLTQ_CATEGORIES = ['BGLTQ+', 'Non-BGLTQ+']
FGLI_CATEGORIES = ['FGLI', 'Non-FGLI']
CLASS_YEAR_CATEGORIES = ['First-year', 'Sophomore', 'Junior', 'Senior']
#SCHOOL_CATEGORIES = ['Arts and Humanities', 'Social Sciences', 'Pure Sciences', 'Engineering and Applied Sciences']
SCHOOL_CATEGORIES = ['SEAS', 'Non-SEAS']
DISABILITY_CATEGORIES = ['Disability', 'Non-Disability']

# Filter options
GENDER_FILTER_OPTIONS = GENDER_CATEGORIES.copy()
GENDER_FILTER_OPTIONS.insert(0, 'All')
RACE_ETHNICITY_FILTER_OPTIONS = RACE_ETHNICITY_CATEGORIES.copy()
RACE_ETHNICITY_FILTER_OPTIONS.insert(0, 'All')
BGLTQ_FILTER_OPTIONS = BGLTQ_CATEGORIES.copy()
BGLTQ_FILTER_OPTIONS.insert(0, 'All')
FGLI_FILTER_OPTIONS = FGLI_CATEGORIES.copy()
FGLI_FILTER_OPTIONS.insert(0, 'All')
CLASS_YEAR_FILTER_OPTIONS = CLASS_YEAR_CATEGORIES.copy()
CLASS_YEAR_FILTER_OPTIONS.insert(0, 'All')
SCHOOL_FILTER_OPTIONS = SCHOOL_CATEGORIES.copy()
SCHOOL_FILTER_OPTIONS.insert(0, 'All')
CONCENTRATION_FILTER_OPTIONS = ['All', 'Computer Science']

DISABILITY_FILTER_OPTIONS = DISABILITY_CATEGORIES.copy()
DISABILITY_FILTER_OPTIONS.insert(0, 'All')

# Empty figure
EMPTY_FIGURE = {
    "layout": {
        "xaxis": {
            "visible": False
        },
        "yaxis": {
            "visible": False
        },
        "annotations": [
            {
                "text": "Not enough data",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                 "font": {
                    "size": 28
                }
            }
        ]
    }
}