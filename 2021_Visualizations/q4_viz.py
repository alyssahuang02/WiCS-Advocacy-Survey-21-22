import constants as C
import dataframe_init as D

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime
import dash_bootstrap_components as dbc


# constants
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
q_id = 'Q4'

CS = ["Computer Science"]
SEAS = ["Applied Mathematics", "Biomedical Engineering", "Electrical Engineering", "Engineering Sciences", "Environmental Science and Engineering", "Mechanical Engineering"]
Science = ["Astrophysics", "Chemical and Physical Biology", "Chemistry", "Chemistry and Physics", "Earth and Planetary Sciences", "Environmental Science and Public Policy", 
    "Human Developmental and Regenerative Biology", "Human Evolutionary Biology", "Integrative Biology", "Mathematics", "Molecular and Cellular Biology", "Neuroscience",
    "Physics", "Psychology", "Statistics"]
Arts_and_Humanities = ["Art, Film, and Visual Studies", "Classics", "Comparative Literature", "East Asian Studies", "English", "Folklore and Mythology", "Germanic Languages and Literatures",
    "History & Literature", "History of Art and Architecture", "Linguistics", "Music", "Near Eastern Languages and Civilizations", "Philosophy", "Religion, Comparative Study of",
    "Romance Languages and Literatures", "Slavic Languages and Literatures", "South Asian Studies", "Theater, Dance & Media"]
Social_Science = ["African and African American Studies", "Anthropology", "East Asian Studies", "Economics", "Government", "History", "History and Science", "Psychology", "Social Studies",
    "Sociology", "Women, Gender, and Sexuality, Studies of"]

categories = {'CS':CS, 'SEAS':SEAS, 'Science':Science, 'Arts and Humanities':Arts_and_Humanities, 'Social Science':Social_Science}

