import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Read the CSV file
print("Loading movie database...")
df = pd.read_csv('mymoviedb.csv', sep=';', encoding='utf-8')

# Clean column names (remove extra semicolons)
df.columns = df.columns.str.strip()

# Display basic info
print(f"\nTotal movies in database: {len(df)}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nFirst few rows:")
print(df.head())

# Convert Release_Date to datetime
df['Release_Date'] = pd.to_datetime(df['Release_Date'], format='%d/%m/%Y', errors='coerce')

# Calculate the date 5 years ago from now
five_years_ago = datetime.now() - timedelta(days=5*365)
print(f"\nAnalyzing movies from {five_years_ago.date()} onwards...")

# Filter movies from last 5 years
df_recent = df[df['Release_Date'] >= five_years_ago].copy()
print(f"Movies in last 5 years: {len(df_recent)}")

# Convert numeric columns
df_recent['Popularity'] = pd.to_numeric(df_recent['Popularity'].astype(str).str.replace('.', '').str.replace(',', '.'), errors='coerce')
df_recent['Vote_Count'] = pd.to_numeric(df_recent['Vote_Count'], errors='coerce')
df_recent['Vote_Average'] = pd.to_numeric(df_recent['Vote_Average'], errors='coerce')

# ============================================
# ANALYSIS 1: MOST VIEWED MOVIES (Last 5 years)
# ============================================
print("\n" + "="*80)
print("ANALYSIS 1: TOP 20 MOST VIEWED MOVIES IN THE LAST 5 YEARS")
print("="*80)

# Sort by Vote_Count (number of votes = views/engagement)
top_movies_by_votes = df_recent.nlargest(20, 'Vote_Count')[['Title', 'Release_Date', 'Vote_Count', 'Vote_Average', 'Popularity', 'Genre', 'Original_Language']]
print("\nTop 20 by Vote Count (Most Viewed):")
print(top_movies_by_votes.to_string(index=False))

# Also show top by popularity
print("\n" + "-"*80)
top_movies_by_popularity = df_recent.nlargest(20, 'Popularity')[['Title', 'Release_Date', 'Popularity', 'Vote_Count', 'Vote_Average', 'Genre', 'Original_Language']]
print("\nTop 20 by Popularity Score:")
print(top_movies_by_popularity.to_string(index=False))

# ============================================
# ANALYSIS 2: ACTORS ANALYSIS
# ============================================
print("\n" + "="*80)
print("ANALYSIS 2: ACTOR ANALYSIS")
print("="*80)
print("\nNOTE: The current dataset does not contain actor information.")
print("The available columns are:", df.columns.tolist())
print("\nTo perform actor analysis, we would need additional data with cast information.")
print("Recommendation: Enhance the dataset with actor/cast columns for comprehensive analysis.")

# ============================================
# ANALYSIS 3: FAVORITE CATEGORIES BY COUNTRY
# ============================================
print("\n" + "="*80)
print("ANALYSIS 3: FAVORITE GENRES BY COUNTRY (Based on Original Language)")
print("="*80)

# Map language codes to countries
language_to_country = {
    'en': 'USA/UK (English)',
    'es': 'Spain/Latin America (Spanish)',
    'fr': 'France (French)',
    'ja': 'Japan (Japanese)',
    'ko': 'South Korea (Korean)',
    'hi': 'India (Hindi)',
    'ru': 'Russia (Russian)',
    'de': 'Germany (German)',
    'th': 'Thailand (Thai)',
    'tr': 'Turkey (Turkish)',
    'it': 'Italy (Italian)',
    'zh': 'China (Chinese)',
    'pt': 'Portugal/Brazil (Portuguese)'
}

df_recent['Country'] = df_recent['Original_Language'].map(language_to_country).fillna('Other')

# Split genres and analyze
genre_by_country = {}
for country in df_recent['Country'].unique():
    country_df = df_recent[df_recent['Country'] == country]
    
    # Split genres (they are comma-separated)
    all_genres = []
    for genres_str in country_df['Genre'].dropna():
        genres = [g.strip() for g in str(genres_str).split(',')]
        all_genres.extend(genres)
    
    genre_counts = Counter(all_genres)
    genre_by_country[country] = genre_counts

# Display results
for country, genres in sorted(genre_by_country.items(), key=lambda x: sum(x[1].values()), reverse=True):
    if sum(genres.values()) > 0:  # Only show countries with data
        print(f"\n{country}:")
        print(f"  Total movies: {sum(genres.values())}")
        print(f"  Top 5 genres:")
        for genre, count in genres.most_common(5):
            percentage = (count / sum(genres.values())) * 100
            print(f"    - {genre}: {count} movies ({percentage:.1f}%)")

