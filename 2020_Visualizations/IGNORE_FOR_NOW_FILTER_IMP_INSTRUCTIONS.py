# INSTRUCTIONS FOR IMPLEMENTING FILTER

'''
STEP 1: Add the following code to constants.py, around line 60
        (after "Axes categories" are defined).
'''

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


'''
STEP 2: On the command line, install Dash Bootstrap Components.
'''

pip install dash-bootstrap-components


'''
STEP 3: Import dash_bootstrap_components in your main code file.
'''

import dash_bootstrap_components as dbc


'''
STEP 4: Set the external stylesheets to dbc.themes.BOOTSTRAP.
'''

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


'''
STEP 5: Add the following HTML Dash elements within app.layout
        (replacing the current HTML Dash element for Axis).
        Be mindful not to delete any additional HTML elements you
        may have implemented.
'''

html.Div([
    html.H1('Explore'),
    html.P('Explore the experiences of Harvard undergraduate students with computer science, as they relate to gender and other aspects of identity.')
], style={'width': '30%', 'display': 'inline-table', 'margin-top' : 60, 'margin-left' : 50}),
html.Div([
    html.H4('Split by'),
    html.Div([
        dcc.Dropdown(
            id='axis',
            options=[{'label': i, 'value': i} for i in C.VIZ_AXES],
            value='Gender',
            clearable=False
        )
    ])
], style={'width': '20%', 'display': 'inline-table', 'margin-top' : 20, 'margin-left' : 50}),
html.Div([
    html.H4('Filter'),
    dbc.Button("Select Filters", color="info", id="open-filter", className="mr-1"),
    dbc.Modal(
        [
            dbc.ModalHeader("Filter Options"),
            dbc.ModalBody("You may only select up to two filters at a time, and you may not filter on the basis of your selected split."),
            html.Div([
                html.Div([
                    html.P('Gender'),
                    dcc.Dropdown(
                        id='filter-gender-dropdown',
                        options=[{'label': i, 'value': i} for i in C.GENDER_FILTER_OPTIONS],
                        value='All',
                        clearable=False
                    )
                ],
                style={'width': '40%', 'display': 'inline-block', 'margin' : 15}),
                html.Div([
                    html.P('Race/Ethnicity'),
                    dcc.Dropdown(
                        id='filter-race-ethnicity-dropdown',
                        options=[{'label': i, 'value': i} for i in C.RACE_ETHNICITY_FILTER_OPTIONS],
                        value='All',
                        clearable=False
                    )
                ],
                style={'width': '40%', 'display': 'inline-block', 'margin' : 15})
            ]),
            html.Div([
                html.Div([
                    html.P('BGLTQ+'),
                    dcc.Dropdown(
                        id='filter-bgltq-dropdown',
                        options=[{'label': i, 'value': i} for i in C.BGLTQ_FILTER_OPTIONS],
                        value='All',
                        clearable=False
                    )
                ],
                style={'width': '40%', 'display': 'inline-block', 'margin' : 15}),
                html.Div([
                    html.P('First Generation, Low Income (FGLI)'),
                    dcc.Dropdown(
                        id='filter-fgli-dropdown',
                        options=[{'label': i, 'value': i} for i in C.FGLI_FILTER_OPTIONS],
                        value='All',
                        clearable=False
                    )
                ],
                style={'width': '40%', 'display': 'inline-block', 'margin' : 15}),
            ]),
            html.Div([
                html.Div([
                    html.P('Class Year'),
                    dcc.Dropdown(
                        id='filter-class-year-dropdown',
                        options=[{'label': i, 'value': i} for i in C.CLASS_YEAR_FILTER_OPTIONS],
                        value='All',
                        clearable=False
                    )
                ],
                style={'width': '40%', 'display': 'inline-block', 'margin' : 15}),
                html.Div([
                    html.P('School of Primary Concentration'),
                    dcc.Dropdown(
                        id='filter-school-dropdown',
                        options=[{'label': i, 'value': i} for i in C.SCHOOL_FILTER_OPTIONS],
                        value='All',
                        clearable=False
                    )
                ],
                style={'width': '40%', 'display': 'inline-block', 'margin' : 15})
            ]),
            html.Div([
                html.Div([
                    html.P('Primary Concentration'),
                    dcc.Dropdown(
                        id='filter-concentration-dropdown',
                        options=[{'label': i, 'value': i} for i in C.CONCENTRATION_FILTER_OPTIONS],
                        value='All',
                        clearable=False
                    )
                ],
                style={'width': '40%', 'display': 'inline-block', 'margin' : 15})
            ]),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-filter", className="ml-auto")
            ),
        ],
        id="filter-modal",
        size="lg",
    ),
    html.P('Filters: None', id='filters-label', style={'font-style' : 'italic'})
], style={'width': '30%', 'display': 'inline-table', 'margin-top' : 20, 'margin-left' : 50}),


