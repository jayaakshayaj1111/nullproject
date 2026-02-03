"""
PROJECT 1: Grouped Bar Chart - Average Rating vs Total Reviews
"""
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

DATA_FILE = 'googleplaystore.csv'
TESTING_MODE = True

print("="*80)
print("PROJECT 1: GROUPED BAR CHART".center(80))
print("="*80)
print()

# Load and clean data
df = pd.read_csv(DATA_FILE)
df['Installs'] = df['Installs'].str.replace(',', '').str.replace('+', '').str.replace('Free', '0')
df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce').fillna(0)

def parse_size(s):
    if pd.isna(s): return 0
    s = str(s).strip()
    if 'M' in s: return float(s.replace('M', ''))
    if 'k' in s: return float(s.replace('k', ''))/1024
    return 0

df['Size_MB'] = df['Size'].apply(parse_size)
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')
df['Update_Month'] = df['Last Updated'].dt.month

print(f"✅ Loaded {len(df):,} apps")

# Apply filters
df_filt = df[(df['Rating'] >= 4.0) & (df['Size_MB'] >= 10) & (df['Update_Month'] == 1)].copy()
print(f"✅ After filters: {len(df_filt):,} apps")

# Top 10 categories
cat_totals = df_filt.groupby('Category')['Installs'].sum().sort_values(ascending=False)
top_10 = cat_totals.head(10).index.tolist()
df_top10 = df_filt[df_filt['Category'].isin(top_10)]

# Statistics
stats = df_top10.groupby('Category').agg({'Rating': 'mean', 'Reviews': 'sum'}).reset_index()
stats.columns = ['Category', 'Avg_Rating', 'Total_Reviews']
stats['Avg_Rating'] = stats['Avg_Rating'].round(2)
stats['Category'] = pd.Categorical(stats['Category'], categories=top_10, ordered=True)
stats = stats.sort_values('Category')

print("Top 10 Categories:")
for _, row in stats.iterrows():
    print(f"  {row['Category']:30s} Rating: {row['Avg_Rating']:.2f} Reviews: {row['Total_Reviews']:,.0f}")
print()

# Create chart
fig = go.Figure()

fig.add_trace(go.Bar(
    name='Average Rating',
    x=stats['Category'],
    y=stats['Avg_Rating'],
    marker={'color': '#3498DB', 'line': {'width': 1.5, 'color': '#2C3E50'}},
    text=stats['Avg_Rating'].round(2),
    textposition='outside'
))

max_rev = stats['Total_Reviews'].max()
fig.add_trace(go.Bar(
    name='Total Reviews',
    x=stats['Category'],
    y=stats['Total_Reviews'] * (5/max_rev),
    marker={'color': '#E74C3C', 'line': {'width': 1.5, 'color': '#C0392B'}},
    text=stats['Total_Reviews'].apply(lambda x: f'{x:,.0f}'),
    textposition='outside',
    customdata=stats['Total_Reviews'],
    hovertemplate='Reviews: %{customdata:,}<extra></extra>'
))

fig.update_layout(
    title='<b>Top 10 Categories: Rating vs Reviews</b><br><sub>Rating≥4.0 | Size≥10MB | January Updates</sub>',
    xaxis={'title': '<b>Category</b>', 'tickangle': -45},
    yaxis={'title': '<b>Value (0-5 scale)</b>', 'range': [0, 5.5]},
    barmode='group',
    height=600,
    width=1200,
    template='plotly_white'
)

# Time check
ist = pytz.timezone('Asia/Kolkata')
hour = datetime.now(ist).hour

if TESTING_MODE or (15 <= hour < 17):
    print("✅ Displaying chart...")
    fig.show()
    fig.write_html('project1_chart.html')
    print("💾 Saved: project1_chart.html")
else:
    print("🚫 Outside 3-5 PM IST")

print("\n" + "="*80)
print("PROJECT 1 COMPLETE".center(80))
print("="*80)