# ============================================
# STATISTICAL SUMMARY
# ============================================
print("\n" + "="*80)
print("STATISTICAL SUMMARY (Last 5 Years)")
print("="*80)

print(f"\nTotal movies analyzed: {len(df_recent)}")
print(f"Date range: {df_recent['Release_Date'].min().date()} to {df_recent['Release_Date'].max().date()}")
print(f"\nAverage rating: {df_recent['Vote_Average'].mean():.2f}")
print(f"Average vote count: {df_recent['Vote_Count'].mean():.0f}")
print(f"Average popularity: {df_recent['Popularity'].mean():.2f}")

print(f"\nMovies by year:")
df_recent['Year'] = df_recent['Release_Date'].dt.year
year_counts = df_recent['Year'].value_counts().sort_index()
for year, count in year_counts.items():
    print(f"  {int(year)}: {count} movies")

print(f"\nTop 10 most common genres overall:")
all_genres_recent = []
for genres_str in df_recent['Genre'].dropna():
    genres = [g.strip() for g in str(genres_str).split(',')]
    all_genres_recent.extend(genres)
genre_counts_overall = Counter(all_genres_recent)
for genre, count in genre_counts_overall.most_common(10):
    percentage = (count / len(all_genres_recent)) * 100
    print(f"  {genre}: {count} ({percentage:.1f}%)")

print(f"\nLanguage distribution:")
lang_counts = df_recent['Original_Language'].value_counts().head(10)
for lang, count in lang_counts.items():
    country_name = language_to_country.get(lang, f"Unknown ({lang})")
    percentage = (count / len(df_recent)) * 100
    print(f"  {country_name}: {count} movies ({percentage:.1f}%)")

# ============================================
# SAVE RESULTS TO FILE
# ============================================
print("\n" + "="*80)
print("Saving detailed results to 'movie_analysis_report.txt'...")
print("="*80)

with open('movie_analysis_report.txt', 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("MOVIE DATABASE ANALYSIS REPORT\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("="*80 + "\n\n")
    
    f.write("ANALYSIS PERIOD: Last 5 Years\n")
    f.write(f"From: {five_years_ago.date()}\n")
    f.write(f"To: {datetime.now().date()}\n")
    f.write(f"Total movies analyzed: {len(df_recent)}\n\n")
    
    f.write("="*80 + "\n")
    f.write("1. TOP 20 MOST VIEWED MOVIES (by Vote Count)\n")
    f.write("="*80 + "\n\n")
    f.write(top_movies_by_votes.to_string(index=False))
    
    f.write("\n\n" + "="*80 + "\n")
    f.write("2. TOP 20 MOST POPULAR MOVIES (by Popularity Score)\n")
    f.write("="*80 + "\n\n")
    f.write(top_movies_by_popularity.to_string(index=False))
    
    f.write("\n\n" + "="*80 + "\n")
    f.write("3. FAVORITE GENRES BY COUNTRY\n")
    f.write("="*80 + "\n\n")
    
    for country, genres in sorted(genre_by_country.items(), key=lambda x: sum(x[1].values()), reverse=True):
        if sum(genres.values()) > 0:
            f.write(f"\n{country}:\n")
            f.write(f"  Total movies: {sum(genres.values())}\n")
            f.write(f"  Top genres:\n")
            for genre, count in genres.most_common(10):
                percentage = (count / sum(genres.values())) * 100
                f.write(f"    - {genre}: {count} movies ({percentage:.1f}%)\n")
    
    f.write("\n\n" + "="*80 + "\n")
    f.write("4. STATISTICAL SUMMARY\n")
    f.write("="*80 + "\n\n")
    f.write(f"Average rating: {df_recent['Vote_Average'].mean():.2f}\n")
    f.write(f"Average vote count: {df_recent['Vote_Count'].mean():.0f}\n")
    f.write(f"Average popularity: {df_recent['Popularity'].mean():.2f}\n\n")
    
    f.write("Movies by year:\n")
    for year, count in year_counts.items():
        f.write(f"  {int(year)}: {count} movies\n")
    
    f.write("\nTop genres overall:\n")
    for genre, count in genre_counts_overall.most_common(15):
        percentage = (count / len(all_genres_recent)) * 100
        f.write(f"  {genre}: {count} ({percentage:.1f}%)\n")

print("\nAnalysis complete! Report saved to 'movie_analysis_report.txt'")

# Made with Bob