'''
STEP 6: Add the following functions to your file, above update_graph().
'''

@app.callback(
    Output('filter-modal', 'is_open'),
    Input('open-filter', 'n_clicks'),
    Input('close-filter', 'n_clicks'),
    State('filter-modal', 'is_open'))
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output('filter-gender-dropdown', 'disabled'),
    Output('filter-race-ethnicity-dropdown', 'disabled'),
    Output('filter-bgltq-dropdown', 'disabled'),
    Output('filter-fgli-dropdown', 'disabled'),
    Output('filter-class-year-dropdown', 'disabled'),
    Output('filter-school-dropdown', 'disabled'),
    Output('filter-concentration-dropdown', 'disabled'),
    Input('axis', 'value'),
    Input('filter-gender-dropdown', 'value'),
    Input('filter-race-ethnicity-dropdown', 'value'),
    Input('filter-bgltq-dropdown', 'value'),
    Input('filter-fgli-dropdown', 'value'),
    Input('filter-class-year-dropdown', 'value'),
    Input('filter-school-dropdown', 'value'),
    Input('filter-concentration-dropdown', 'value'))
def toggle_filters(axis, gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, 
    class_year_filter, school_filter, concentration_filter):
    filter_count = 0
    filter_enable_list = [False, False, False, False, False, False, False]
    filter_enable_list[C.VIZ_AXES.index(axis)] = True
    filter_disable_list = filter_enable_list.copy()

    filter_selections = [gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, class_year_filter, school_filter, concentration_filter]
    for i in range(len(filter_selections)):
        if filter_selections[i] == 'All':
            filter_disable_list[i] = (True)
        else:
            filter_count += 1

    if filter_count >= 2:
        return filter_disable_list
    return filter_enable_list

@app.callback(
    Output('filter-gender-dropdown', 'value'),
    Output('filter-race-ethnicity-dropdown', 'value'),
    Output('filter-bgltq-dropdown', 'value'),
    Output('filter-fgli-dropdown', 'value'),
    Output('filter-class-year-dropdown', 'value'),
    Output('filter-school-dropdown', 'value'),
    Output('filter-concentration-dropdown', 'value'),
    Input('axis', 'value'))
def reset_filters(axis):
    return ['All', 'All', 'All', 'All', 'All', 'All', 'All']

@app.callback(
    Output('filters-label', 'children'),
    Input('filter-gender-dropdown', 'value'),
    Input('filter-race-ethnicity-dropdown', 'value'),
    Input('filter-bgltq-dropdown', 'value'),
    Input('filter-fgli-dropdown', 'value'),
    Input('filter-class-year-dropdown', 'value'),
    Input('filter-school-dropdown', 'value'),
    Input('filter-concentration-dropdown', 'value'))
def set_filters_label(gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, 
    class_year_filter, school_filter, concentration_filter):
    filter_str_list = []
    filter_selections = [gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, class_year_filter, school_filter, concentration_filter]
    for sel in filter_selections:
        if sel != 'All':
            filter_str_list.append(sel)
    
    if len(filter_str_list) == 0:
        return 'Filters: None'
    return 'Filters: ' + ', '.join(filter_str_list)


'''
STEP 7: Update the signature for update_graph() to include the following
        new inputs. Be mindful not to delete any additional input arguments
        you may have implemented.
'''