app.layout = html.Div([

    html.Div([
        html.H1('Explore'),
        html.P('Explore the experiences of Harvard undergraduate students with computer science, as they relate to gender and other aspects of identity.')
    ], style={'width': '30%', 'display': 'inline-table', 'margin-top': 60, 'margin-left': 50}),
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
    ], style={'width': '20%', 'display': 'inline-table', 'margin-top': 20, 'margin-left': 50}),
    html.Div([
        html.H4('Filter'),
        dbc.Button("Select Filters", color="info",
                   id="open-filter", className="mr-1"),
        dbc.Modal(
            [
                dbc.ModalHeader("Filter Options"),
                dbc.ModalBody(
                    "You may only select up to two filters at a time, and you may not filter on the basis of your selected split."),
                html.Div([
                    html.Div([
                        html.P('Gender'),
                        dcc.Dropdown(
                            id='filter-gender-dropdown',
                            options=[{'label': i, 'value': i}
                                     for i in C.GENDER_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                        style={'width': '40%', 'display': 'inline-block', 'margin': 15}),
                    html.Div([
                        html.P('Race/Ethnicity'),
                        dcc.Dropdown(
                            id='filter-race-ethnicity-dropdown',
                            options=[{'label': i, 'value': i}
                                     for i in C.RACE_ETHNICITY_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                        style={'width': '40%', 'display': 'inline-block', 'margin': 15})
                ]),
                html.Div([
                    html.Div([
                        html.P('BGLTQ+'),
                        dcc.Dropdown(
                            id='filter-bgltq-dropdown',
                            options=[{'label': i, 'value': i}
                                     for i in C.BGLTQ_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                        style={'width': '40%', 'display': 'inline-block', 'margin': 15}),
                    html.Div([
                        html.P('First Generation, Low Income (FGLI)'),
                        dcc.Dropdown(
                            id='filter-fgli-dropdown',
                            options=[{'label': i, 'value': i}
                                     for i in C.FGLI_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                        style={'width': '40%', 'display': 'inline-block', 'margin': 15}),
                ]),
                html.Div([
                    html.Div([
                        html.P('Class Year'),
                        dcc.Dropdown(
                            id='filter-class-year-dropdown',
                            options=[{'label': i, 'value': i}
                                     for i in C.CLASS_YEAR_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                        style={'width': '40%', 'display': 'inline-block', 'margin': 15}),
                    html.Div([
                        html.P('School of Primary Concentration'),
                        dcc.Dropdown(
                            id='filter-school-dropdown',
                            options=[{'label': i, 'value': i}
                                     for i in C.SCHOOL_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                        style={'width': '40%', 'display': 'inline-block', 'margin': 15})
                ]),
                html.Div([
                    html.Div([
                        html.P('Primary Concentration'),
                        dcc.Dropdown(
                            id='filter-concentration-dropdown',
                            options=[{'label': i, 'value': i}
                                     for i in C.CONCENTRATION_FILTER_OPTIONS],
                            value='All',
                            clearable=False
                        )
                    ],
                        style={'width': '40%', 'display': 'inline-block', 'margin': 15})
                ]),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-filter", className="ml-auto")
                ),
            ],
            id="filter-modal",
            size="lg",
        ),
        html.P('Filters: None', id='filters-label',
               style={'font-style': 'italic'})
    ], style={'width': '30%', 'display': 'inline-table', 'margin-top': 20, 'margin-left': 50}),



    html.Div(
        children=[
            dcc.Graph(id='visualization')
        ],
        style={'margin-top': 40, 'margin-right': 90,
               'justify-content': 'center'}
    ),

])


def is_sample_size_insufficient(dff, axis):
    # get number of responses per category
    category_counts = dff[axis].value_counts().reset_index(name='counts')[
        'counts'].tolist()
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

    filter_selections = [gender_filter, race_ethnicity_filter, bgltq_filter,
                         fgli_filter, class_year_filter, school_filter, concentration_filter]
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
    filter_selections = [gender_filter, race_ethnicity_filter, bgltq_filter,
                         fgli_filter, class_year_filter, school_filter, concentration_filter]
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
    Input('filter-concentration-dropdown', 'value'))
def update_graph(axis, gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter,
                 class_year_filter, school_filter, concentration_filter):
    # get relevant dataframe according to axis
    dff = filter_df(D.AXIS_DF[axis], gender_filter, race_ethnicity_filter, bgltq_filter, fgli_filter,
        class_year_filter, school_filter, concentration_filter)

    unique_categories = dff[axis].unique()
    category_names = list(dff[axis].unique())
    
    new_category = []
    
    for c in unique_categories:
        category_df = dff[dff[axis] == c]
        new_category.append(category_df)
 
    generateSpecs = [[{"type": "pie"} for _ in new_category]]
    fig = make_subplots(rows=1, cols=len(new_category),specs = generateSpecs, subplot_titles = category_names)
    colNum = 1
   
    text_annotations=[]
    text_annotations.append(dict(font=dict(size=14)))

    cs_num = 0
    seas_num = 0
    science_num = 0
    aah_num = 0
    ss_num = 0
    values_list = [cs_num, seas_num, science_num, aah_num, ss_num]

    for df in new_category: #new category = inc. in colnum
        for el in df[q_id]:
            index = 0
            for key in categories:
                if el in categories[key]:
                    values_list[index] += 1
                index += 1

        fig.add_trace(go.Pie(
            labels = ['CS', 'SEAS', 'Science', 'Arts and Humanities', 'Social Science'],
            values = values_list,
            textinfo='none',
            hoverinfo='label+percent',
            direction = 'clockwise',
            sort = False,
            marker={'colors': ['rgba(102, 0, 0, 0.8)', 'rgba(204, 0, 0, 0.8)', 'rgba(217, 217, 217, 0.8)', 'rgba(60, 120, 216, 0.8)', 'rgba(28, 69, 135, 0.8)']}
        ), row=1, col=colNum)
        colNum +=1
    fig.update_layout(
        title='Before attending Harvard, which of the following concentrations did you consider pursuing (grouped by schools)?',
        annotations=text_annotations,
        height=300,
        margin=dict(l=0, r=0, t=70, b=30),
        legend=dict(
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=1.02,
            itemclick=False,
            itemdoubleclick=False
        )
    )

    # check for errors
    if fig == None or is_sample_size_insufficient(dff, axis):
        print("ERROR")
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)