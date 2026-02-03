"""
PROJECT 3: Treemap - Global Installs by Category
"""
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

DATA_FILE = 'googleplaystore.csv'
TESTING_MODE = True

print("="*80)
print("PROJECT 3: TREEMAP".center(80))
print("="*80)
print()

# Load
df = pd.read_csv(DATA_FILE)
df['Installs'] = pd.to_numeric(df['Installs'].str.replace(',', '').str.replace('+', ''), errors='coerce').fillna(0)

print(f"✅ Loaded {len(df):,} apps")

# Filter
df_filt = df[
    (df['Installs'] > 1000000) &
    (~df['Category'].str[0].isin(['A', 'C', 'G', 'S']))
].copy()

print(f"✅ After filters: {len(df_filt):,} apps")

# Top 5
cat_installs = df_filt.groupby('Category')['Installs'].sum().nlargest(5).reset_index()
cat_installs.columns = ['Category', 'Total_Installs']
cat_installs['Percentage'] = (cat_installs['Total_Installs'] / cat_installs['Total_Installs'].sum() * 100).round(1)

print("Top 5 Categories:")
for _, row in cat_installs.iterrows():
    print(f"  {row['Category']:30s} {row['Total_Installs']:>15,.0f}")
print()

# Treemap
fig = px.treemap(
    cat_installs,
    path=['Category'],
    values='Total_Installs',
    color='Total_Installs',
    color_continuous_scale='Blues',
    title='<b>Global Installs by Category (Top 5)</b>',
    hover_data={'Total_Installs': ':,', 'Percentage': ':.1f'}
)

fig.update_layout(height=700, width=1200)
fig.update_traces(
    textposition='middle center',
    textfont={'size': 16, 'color': 'white'},
    marker={'line': {'width': 3, 'color': 'white'}}
)

# Time check
ist = pytz.timezone('Asia/Kolkata')
hour = datetime.now(ist).hour

if TESTING_MODE or (18 <= hour < 20):
    print("✅ Displaying chart...")
    fig.show()
    fig.write_html('project3_treemap.html')
    print("💾 Saved: project3_treemap.html")
else:
    print("🚫 Outside 6-8 PM IST")

print("\n" + "="*80)
print("PROJECT 3 COMPLETE".center(80))
print("="*80)