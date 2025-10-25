from plotly.data import gapminder
from dash import dcc, html, Dash, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go

css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css"]
app = Dash(name="Gapminder Dashboard", external_stylesheets=css)

################### DATASET ####################################
gapminder_df = gapminder(datetimes=True, centroids=True, pretty_names=True)
gapminder_df["Year"] = gapminder_df.Year.dt.year

#################### CHARTS #####################################
def create_table():
    fig = go.Figure(data=[go.Table(
        header=dict(values=gapminder_df.columns, align='left'),
        cells=dict(values=gapminder_df.values.T, align='left'))
    ])
    fig.update_layout(paper_bgcolor="#e5ecf6", margin={"t":0, "l":0, "r":0, "b":0}, height=700)
    return fig

def create_population_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df.Continent==continent) & (gapminder_df.Year==year)]
    filtered_df = filtered_df.sort_values(by="Population", ascending=False).head(15)
    fig = px.bar(filtered_df, x="Country", y="Population", color="Country",
                 title=f"Country Population for {continent} Continent in {year}", text_auto=True)
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
    return fig

def create_gdp_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df.Continent==continent) & (gapminder_df.Year==year)]
    filtered_df = filtered_df.sort_values(by="GDP per Capita", ascending=False).head(15)
    fig = px.bar(filtered_df, x="Country", y="GDP per Capita", color="Country",
                 title=f"Country GDP per Capita for {continent} Continent in {year}", text_auto=True)
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
    return fig

def create_life_exp_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[(gapminder_df.Continent==continent) & (gapminder_df.Year==year)]
    filtered_df = filtered_df.sort_values(by="Life Expectancy", ascending=False).head(15)
    fig = px.bar(filtered_df, x="Country", y="Life Expectancy", color="Country",
                 title=f"Country Life Expectancy for {continent} Continent in {year}", text_auto=True)
    fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
    return fig

def create_choropleth_map(variable, year):
    filtered_df = gapminder_df[gapminder_df.Year==year]
    fig = px.choropleth(
        filtered_df, color=variable,
        locations="ISO Alpha Country Code", locationmode="ISO-3",
        color_continuous_scale="RdYlBu", hover_data=["Country", variable],
        title=f"{variable} Choropleth Map [{year}]"
    )
    fig.update_layout(dragmode=False, paper_bgcolor="#e5ecf6", height=600, margin={"l":0, "r":0})
    return fig

##################### WIDGETS ####################################
continents = gapminder_df.Continent.unique()
years = gapminder_df.Year.unique()

cont_population = dcc.Dropdown(id="cont_pop", options=continents, value="Asia", clearable=False)
year_population = dcc.Dropdown(id="year_pop", options=years, value=1952, clearable=False)

cont_gdp = dcc.Dropdown(id="cont_gdp", options=continents, value="Asia", clearable=False)
year_gdp = dcc.Dropdown(id="year_gdp", options=years, value=1952, clearable=False)

cont_life_exp = dcc.Dropdown(id="cont_life_exp", options=continents, value="Asia", clearable=False)
year_life_exp = dcc.Dropdown(id="year_life_exp", options=years, value=1952, clearable=False)

year_map = dcc.Dropdown(id="year_map", options=years, value=1952, clearable=False)
var_map = dcc.Dropdown(
    id="var_map",
    options=["Population", "GDP per Capita", "Life Expectancy"],
    value="Life Expectancy",
    clearable=False
)

##################### APP LAYOUT（左侧竖排 Tabs） ####################################
app.layout = html.Div([
    html.Div([
        html.H1("Gapminder Dataset Analysis", className="text-center fw-bold my-3"),
        html.Div([
            # 左侧：竖排 Tabs
            html.Div([
                dcc.Tabs(
                    id='tabs-left',
                    value='tab1',
                    children=[
                        dcc.Tab(label='Dataset', value='tab1'),
                        dcc.Tab(label='Population', value='tab2'),
                        dcc.Tab(label='GDP Per Capita', value='tab3'),
                        dcc.Tab(label='Life Expectancy', value='tab4'),
                        dcc.Tab(label='Choropleth Map', value='tab5'),
                    ],
                    vertical=True,  # 竖排
                    style={
                        "height": "100%",
                        "width": "220px",
                        "borderRight": "2px solid #cfd8dc",
                        "fontWeight": "600"
                    }
                )
            ], className="col-2 pe-0"),

            # 右侧：内容区
            html.Div(id='tab-content', className="col-10 ps-4"),

        ], className="row", style={"minHeight": "85vh"}),
    ], className="col-10 mx-auto"),
], style={"backgroundColor": "#e5ecf6", "minHeight": "100vh"})

##################### CALLBACKS（原有图表更新） ####################################
@callback(Output("population", "figure"), [Input("cont_pop", "value"), Input("year_pop", "value")])
def update_population_chart(continent, year):
    return create_population_chart(continent, year)

@callback(Output("gdp", "figure"), [Input("cont_gdp", "value"), Input("year_gdp", "value")])
def update_gdp_chart(continent, year):
    return create_gdp_chart(continent, year)

@callback(Output("life_expectancy", "figure"), [Input("cont_life_exp", "value"), Input("year_life_exp", "value")])
def update_life_exp_chart(continent, year):
    return create_life_exp_chart(continent, year)

@callback(Output("choropleth_map", "figure"), [Input("var_map", "value"), Input("year_map", "value")])
def update_map(var_map, year):
    return create_choropleth_map(var_map, year)

##################### 新增：根据左侧竖排 Tabs 切换内容 ###############################
@callback(Output('tab-content', 'children'), Input('tabs-left', 'value'))
def render_tab(tab):
    if tab == 'tab1':
        return dcc.Graph(figure=create_table(), style={"height": "700px"})
    elif tab == 'tab2':
        return html.Div([
            html.Label("Continent", className="fw-semibold small mt-2"),
            cont_population,
            html.Br(),
            html.Label("Year", className="fw-semibold small"),
            year_population,
            html.Br(),
            dcc.Graph(id="population")
        ])
    elif tab == 'tab3':
        return html.Div([
            html.Label("Continent", className="fw-semibold small mt-2"),
            cont_gdp,
            html.Br(),
            html.Label("Year", className="fw-semibold small"),
            year_gdp,
            html.Br(),
            dcc.Graph(id="gdp")
        ])
    elif tab == 'tab4':
        return html.Div([
            html.Label("Continent", className="fw-semibold small mt-2"),
            cont_life_exp,
            html.Br(),
            html.Label("Year", className="fw-semibold small"),
            year_life_exp,
            html.Br(),
            dcc.Graph(id="life_expectancy")
        ])
    elif tab == 'tab5':
        return html.Div([
            html.Label("Variable", className="fw-semibold small mt-2"),
            var_map,
            html.Br(),
            html.Label("Year", className="fw-semibold small"),
            year_map,
            html.Br(),
            dcc.Graph(id="choropleth_map")
        ])

if __name__ == "__main__":
    app.run(debug=True, port=8060)
