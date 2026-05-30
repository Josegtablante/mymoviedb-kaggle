import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Read the CSV file
print("Loading movie database...")
df = pd.read_csv('mymoviedb.csv', sep=';', encoding='utf-8')
df.columns = df.columns.str.strip()

# Convert Release_Date to datetime
df['Release_Date'] = pd.to_datetime(df['Release_Date'], format='%d/%m/%Y', errors='coerce')

# Filter last 5 years
five_years_ago = datetime.now() - timedelta(days=5*365)
df_recent = df[df['Release_Date'] >= five_years_ago].copy()

# Convert numeric columns
df_recent['Popularity'] = pd.to_numeric(df_recent['Popularity'].astype(str).str.replace('.', '').str.replace(',', '.'), errors='coerce')
df_recent['Vote_Count'] = pd.to_numeric(df_recent['Vote_Count'], errors='coerce')
df_recent['Vote_Average'] = pd.to_numeric(df_recent['Vote_Average'], errors='coerce')
df_recent['Year'] = df_recent['Release_Date'].dt.year

print(f"Creating visualizations for {len(df_recent)} movies from last 5 years...")

# Language to country mapping
language_to_country = {
    'en': 'USA/UK',
    'es': 'Spain/LatAm',
    'fr': 'France',
    'ja': 'Japan',
    'ko': 'S. Korea',
    'hi': 'India',
    'ru': 'Russia',
    'de': 'Germany',
    'th': 'Thailand',
    'tr': 'Turkey',
    'it': 'Italy',
    'zh': 'China',
    'pt': 'Portugal/Brazil'
}

df_recent['Country'] = df_recent['Original_Language'].map(language_to_country).fillna('Other')

# Create figure with subplots
fig = plt.figure(figsize=(20, 24))

# ============================================
# GRAPH 1: Top 15 Most Viewed Movies
# ============================================
ax1 = plt.subplot(4, 2, 1)
top_movies = df_recent.nlargest(15, 'Vote_Count')[['Title', 'Vote_Count']].sort_values('Vote_Count')
ax1.barh(range(len(top_movies)), top_movies['Vote_Count'].values, color='steelblue')
ax1.set_yticks(range(len(top_movies)))
ax1.set_yticklabels(top_movies['Title'].values, fontsize=9)
ax1.set_xlabel('Number of Votes', fontsize=10, fontweight='bold')
ax1.set_title('Top 15 Most Viewed Movies (Last 5 Years)', fontsize=12, fontweight='bold', pad=10)
ax1.grid(axis='x', alpha=0.3)
for i, v in enumerate(top_movies['Vote_Count'].values):
    ax1.text(v + 100, i, f'{int(v):,}', va='center', fontsize=8)

# ============================================
# GRAPH 2: Top 15 by Popularity
# ============================================
ax2 = plt.subplot(4, 2, 2)
top_popular = df_recent.nlargest(15, 'Popularity')[['Title', 'Popularity']].sort_values('Popularity')
ax2.barh(range(len(top_popular)), top_popular['Popularity'].values, color='coral')
ax2.set_yticks(range(len(top_popular)))
ax2.set_yticklabels(top_popular['Title'].values, fontsize=9)
ax2.set_xlabel('Popularity Score', fontsize=10, fontweight='bold')
ax2.set_title('Top 15 Most Popular Movies (Last 5 Years)', fontsize=12, fontweight='bold', pad=10)
ax2.grid(axis='x', alpha=0.3)
ax2.ticklabel_format(style='plain', axis='x')

# ============================================
# GRAPH 3: Movies by Year
# ============================================
ax3 = plt.subplot(4, 2, 3)
year_counts = df_recent['Year'].value_counts().sort_index()
colors = plt.cm.viridis(range(len(year_counts)))
bars = ax3.bar(year_counts.index.astype(int), year_counts.values, color=colors, edgecolor='black', linewidth=1.5)
ax3.set_xlabel('Year', fontsize=10, fontweight='bold')
ax3.set_ylabel('Number of Movies', fontsize=10, fontweight='bold')
ax3.set_title('Movies Released by Year', fontsize=12, fontweight='bold', pad=10)
ax3.grid(axis='y', alpha=0.3)
for bar in bars:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

