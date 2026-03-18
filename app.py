import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load dataset
df = pd.read_csv("youtube.csv", encoding='latin1')

# Category Mapping
category_map = {
    1: "Film & Animation", 2: "Autos & Vehicles", 10: "Music",
    15: "Pets & Animals", 17: "Sports", 19: "Travel & Events",
    20: "Gaming", 22: "People & Blogs", 23: "Comedy",
    24: "Entertainment", 25: "News & Politics", 26: "Howto & Style",
    27: "Education", 28: "Science & Technology", 29: "Nonprofits & Activism"
}

# Convert category_id → category_name
df['category_name'] = df['category_id'].map(category_map)

# Create app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("YouTube Trending Video Dashboard", style={'textAlign': 'center'}),

    dcc.Dropdown(
        id='category_filter',
        options=[{'label': i, 'value': i} for i in sorted(df['category_name'].dropna().unique())],
        placeholder="Select Category"
    ),

    dcc.Graph(id='bar_chart'),
    dcc.Graph(id='scatter_chart'),
    dcc.Graph(id='channel_chart')
])

# Callback
@app.callback(
    [Output('bar_chart', 'figure'),
     Output('scatter_chart', 'figure'),
     Output('channel_chart', 'figure')],
    [Input('category_filter', 'value')]
)
def update_graph(category):

    # Filter data
    filtered_df = df if not category else df[df['category_name'] == category]

    # 1️⃣ Most Popular Categories (always full dataset)
    cat_data = df['category_name'].value_counts().reset_index()
    cat_data.columns = ['category_name', 'count']
    bar_fig = px.bar(cat_data, x='category_name', y='count',
                     title="Most Popular Categories")

    # 2️⃣ Views vs Likes
    scatter_fig = px.scatter(filtered_df, x='views', y='likes',
                             title="Views vs Likes Correlation")

    # 3️⃣ Top Channels
    top_channels = filtered_df['channel_title'].value_counts().head(10).reset_index()
    top_channels.columns = ['channel_title', 'count']
    channel_fig = px.bar(top_channels, x='channel_title', y='count',
                         title="Top Channels")

    return bar_fig, scatter_fig, channel_fig


# Run app
if __name__ == '__main__':
    app.run(debug=True)