@app.callback(
    Output('visualization', 'figure'),
    Input('axis', 'value'),
    Input('filter-gender-dropdown', 'value'),
    Input('filter-race-ethnicity-dropdown', 'value'),
    Input('filter-bgltq-dropdown', 'value'),
    Input('filter-fgli-dropdown', 'value'),
    Input('filter-class-year-dropdown', 'value'),
    Input('filter-school-dropdown', 'value'),
    Input('filter-concentration-dropdown', 'value'))
def update_graph(axis, gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, 
    class_year_filter, school_filter, concentration_filter):


'''
At this point, you should have a redesigned header with a Select Filters button.
A modal with the filter options should appear when the button is pressed, and
the filter restrictions should work as expected. Next, we implement the actual
filtering.
'''

'''
STEP 8: In dataframe_init.py, replace the "Class year filter (non-constant)" section
        and the "Create dataframe per axis" section with the following code:
'''

# Filter methods

def filter_gender(df, c):
    if c == 'Male':
        return filter_male(df)
    if c == 'Non-male':
        return filter_non_male(df)
    return df

def filter_male(df):
    return df[df['Q37'].isin(C.MALE)]

def filter_non_male(df):
    return df[df['Q37'].isin(C.NONMALE)]

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
    return df[df['Q40'].str.contains('Asian', na=False)]

def filter_black(df):
    return df[df['Q40'].str.contains('Black or African American', na=False)]

def filter_hispanic(df):
    return df[df['Q41'] == 'Yes, of Hispanic or Latinx origin']

def filter_white(df):
    return df[df['Q40'].str.contains('White', na=False)]

def filter_bgltq(df, c):
    if c == 'BGLTQ+':
        return filter_is_bgltq(df)
    if c == 'Non-BGLTQ+':
        return filter_is_non_bgltq(df)
    return df

def filter_is_bgltq(df):
    return df[(df['Q38'] == 'Yes') | df['Q39'].isin(C.NONSTRAIGHT)]

def filter_is_non_bgltq(df):
    return df[(df['Q38'] == 'No') & df['Q39'].isin(C.STRAIGHT)]

def filter_fgli(df, c):
    if c == 'FGLI':
        return filter_is_fgli(df)
    if c == 'Non-FGLI':
        return filter_is_non_fgli(df)
    return df

def filter_is_fgli(df):
    return df[(df['Q42'] == 'Yes') | (df['Q43'] == 'Yes')]

def filter_is_non_fgli(df):
    return df[(df['Q42'] == 'No') & (df['Q43'] == 'No')]

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
    return df[(datetime(2023, 9, 1) <= df['Q4_DT']) & (df['Q4_DT'] <= datetime(2024, 8, 31))]

def filter_sophomore(df):
    return df[(datetime(2022, 9, 1) <= df['Q4_DT']) & (df['Q4_DT'] <= datetime(2023, 8, 31))]

def filter_junior(df):
    return df[(datetime(2021, 9, 1) <= df['Q4_DT']) & (df['Q4_DT'] <= datetime(2022, 8, 31))]

def filter_senior(df):
    return df[(datetime(2020, 9, 1) <= df['Q4_DT']) & (df['Q4_DT'] <= datetime(2021, 8, 31))]

def filter_school(df, c):
    if c == 'Arts and Humanities':
        return filter_arts_humanitites(df)
    if c == 'Social Sciences':
        return filter_social_sciences(df)
    if c == 'Pure Sciences':
        return filter_pure_sciences(df)
    if c == 'Engineering and Applied Sciences':
        return filter_seas(df)
    return df

def filter_arts_humanitites(df):
    return df[df['Q1'].isin(C.ARTS_HUMANITIES)]

def filter_social_sciences(df):
    return df[df['Q1'].isin(C.SOCIAL_SCIENCES)]

def filter_pure_sciences(df):
    return df[df['Q1'].isin(C.PURE_SCIENCES)]

