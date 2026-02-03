"""
PROJECT 6: Time Series Line Chart - Install Trends Over Time
"""
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

DATA_FILE = 'googleplaystore.csv'
TESTING_MODE = True

TRANSLATIONS = {'BEAUTY': 'सुंदरता', 'BUSINESS': 'வணிகம்', 'DATING': 'Dating'}

print("="*80)
print("PROJECT 6: TIME SERIES CHART".center(80))
print("="*80)
print()

# Load
df = pd.read_csv(DATA_FILE)
df['Installs'] = pd.to_numeric(df['Installs'].str.replace(',', '').str.replace('+', ''), errors='coerce').fillna(0)
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')

print(f"✅ Loaded {len(df):,} apps")

# Filters
df_filt = df[
    (~df['App'].str[0].isin(['X', 'Y', 'Z'])) &
    (df['Category'].str[0].isin(['E', 'C', 'B'])) &
    (df['Reviews'] > 500) &
    (~df['App'].str.contains('S', case=False, na=False))
].copy()

print(f"✅ After filters: {len(df_filt):,} apps")

# Translations
df_filt['Category_Display'] = df_filt['Category'].replace(TRANSLATIONS)

# Time series
df_filt['Last Updated'] = pd.to_datetime(df_filt['Last Updated'], errors='coerce')
df_filt['Year_Month'] = df_filt['Last Updated'].dt.to_period('M').astype(str)

time_series = df_filt.groupby(['Year_Month', 'Category_Display'])['Installs'].sum().reset_index()
time_series = time_series.sort_values(['Category_Display', 'Year_Month'])
time_series['MoM_Growth'] = time_series.groupby('Category_Display')['Installs'].pct_change() * 100
time_series['High_Growth'] = time_series['MoM_Growth'] > 20

# Chart
fig = go.Figure()

categories = time_series['Category_Display'].unique()
colors = {'ENTERTAINMENT': '#E74C3C', 'COMMUNICATION': '#3498DB', 'BUSINESS': '#2ECC71', 
          'வணிகம்': '#2ECC71', 'सुंदरता': '#E91E63'}

for cat in categories:
    cat_data = time_series[time_series['Category_Display'] == cat].sort_values('Year_Month')
    color = colors.get(cat, '#95A5A6')
    
    fig.add_trace(go.Scatter(
        name=cat,
        x=cat_data['Year_Month'],
        y=cat_data['Installs'],
        mode='lines+markers',
        line={'width': 3, 'color': color},
        marker={'size': 8}
    ))

# Shaded regions
high_months = time_series[time_series['High_Growth'] == True]['Year_Month'].unique()
all_months = sorted(time_series['Year_Month'].unique())

for month in high_months:
    try:
        idx = all_months.index(month)
        fig.add_shape(
            type="rect",
            xref="x", yref="paper",
            x0=idx-0.4, x1=idx+0.4,
            y0=0, y1=1,
            fillcolor="rgba(255,0,0,0.1)",
            layer="below", line_width=0
        )
    except:
        pass

fig.update_layout(
    title='<b>Install Trends Over Time</b><br><sub>Red shading = >20% MoM Growth</sub>',
    xaxis={'tickangle': -45, 'type': 'category'},
    yaxis={'tickformat': ','},
    height=700,
    width=1200
)

# Time check
ist = pytz.timezone('Asia/Kolkata')
hour = datetime.now(ist).hour

if TESTING_MODE or (18 <= hour < 21):
    print("✅ Displaying chart...")
    fig.show()
    fig.write_html('project6_chart.html')
    print("💾 Saved: project6_chart.html")
else:
    print("🚫 Outside 6-9 PM IST")

print("\n" + "="*80)
print("PROJECT 6 COMPLETE".center(80))
print("="*80)