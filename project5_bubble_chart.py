"""
PROJECT 5: Bubble Chart - Size vs Rating
"""
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

DATA_FILE = 'googleplaystore.csv'
REVIEWS_FILE = 'googleplaystore_user_reviews.csv'
TESTING_MODE = True

ALLOWED_CATS = ['GAME', 'BEAUTY', 'BUSINESS', 'COMICS', 'COMMUNICATION', 'DATING', 'ENTERTAINMENT', 'SOCIAL', 'EVENTS']
TRANSLATIONS = {'BEAUTY': 'सुंदरता', 'BUSINESS': 'வணிகம்', 'DATING': 'Dating'}

print("="*80)
print("PROJECT 5: BUBBLE CHART".center(80))
print("="*80)
print()

# Load
df = pd.read_csv(DATA_FILE)
reviews_df = pd.read_csv(REVIEWS_FILE)

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

# Merge sentiment
sentiment_avg = reviews_df.groupby('App')['Sentiment_Subjectivity'].mean().reset_index()
df = df.merge(sentiment_avg, on='App', how='left')

print(f"✅ Loaded {len(df):,} apps")

# Filters
df_filt = df[
    (df['Rating'] > 3.5) &
    (df['Category'].isin(ALLOWED_CATS)) &
    (df['Reviews'] > 500) &
    (~df['App'].str.contains('S', case=False, na=False)) &
    (df['Sentiment_Subjectivity'] > 0.5) &
    (df['Installs'] > 50000)
].copy()

print(f"✅ After filters: {len(df_filt):,} apps")

# Translations
df_filt['Category_Display'] = df_filt['Category'].replace(TRANSLATIONS)

# Aggregate
bubble_data = df_filt.groupby('Category_Display').agg({
    'Size_MB': 'mean',
    'Rating': 'mean',
    'Installs': 'sum'
}).reset_index()
bubble_data.columns = ['Category', 'Avg_Size', 'Avg_Rating', 'Total_Installs']

print("Categories in chart:")
for _, row in bubble_data.iterrows():
    print(f"  {row['Category']}")
print()

# Chart
fig = go.Figure()

colors = {'GAME': '#FF69B4', 'सुंदरता': '#E91E63', 'வணிகம்': '#2196F3'}

for _, row in bubble_data.iterrows():
    color = colors.get(row['Category'], '#607D8B')
    is_game = row['Category'] == 'GAME'
    
    fig.add_trace(go.Scatter(
        name=row['Category'],
        x=[row['Avg_Size']],
        y=[row['Avg_Rating']],
        mode='markers',
        marker={
            'size': row['Total_Installs'] / 100000,
            'color': color,
            'line': {'width': 3 if is_game else 2, 'color': 'white'},
            'opacity': 0.9 if is_game else 0.7
        },
        hovertemplate=f"<b>{row['Category']}</b><br>Size: {row['Avg_Size']:.1f}MB<br>Rating: {row['Avg_Rating']:.2f}"
    ))

fig.update_layout(
    title='<b>Size vs Rating (Bubble = Installs)</b><br><sub>🎮 GAME in PINK</sub>',
    xaxis={'title': 'Avg Size (MB)'},
    yaxis={'title': 'Avg Rating', 'range': [3.4, 5.1]},
    height=700,
    width=1200
)

# Time check
ist = pytz.timezone('Asia/Kolkata')
hour = datetime.now(ist).hour

if TESTING_MODE or (17 <= hour < 19):
    print("✅ Displaying chart...")
    fig.show()
    fig.write_html('project5_chart.html')
    print("💾 Saved: project5_chart.html")
else:
    print("🚫 Outside 5-7 PM IST")

print("\n" + "="*80)
print("PROJECT 5 COMPLETE".center(80))
print("="*80)