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

# Initialize Dash app
app = Dash(__name__)
app.title = "YouTube Trending Dashboard"

# ----------------------------
# Function to create layout
# ----------------------------
def create_layout():
    return html.Div([
        html.H1("YouTube Trending Dashboard", style={
            'textAlign': 'center', 'marginBottom': '20px', 'color': '#1a1a1a'
        }),

        html.Div([
            dcc.Dropdown(
                id='category_filter',
                options=[{'label': i, 'value': i} for i in sorted(df['category_name'].dropna().unique())],
                placeholder="Select a Category",
                style={'width': '300px'}
            )
        ], style={'display': 'flex', 'justifyContent': 'center', 'marginBottom': '30px'}),

        html.Div([
            dcc.Graph(id='bar_chart', style={'height': '400px'}),
            dcc.Graph(id='scatter_chart', style={'height': '400px'}),
            dcc.Graph(id='channel_chart', style={'height': '400px'})
        ], style={'display': 'grid', 'gridTemplateColumns': '1fr', 'gap': '40px', 'padding': '0 50px'})
    ])

# Set app layout
app.layout = create_layout

# ----------------------------
# Callback for interactivity
# ----------------------------
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
    bar_fig = px.bar(
        cat_data, x='category_name', y='count',
        title="Most Popular Categories",
        text='count', template='plotly_white'
    )
    bar_fig.update_traces(marker_color='skyblue', textposition='outside')

    # 2️⃣ Views vs Likes Scatter
    scatter_fig = px.scatter(
        filtered_df, x='views', y='likes',
        title="Views vs Likes Correlation",
        hover_data=['title', 'channel_title', 'category_name'],
        template='plotly_white'
    )
    scatter_fig.update_traces(marker=dict(size=10, color='orange', opacity=0.7))

    # 3️⃣ Top Channels
    top_channels = filtered_df['channel_title'].value_counts().head(10).reset_index()
    top_channels.columns = ['channel_title', 'count']
    channel_fig = px.bar(
        top_channels, x='channel_title', y='count',
        title="Top Channels (Filtered)",
        text='count', template='plotly_white'
    )
    channel_fig.update_traces(marker_color='lightgreen', textposition='outside')

    return bar_fig, scatter_fig, channel_fig

# Run app
if __name__ == '__main__':
    app.run(debug=True)