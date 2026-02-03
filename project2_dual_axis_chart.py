"""
PROJECT 2: Dual-Axis Chart - Free vs Paid Apps
"""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import pytz

DATA_FILE = 'googleplaystore.csv'
TESTING_MODE = True

print("="*80)
print("PROJECT 2: DUAL-AXIS CHART".center(80))
print("="*80)
print()

# Load and clean
df = pd.read_csv(DATA_FILE)
df['Installs'] = pd.to_numeric(df['Installs'].str.replace(',', '').str.replace('+', ''), errors='coerce').fillna(0)
df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace('$', ''), errors='coerce').fillna(0)
df['Revenue'] = df['Installs'] * df['Price']

def parse_size(s):
    if pd.isna(s): return 0
    s = str(s).strip()
    if 'M' in s: return float(s.replace('M', ''))
    if 'k' in s: return float(s.replace('k', ''))/1024
    return 0

df['Size_MB'] = df['Size'].apply(parse_size)

def parse_android(v):
    if pd.isna(v): return 0
    v = str(v)
    try: return float(v.split()[0])
    except: return 0

df['Android_Ver'] = df['Android Ver'].apply(parse_android)
df['App_Name_Len'] = df['App'].str.len()

print(f"✅ Loaded {len(df):,} apps")

# Filters
df_filt = df[
    (df['Installs'] >= 10000) &
    (df['Revenue'] >= 10000) &
    (df['Android_Ver'] > 4.0) &
    (df['Size_MB'] > 15) &
    (df['Content Rating'] == 'Everyone') &
    (df['App_Name_Len'] <= 30)
].copy()

print(f"✅ After filters: {len(df_filt):,} apps")

# Top 3 categories
top_3 = df_filt.groupby('Category')['Installs'].sum().nlargest(3).index.tolist()
df_top3 = df_filt[df_filt['Category'].isin(top_3)]

print("Top 3 Categories:")
for cat in top_3:
    print(f"  {cat}")
print()

# Stats
comp = df_top3.groupby(['Category', 'Type']).agg({
    'Installs': 'mean',
    'Revenue': 'mean'
}).reset_index()
comp.columns = ['Category', 'Type', 'Avg_Installs', 'Avg_Revenue']

free = comp[comp['Type'] == 'Free']
paid = comp[comp['Type'] == 'Paid']

# Chart
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Bar(name='Free-Installs', x=free['Category'], y=free['Avg_Installs'],
    marker={'color': '#3498DB'}), secondary_y=False)
fig.add_trace(go.Bar(name='Paid-Installs', x=paid['Category'], y=paid['Avg_Installs'],
    marker={'color': '#E74C3C'}), secondary_y=False)

fig.add_trace(go.Scatter(name='Free-Revenue', x=free['Category'], y=free['Avg_Revenue'],
    mode='lines+markers', marker={'color': '#1ABC9C', 'size': 12}), secondary_y=True)
fig.add_trace(go.Scatter(name='Paid-Revenue', x=paid['Category'], y=paid['Avg_Revenue'],
    mode='lines+markers', marker={'color': '#F39C12', 'size': 12}), secondary_y=True)

fig.update_layout(
    title='<b>Free vs Paid: Installs & Revenue</b>',
    barmode='group',
    height=700,
    width=1200
)
fig.update_yaxes(title_text="Avg Installs", secondary_y=False)
fig.update_yaxes(title_text="Avg Revenue ($)", secondary_y=True)

# Time check
ist = pytz.timezone('Asia/Kolkata')
hour = datetime.now(ist).hour

if TESTING_MODE or (13 <= hour < 14):
    print("✅ Displaying chart...")
    fig.show()
    fig.write_html('project2_chart.html')
    print("💾 Saved: project2_chart.html")
else:
    print("🚫 Outside 1-2 PM IST")

print("\n" + "="*80)
print("PROJECT 2 COMPLETE".center(80))
print("="*80)