from plotly.data import gapminder
from dash import dcc, html, Dash, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go

# ---- 外观：引入 Bootstrap ----
css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css"]
app = Dash(name="Gapminder Dashboard", external_stylesheets=css)

# =================== 数据 ===================
gapminder_df = gapminder(datetimes=True, centroids=True, pretty_names=True)
gapminder_df["Year"] = gapminder_df.Year.dt.year

# 可选：统一字体与背景（可注释）
BASE_BG = "#f4f6fa"
FONT = dict(size=14, color="#1a1a1a")

# =================== 图表函数 ===================
def create_table():
    fig = go.Figure(
        data=[go.Table(
            header=dict(values=gapminder_df.columns, align='left'),
            cells=dict(values=gapminder_df.values.T, align='left')
        )]
    )
    fig.update_layout(
        paper_bgcolor=BASE_BG,
        margin={"t": 0, "l": 0, "r": 0, "b": 0},
        height=700,
        font=FONT
    )
    return fig


def create_population_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[
        (gapminder_df.Continent == continent) & (gapminder_df.Year == year)
    ].sort_values(by="Population", ascending=False).head(15)

    fig = px.pie(
        filtered_df,
        names="Country",
        values="Population",
        title=f"Population Share — {continent} in {year}",
        color_discrete_sequence=px.colors.qualitative.Bold  # 鲜艳配色
    )
    fig.update_layout(paper_bgcolor=BASE_BG, plot_bgcolor=BASE_BG, font=FONT, height=600)
    return fig


def create_gdp_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[
        (gapminder_df.Continent == continent) & (gapminder_df.Year == year)
    ].sort_values(by="GDP per Capita", ascending=False).head(15)

    fig = px.pie(
        filtered_df,
        names="Country",
        values="GDP per Capita",
        title=f"GDP per Capita Share — {continent} in {year}",
        color_discrete_sequence=px.colors.qualitative.Vivid  # 更亮丽
    )
    fig.update_layout(paper_bgcolor=BASE_BG, plot_bgcolor=BASE_BG, font=FONT, height=600)
    return fig


def create_life_exp_chart(continent="Asia", year=1952):
    filtered_df = gapminder_df[
        (gapminder_df.Continent == continent) & (gapminder_df.Year == year)
    ].sort_values(by="Life Expectancy", ascending=False).head(15)

    fig = px.pie(
        filtered_df,
        names="Country",
        values="Life Expectancy",
        title=f"Life Expectancy Share — {continent} in {year}",
        color_discrete_sequence=px.colors.qualitative.Pastel1  # 柔和多彩
    )
    fig.update_layout(paper_bgcolor=BASE_BG, plot_bgcolor=BASE_BG, font=FONT, height=600)
    return fig


def create_choropleth_map(variable, year):
    filtered_df = gapminder_df[gapminder_df.Year == year]

    fig = px.choropleth(
        filtered_df,
        color=variable,
        locations="ISO Alpha Country Code",
        locationmode="ISO-3",
        color_continuous_scale="Turbo",  # 炫彩渐变
        hover_data=["Country", variable],
        title=f"{variable} Choropleth Map [{year}]"
    )
    fig.update_layout(
        dragmode=False,
        paper_bgcolor=BASE_BG,
        font=FONT,
        height=600,
        margin={"l": 0, "r": 0}
    )
    return fig

# =================== 组件（下拉） ===================
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

# =================== 布局：左侧竖向 Tabs + 右侧内容 ===================
app.layout = html.Div([
    html.Div([
        html.H1("Gapminder Dataset Analysis", className="text-center fw-bold m-2"),
        html.Br(),
        dcc.Tabs(
            children=[
                dcc.Tab(
                    label="Dataset",
                    children=[html.Br(), dcc.Graph(id="dataset", figure=create_table())]
                ),
                dcc.Tab(
                    label="Population",
                    children=[
                        html.Br(), html.Div("Continent"), cont_population,
                        html.Div("Year", className="mt-2"), year_population, html.Br(),
                        dcc.Graph(id="population")
                    ]
                ),
                dcc.Tab(
                    label="GDP Per Capita",
                    children=[
                        html.Br(), html.Div("Continent"), cont_gdp,
                        html.Div("Year", className="mt-2"), year_gdp, html.Br(),
                        dcc.Graph(id="gdp")
                    ]
                ),
                dcc.Tab(
                    label="Life Expectancy",
                    children=[
                        html.Br(), html.Div("Continent"), cont_life_exp,
                        html.Div("Year", className="mt-2"), year_life_exp, html.Br(),
                        dcc.Graph(id="life_expectancy")
                    ]
                ),
                dcc.Tab(
                    label="Choropleth Map",
                    children=[
                        html.Br(), html.Div("Variable"), var_map,
                        html.Div("Year", className="mt-2"), year_map, html.Br(),
                        dcc.Graph(id="choropleth_map")
                    ]
                ),
            ],
            vertical=True,                     # 竖向分布
            style={"width": "260px"},         # 左侧栏宽度
            parent_style={"display": "flex"}, # Tabs整体为左右分布
            content_style={"padding": "0 0 0 16px", "flex": 1, "backgroundColor": BASE_BG}
        )
    ], className="col-10 mx-auto"),
], style={"background-color": BASE_BG, "minHeight": "100vh"})

# =================== 交互回调 ===================
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

# =================== 启动 ===================
if __name__ == "__main__":
    app.run(debug=True, port=8060)
