# format better, make green, add title, show on same line

# potentially do (at time of write up): see which ones are most interesting/have best results

import constants as C
import dataframe_init as D

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np

from datetime import datetime

import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

QUESTION_OPTIONS = [      
    'I have already taken all of the CS courses I am interested in',
    'I am not required to take any additional CS courses to fulfill my concentration/secondary',
    'I am no longer interested in CS',
    'CS course material is too difficult',
    'CS courses are too time-intensive',
    'CS courses are poorly designed or organized',
    'I do not have any friends or community within the CS department',
    'I do not feel supported by the CS department',
    'I do not have enough space in my schedule']

QUESTION_ID = 'Q15'

app.layout = html.Div([
    html.Div([
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

        html.Div([
            dcc.Dropdown(
                id='question_option',
                options=[{'label': i, 'value': i} for i in QUESTION_OPTIONS],
                value=QUESTION_OPTIONS[0]),
                
        ], style={'width': '50%', 'margin-left': '50px'})
    ],
    style={'width': '100%', 'display': 'inline-table', 'margin-top' : '15'}),

    dcc.Graph(id='visualization')
])

def is_sample_size_insufficient(dff, axis):
    # get number of responses per category
    category_counts = dff[axis].value_counts().reset_index(name='counts')['counts'].tolist()
    # check number of responses per category is greater than minimum sample size
    return any(c < C.MIN_SAMPLE_SIZE for c in category_counts)


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

@app.callback(
    Output('visualization', 'figure'),
    Input('axis', 'value'),
    Input('filter-gender-dropdown', 'value'),
    Input('filter-race-ethnicity-dropdown', 'value'),
    Input('filter-bgltq-dropdown', 'value'),
    Input('filter-fgli-dropdown', 'value'),
    Input('filter-class-year-dropdown', 'value'),
    Input('filter-school-dropdown', 'value'),
    Input('filter-concentration-dropdown', 'value'),
    Input('question_option', 'value'))
def update_graph(axis, gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, 
    class_year_filter, school_filter, concentration_filter, question_option):
    # get relevant dataframe according to axis
    dff = filter_df(D.AXIS_DF[axis], gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter, class_year_filter, school_filter, concentration_filter)
    
    # names is used for labelling
    names = list(dff[axis].unique())
    
    # new_category = []
    
    # for c in names:
    #     category_df = dff[dff[axis] == c]
    #     new_category.append(category_df) #total_cateogires = [Male_df,Non-male_df]

    # print(len(new_category))
 
    # implement figure   
    generateSpecs = [[{"type": "pie"} for _ in names]]
    fig = make_subplots(rows=1, cols=len(names), specs = generateSpecs, subplot_titles = names)
    colNum = 1

    for name in names:
        df = dff[dff[axis] == name]
        yes_num = df[df[QUESTION_ID].str.contains(question_option, na=False)].shape[0] #filters out yes respondents 
        no_num = df[~(df[QUESTION_ID].str.contains(question_option, na=False))].shape[0] #filters our no respondents
        y_n_values = [yes_num,no_num]

        fig.add_trace(go.Pie(labels=['Yes', 'No'], values=y_n_values, textinfo='none',
                                hoverinfo='label+percent', marker={
            'colors': [
            'rgb(71,159,118)', 'rgb(233,236,239)']}), row=1, col=colNum)
    
        colNum +=1
        
    # plot titles
    fig.update_layout(
        title='Question 15',
        font=dict(
            family="Courier New, monospace",
            size=15,
            color="RebeccaPurple"
        )
    )

    # return empty plot if there is not enough data (or if figure is not yet implemented)
    if fig == None or is_sample_size_insufficient(dff, axis):
        return C.EMPTY_FIGURE

    return fig
       
if __name__ == '__main__':
    app.run_server(debug=True)