def filter_seas(df):
    return df[df['Q1'].isin(C.SEAS)]

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
ASIAN_DF = filter_asian(CLEAN_DF)
ASIAN_DF['Race/Ethnicity'] = 'Asian'
BLACK_DF = filter_black(CLEAN_DF)
BLACK_DF['Race/Ethnicity'] = 'Black or African American'
HISPANIC_DF = filter_hispanic(CLEAN_DF)
HISPANIC_DF['Race/Ethnicity'] = 'Hispanic or Latinx'
WHITE_DF = filter_white(CLEAN_DF)
WHITE_DF['Race/Ethnicity'] = 'White'
RACE_ETHNICITY_DF = pd.concat([ASIAN_DF, BLACK_DF, HISPANIC_DF, WHITE_DF], ignore_index=True, sort=False)
RACE_ETHNICITY_DF = RACE_ETHNICITY_DF[RACE_ETHNICITY_DF['Race/Ethnicity'].isin(C.RACE_ETHNICITY_CATEGORIES)]

# BGLTQ+
IS_BGLTQ_DF = filter_bgltq(CLEAN_DF)
IS_BGLTQ_DF['BGLTQ+'] = 'BGLTQ+'
IS_NOT_BGLTQ_DF = filter_non_bgltq(CLEAN_DF)
IS_NOT_BGLTQ_DF['BGLTQ+'] = 'Non-BGLTQ+'
BGLTQ_DF = pd.concat([IS_BGLTQ_DF, IS_NOT_BGLTQ_DF], ignore_index=True, sort=False)
BGLTQ_DF = BGLTQ_DF[BGLTQ_DF['BGLTQ+'].isin(C.BGLTQ_CATEGORIES)]

# FGLI
IS_FGLI_DF = filter_fgli(CLEAN_DF)
IS_FGLI_DF['FGLI'] = 'FGLI'
IS_NOT_FGLI_DF = filter_non_fgli(CLEAN_DF)
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
ARTS_HUMANITIES_DF = filter_arts_humanitites(CLEAN_DF)
ARTS_HUMANITIES_DF['School'] = 'Arts and Humanities'
SOCIAL_SCIENCES_DF = filter_social_sciences(CLEAN_DF)
SOCIAL_SCIENCES_DF['School'] = 'Social Sciences'
PURE_SCIENCES_DF = filter_pure_sciences(CLEAN_DF)
PURE_SCIENCES_DF['School'] = 'Pure Sciences'
SEAS_DF = filter_seas(CLEAN_DF)
SEAS_DF['School'] = 'Engineering and Applied Sciences'
SCHOOL_DF = pd.concat([ARTS_HUMANITIES_DF, SOCIAL_SCIENCES_DF, PURE_SCIENCES_DF, SEAS_DF], ignore_index=True, sort=False)
SCHOOL_DF = SCHOOL_DF[SCHOOL_DF['School'].isin(C.SCHOOL_CATEGORIES)]

'''
Make sure your visualization is still working as expected.
'''


'''
STEP 9: Add the following function to your file, above update_graph().
'''

def filter_df(df, gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, 
    class_year_filter, school_filter, concentration_filter):
    df = D.filter_gender(df, gender_filter)
    df = D.filter_race_ethnicity(df, race_ethnicity_filter)
    df = D.filter_bgltq(df, bgltq_filter)
    df = D.filter_fgli(df, fgli_filter)
    df = D.filter_class_year(df, class_year_filter)
    df = D.filter_school(df, school_filter)
    df = D.filter_conc(df, concentration_filter)
    return df


'''
STEP 10: In update_graph(), replace dff = D.AXIS_DF[axis] with the following.
'''

dff = filter_df(D.AXIS_DF[axis], gender_filter, race_ethnicity_filter, bgltq_filter,
        fgli_filter, class_year_filter, school_filter, concentration_filter)

'''
Filtering should now work as expected.
'''


'''
STEP 11: [Bug Fix] In is_sample_size_insufficient(...), replace 'all' with 'any' as
         shown below
'''

def is_sample_size_insufficient(dff, axis):
    # get number of responses per category
    category_counts = dff[axis].value_counts().reset_index(name='counts')['counts'].tolist()
    # check number of responses per category is greater than minimum sample size
    return any(c < C.MIN_SAMPLE_SIZE for c in category_counts)