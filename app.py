import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ----------------------------
# Load dataset with error handling
# ----------------------------
try:
    df = pd.read_csv("youtube.csv", encoding='latin1')
    # Convert dates
    df['trending_date'] = pd.to_datetime(df['trending_date'], format='%y.%d.%m', errors='coerce')
    df['publish_date'] = pd.to_datetime(df['publish_date'], errors='coerce')
except Exception as e:
    print(f"Error loading data: {e}")
    df = pd.DataFrame()

# Category Mapping
category_map = {
    1: "Film & Animation", 2: "Autos & Vehicles", 10: "Music",
    15: "Pets & Animals", 17: "Sports", 19: "Travel & Events",
    20: "Gaming", 22: "People & Blogs", 23: "Comedy",
    24: "Entertainment", 25: "News & Politics", 26: "Howto & Style",
    27: "Education", 28: "Science & Technology", 29: "Nonprofits & Activism"
}
if not df.empty:
    df['category_name'] = df['category_id'].map(category_map)

# ----------------------------
# Initialize app
# ----------------------------
app = Dash(__name__)
app.title = "YouTube Trending Dashboard"

# ----------------------------
# Layout function
# ----------------------------
def create_layout():
    if df.empty:
        return html.Div([html.H1("Error: Unable to load data. Please check youtube.csv")])
    
    return html.Div([
        html.H1("YouTube Trending Dashboard", style={
            'textAlign': 'center', 'marginBottom': '20px', 'color': '#2c3e50',
            'fontFamily': 'Arial Black'
        }),

        # Filters
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='category_filter',
                    options=[{'label': i, 'value': i} for i in sorted(df['category_name'].dropna().unique())],
                    placeholder="Select Categories",
                    multi=True,
                    style={'width': '300px'}
                )
            ]),
            html.Div([
                dcc.DatePickerRange(
                    id='date_range',
                    start_date=df['trending_date'].min() if not df.empty else None,
                    end_date=df['trending_date'].max() if not df.empty else None,
                    display_format='YYYY-MM-DD'
                )
            ])
        ], style={'display': 'flex', 'justifyContent': 'center', 'gap': '20px', 'marginBottom': '30px'}),

        # Metric Cards
        html.Div([
            html.Div(id='total_videos', className='card', style={'flex': 1}),
            html.Div(id='total_views', className='card', style={'flex': 1}),
            html.Div(id='total_likes', className='card', style={'flex': 1}),
            html.Div(id='avg_views', className='card', style={'flex': 1}),
        ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '40px'}),

        # Charts
        html.Div([
            html.Div(dcc.Loading(dcc.Graph(id='bar_chart')), style={'flex': 1}),
            html.Div(dcc.Loading(dcc.Graph(id='scatter_chart')), style={'flex': 1}),
        ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '40px'}),

        html.Div([
            html.Div(dcc.Loading(dcc.Graph(id='channel_chart')), style={'flex': 1}),
            html.Div(dcc.Loading(dcc.Graph(id='trend_chart')), style={'flex': 1}),
        ], style={'display': 'flex', 'gap': '20px', 'marginBottom': '40px'}),

        html.Div([
            dcc.Loading(dcc.Graph(id='pie_chart'))
        ])
    ], style={'padding': '0 40px', 'backgroundColor': '#f8f9fa', 'fontFamily': 'Arial'})

app.layout = create_layout()

# ----------------------------
# Callback
# ----------------------------
@app.callback(
    [Output('total_videos', 'children'),
     Output('total_views', 'children'),
     Output('total_likes', 'children'),
     Output('avg_views', 'children'),
     Output('bar_chart', 'figure'),
     Output('scatter_chart', 'figure'),
     Output('channel_chart', 'figure'),
     Output('trend_chart', 'figure'),
     Output('pie_chart', 'figure')],
    [Input('category_filter', 'value'),
     Input('date_range', 'start_date'),
     Input('date_range', 'end_date')]
)
def update_dashboard(category, start_date, end_date):
    filtered_df = df.copy()
    if category:
        filtered_df = filtered_df[filtered_df['category_name'].isin(category)]
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['trending_date'] >= start_date) & (filtered_df['trending_date'] <= end_date)]

    if filtered_df.empty:
        empty_fig = go.Figure()
        empty_fig.update_layout(title="No data available for selected filters")
        empty_card = html.Div("No data")
        return empty_card, empty_card, empty_card, empty_card, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig

    # Summary Metrics
    total_videos = len(filtered_df)
    total_views = filtered_df['views'].sum()
    total_likes = filtered_df['likes'].sum()
    avg_views = filtered_df['views'].mean()

    def create_card(title, value, color):
        return html.Div([
            html.H4(title, style={'textAlign': 'center', 'marginBottom': '10px'}),
            html.P(f"{value:,.0f}" if isinstance(value, (int, float)) else str(value), style={'fontSize': '24px', 'textAlign': 'center', 'color': color, 'margin': 0})
        ], style={
            'backgroundColor': 'white',
            'padding': '20px',
            'borderRadius': '15px',
            'boxShadow': '0 4px 8px rgba(0,0,0,0.1)',
            'transition': 'transform 0.2s',
            'textAlign': 'center',
            'cursor': 'pointer'
        })

    total_videos_card = create_card("Total Videos", total_videos, "#2980b9")
    total_views_card = create_card("Total Views", total_views, "#27ae60")
    total_likes_card = create_card("Total Likes", total_likes, "#e67e22")
    avg_views_card = create_card("Average Views", avg_views, "#9b59b6")

    # Charts
    # 1️⃣ Most Popular Categories
    cat_data = df['category_name'].value_counts().reset_index()
    cat_data.columns = ['category_name', 'count']
    bar_fig = px.bar(
        cat_data, x='category_name', y='count',
        title="Most Popular Categories (Overall)",
        text='count', template='plotly_white'
    )
    bar_fig.update_traces(marker_color='#3498db', textposition='outside')
    bar_fig.update_layout(xaxis_tickangle=-45)

    # 2️⃣ Views vs Likes Scatter
    scatter_fig = px.scatter(
        filtered_df, x='views', y='likes',
        hover_data=['title', 'channel_title', 'category_name'],
        title="Views vs Likes Correlation",
        template='plotly_white'
    )
    scatter_fig.update_traces(marker=dict(size=12, color='#f39c12', opacity=0.7))

    # 3️⃣ Top Channels
    top_channels = filtered_df['channel_title'].value_counts().head(10).reset_index()
    top_channels.columns = ['channel_title', 'count']
    channel_fig = px.bar(
        top_channels, x='channel_title', y='count',
        text='count', title="Top Channels (Filtered)",
        template='plotly_white'
    )
    channel_fig.update_traces(marker_color='#2ecc71', textposition='outside')
    channel_fig.update_layout(xaxis_tickangle=-45)

    # 4️⃣ Trend over time
    trend_data = filtered_df.groupby(filtered_df['trending_date'].dt.date)['views'].sum().reset_index()
    trend_fig = px.line(
        trend_data, x='trending_date', y='views',
        title="Views Trend Over Time",
        template='plotly_white'
    )

    # 5️⃣ Category Distribution Pie
    pie_data = filtered_df['category_name'].value_counts().reset_index()
    pie_data.columns = ['category_name', 'count']
    pie_fig = px.pie(
        pie_data, values='count', names='category_name',
        title="Category Distribution (Filtered)",
        template='plotly_white'
    )

    return total_videos_card, total_views_card, total_likes_card, avg_views_card, bar_fig, scatter_fig, channel_fig, trend_fig, pie_fig

# ----------------------------
# Run
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)