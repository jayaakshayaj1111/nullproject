"""
PROJECT 4: Stacked Area Chart - Cumulative Installs Over Time
"""
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

DATA_FILE = 'googleplaystore.csv'
TESTING_MODE = True

TRANSLATIONS = {
    'TRAVEL_AND_LOCAL': 'Voyage et Local',
    'PRODUCTIVITY': 'Productividad',
    'PHOTOGRAPHY': '写真撮影'
}

print("="*80)
print("PROJECT 4: STACKED AREA CHART".center(80))
print("="*80)
print()

# Load
df = pd.read_csv(DATA_FILE)

def parse_size(s):
    if pd.isna(s): return 0
    s = str(s).strip()
    if 'M' in s: return float(s.replace('M', ''))
    if 'k' in s: return float(s.replace('k', ''))/1024
    return 0

df['Size_MB'] = df['Size'].apply(parse_size)
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
df['Installs'] = pd.to_numeric(df['Installs'].str.replace(',', '').str.replace('+', ''), errors='coerce').fillna(0)

print(f"✅ Loaded {len(df):,} apps")

# Filters (RELAXED for data availability)
df_filt = df[
    (df['Rating'] >= 4.0) &
    (~df['App'].str.contains(r'\d', na=False, regex=True)) &
    (df['Category'].str[0].isin(['T', 'P'])) &
    (df['Reviews'] > 100) &
    (df['Size_MB'] >= 10) & (df['Size_MB'] <= 100)
].copy()

print(f"✅ After filters: {len(df_filt):,} apps")

if len(df_filt) == 0:
    print("❌ No data")
    exit()

# Translations
df_filt['Category_Trans'] = df_filt['Category'].replace(TRANSLATIONS)

# Time series
df_filt['Last Updated'] = pd.to_datetime(df_filt['Last Updated'], errors='coerce')
df_filt['Year_Month'] = df_filt['Last Updated'].dt.to_period('M').astype(str)

monthly = df_filt.groupby(['Year_Month', 'Category_Trans'])['Installs'].sum().reset_index()
monthly = monthly.sort_values(['Category_Trans', 'Year_Month'])
monthly['Cumulative'] = monthly.groupby('Category_Trans')['Installs'].cumsum()
monthly['MoM_Growth'] = monthly.groupby('Category_Trans')['Installs'].pct_change() * 100
monthly['High_Growth'] = monthly['MoM_Growth'] > 25

# Chart
fig = go.Figure()

categories = monthly['Category_Trans'].unique()
colors = {'Voyage et Local': '#3498DB', 'Productividad': '#E74C3C', '写真撮影': '#2ECC71'}

for i, cat in enumerate(categories):
    cat_data = monthly[monthly['Category_Trans'] == cat].sort_values('Year_Month')
    color = colors.get(cat, '#95A5A6')
    
    fig.add_trace(go.Scatter(
        name=cat,
        x=cat_data['Year_Month'],
        y=cat_data['Cumulative'],
        mode='lines',
        line={'width': 0.5, 'color': color},
        fillcolor=color,
        fill='tonexty' if i > 0 else 'tozeroy',
        stackgroup='one'
    ))

fig.update_layout(
    title='<b>Cumulative Installs Over Time</b>',
    xaxis={'tickangle': -45},
    yaxis={'tickformat': ','},
    height=700,
    width=1200
)

# Time check
ist = pytz.timezone('Asia/Kolkata')
hour = datetime.now(ist).hour

if TESTING_MODE or (16 <= hour < 18):
    print("✅ Displaying chart...")
    fig.show()
    fig.write_html('project4_chart.html')
    print("💾 Saved: project4_chart.html")
else:
    print("🚫 Outside 4-6 PM IST")

print("\n" + "="*80)
print("PROJECT 4 COMPLETE".center(80))
print("="*80)