# ============================================
# GRAPH 4: Top 10 Genres Overall
# ============================================
ax4 = plt.subplot(4, 2, 4)
all_genres = []
for genres_str in df_recent['Genre'].dropna():
    genres = [g.strip() for g in str(genres_str).split(',')]
    all_genres.extend(genres)
genre_counts = Counter(all_genres)
top_genres = dict(genre_counts.most_common(10))
colors = plt.cm.Set3(range(len(top_genres)))
wedges, texts, autotexts = ax4.pie(top_genres.values(), labels=top_genres.keys(), autopct='%1.1f%%',
                                     colors=colors, startangle=90, textprops={'fontsize': 9})
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
ax4.set_title('Top 10 Genres Distribution', fontsize=12, fontweight='bold', pad=10)

# ============================================
# GRAPH 5: Movies by Country/Language
# ============================================
ax5 = plt.subplot(4, 2, 5)
country_counts = df_recent['Country'].value_counts().head(10).sort_values()
ax5.barh(range(len(country_counts)), country_counts.values, color='mediumseagreen')
ax5.set_yticks(range(len(country_counts)))
ax5.set_yticklabels(country_counts.index, fontsize=9)
ax5.set_xlabel('Number of Movies', fontsize=10, fontweight='bold')
ax5.set_title('Top 10 Countries by Movie Count', fontsize=12, fontweight='bold', pad=10)
ax5.grid(axis='x', alpha=0.3)
for i, v in enumerate(country_counts.values):
    ax5.text(v + 5, i, str(v), va='center', fontsize=9, fontweight='bold')

# ============================================
# GRAPH 6: Average Rating by Year
# ============================================
ax6 = plt.subplot(4, 2, 6)
avg_rating_by_year = df_recent.groupby('Year')['Vote_Average'].mean().sort_index()
ax6.plot(avg_rating_by_year.index.astype(int), avg_rating_by_year.values, 
         marker='o', linewidth=3, markersize=10, color='darkviolet')
ax6.set_xlabel('Year', fontsize=10, fontweight='bold')
ax6.set_ylabel('Average Rating', fontsize=10, fontweight='bold')
ax6.set_title('Average Movie Rating by Year', fontsize=12, fontweight='bold', pad=10)
ax6.grid(True, alpha=0.3)
ax6.set_ylim(0, 10)
for x, y in zip(avg_rating_by_year.index.astype(int), avg_rating_by_year.values):
    ax6.text(x, y + 0.2, f'{y:.2f}', ha='center', fontsize=9, fontweight='bold')

# ============================================
# GRAPH 7: Top Genres by Top 3 Countries
# ============================================
ax7 = plt.subplot(4, 2, 7)
top_countries = df_recent['Country'].value_counts().head(3).index

genre_by_country_data = {}
for country in top_countries:
    country_df = df_recent[df_recent['Country'] == country]
    country_genres = []
    for genres_str in country_df['Genre'].dropna():
        genres = [g.strip() for g in str(genres_str).split(',')]
        country_genres.extend(genres)
    genre_counts = Counter(country_genres)
    genre_by_country_data[country] = dict(genre_counts.most_common(5))

# Prepare data for grouped bar chart
all_genres_top = set()
for genres in genre_by_country_data.values():
    all_genres_top.update(genres.keys())

x = range(len(all_genres_top))
width = 0.25
genres_list = list(all_genres_top)

for i, country in enumerate(top_countries):
    values = [genre_by_country_data[country].get(genre, 0) for genre in genres_list]
    ax7.bar([p + width * i for p in x], values, width, label=country)

ax7.set_xlabel('Genres', fontsize=10, fontweight='bold')
ax7.set_ylabel('Number of Movies', fontsize=10, fontweight='bold')
ax7.set_title('Top Genres by Country (Top 3 Countries)', fontsize=12, fontweight='bold', pad=10)
ax7.set_xticks([p + width for p in x])
ax7.set_xticklabels(genres_list, rotation=45, ha='right', fontsize=8)
ax7.legend(fontsize=9)
ax7.grid(axis='y', alpha=0.3)

# ============================================
# GRAPH 8: Rating vs Popularity Scatter
# ============================================
ax8 = plt.subplot(4, 2, 8)
# Sample data to avoid overcrowding
sample_df = df_recent.sample(min(500, len(df_recent)))
scatter = ax8.scatter(sample_df['Vote_Average'], sample_df['Popularity'], 
                     c=sample_df['Vote_Count'], cmap='YlOrRd', 
                     s=100, alpha=0.6, edgecolors='black', linewidth=0.5)
ax8.set_xlabel('Average Rating', fontsize=10, fontweight='bold')
ax8.set_ylabel('Popularity Score', fontsize=10, fontweight='bold')
ax8.set_title('Rating vs Popularity (colored by Vote Count)', fontsize=12, fontweight='bold', pad=10)
ax8.grid(True, alpha=0.3)
cbar = plt.colorbar(scatter, ax=ax8)
cbar.set_label('Vote Count', fontsize=9, fontweight='bold')

plt.tight_layout(pad=3.0)
plt.savefig('movie_analysis_visualizations.png', dpi=300, bbox_inches='tight')
print("\n[OK] Main visualization saved as 'movie_analysis_visualizations.png'")

# ============================================
# ADDITIONAL GRAPH: Genre Distribution by Country (Separate Figure)
# ============================================
fig2, axes = plt.subplots(2, 3, figsize=(18, 12))
fig2.suptitle('Genre Distribution by Country (Top 6 Countries)', fontsize=16, fontweight='bold', y=0.995)

top_6_countries = df_recent['Country'].value_counts().head(6).index

for idx, country in enumerate(top_6_countries):
    ax = axes[idx // 3, idx % 3]
    country_df = df_recent[df_recent['Country'] == country]
    country_genres = []
    for genres_str in country_df['Genre'].dropna():
        genres = [g.strip() for g in str(genres_str).split(',')]
        country_genres.extend(genres)
    
    genre_counts = Counter(country_genres)
    top_genres_country = dict(genre_counts.most_common(8))
    
    colors = plt.cm.Paired(range(len(top_genres_country)))
    wedges, texts, autotexts = ax.pie(top_genres_country.values(), 
                                        labels=top_genres_country.keys(),
                                        autopct='%1.1f%%',
                                        colors=colors,
                                        startangle=90,
                                        textprops={'fontsize': 8})
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(7)
    
    ax.set_title(f'{country}\n({len(country_df)} movies)', fontsize=11, fontweight='bold', pad=10)

plt.tight_layout()
plt.savefig('genre_distribution_by_country.png', dpi=300, bbox_inches='tight')
print("[OK] Genre distribution by country saved as 'genre_distribution_by_country.png'")

# ============================================
# TIMELINE GRAPH
# ============================================
fig3, ax = plt.subplots(figsize=(16, 8))

# Group by month
df_recent['YearMonth'] = df_recent['Release_Date'].dt.to_period('M')
monthly_counts = df_recent.groupby('YearMonth').size()
monthly_counts.index = monthly_counts.index.to_timestamp()

ax.plot(monthly_counts.index, monthly_counts.values, linewidth=2.5, color='darkblue', marker='o', markersize=4)
ax.fill_between(monthly_counts.index, monthly_counts.values, alpha=0.3, color='lightblue')
ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Movies Released', fontsize=12, fontweight='bold')
ax.set_title('Movie Releases Timeline (Last 5 Years)', fontsize=14, fontweight='bold', pad=15)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.savefig('movie_releases_timeline.png', dpi=300, bbox_inches='tight')
print("[OK] Timeline visualization saved as 'movie_releases_timeline.png'")

print("\n" + "="*60)
print("All visualizations created successfully!")
print("="*60)
print("\nGenerated files:")
print("  1. movie_analysis_visualizations.png - Main dashboard with 8 graphs")
print("  2. genre_distribution_by_country.png - Genre breakdown by country")
print("  3. movie_releases_timeline.png - Release timeline")
print("\nYou can now view these images to visualize the movie data!")

# Made with Bob
