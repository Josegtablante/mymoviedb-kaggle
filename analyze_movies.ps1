# Movie Database Analysis Script
# Analyzes movies from the last 5 years

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "MOVIE DATABASE ANALYSIS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Import CSV
Write-Host "Loading movie database..." -ForegroundColor Yellow
$movies = Import-Csv 'mymoviedb.csv' -Delimiter ';'
Write-Host "Total movies in database: $($movies.Count)" -ForegroundColor Green
Write-Host ""

# Convert dates and filter last 5 years
$fiveYearsAgo = (Get-Date).AddYears(-5)
Write-Host "Analyzing movies from $($fiveYearsAgo.ToString('yyyy-MM-dd')) onwards..." -ForegroundColor Yellow

$recentMovies = $movies | Where-Object {
    try {
        $date = [DateTime]::ParseExact($_.Release_Date, 'd/M/yyyy', $null)
        $date -ge $fiveYearsAgo
    } catch {
        $false
    }
}

Write-Host "Movies in last 5 years: $($recentMovies.Count)" -ForegroundColor Green
Write-Host ""

# Convert numeric fields
$recentMovies | ForEach-Object {
    try {
        $_.Vote_Count = [int]$_.Vote_Count
    } catch {
        $_.Vote_Count = 0
    }
    try {
        # Handle popularity with dots and commas
        $popStr = $_.Popularity -replace '\.', '' -replace ',', '.'
        $_.Popularity = [double]$popStr
    } catch {
        $_.Popularity = 0
    }
    try {
        $_.Vote_Average = [double]$_.Vote_Average
    } catch {
        $_.Vote_Average = 0
    }
}

# ============================================
# ANALYSIS 1: MOST VIEWED MOVIES
# ============================================
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TOP 20 MOST VIEWED MOVIES (Last 5 Years)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$topByVotes = $recentMovies | Sort-Object Vote_Count -Descending | Select-Object -First 20
Write-Host "Ranked by Vote Count (Number of Ratings):" -ForegroundColor Yellow
Write-Host ""

$rank = 1
foreach ($movie in $topByVotes) {
    Write-Host "$rank. $($movie.Title)" -ForegroundColor White
    Write-Host "   Release: $($movie.Release_Date) | Votes: $($movie.Vote_Count) | Rating: $($movie.Vote_Average) | Language: $($movie.Original_Language)" -ForegroundColor Gray
    Write-Host "   Genres: $($movie.Genre)" -ForegroundColor DarkGray
    Write-Host ""
    $rank++
}

Write-Host "----------------------------------------" -ForegroundColor Cyan
Write-Host "TOP 20 BY POPULARITY SCORE" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Cyan
Write-Host ""

$topByPopularity = $recentMovies | Sort-Object Popularity -Descending | Select-Object -First 20
$rank = 1
foreach ($movie in $topByPopularity) {
    Write-Host "$rank. $($movie.Title)" -ForegroundColor White
    Write-Host "   Popularity: $($movie.Popularity) | Votes: $($movie.Vote_Count) | Rating: $($movie.Vote_Average)" -ForegroundColor Gray
    Write-Host ""
    $rank++
}

# ============================================
# ANALYSIS 2: ACTORS
# ============================================
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ACTOR ANALYSIS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "NOTE: The current dataset does not contain actor/cast information." -ForegroundColor Red
Write-Host "Available columns: $($movies[0].PSObject.Properties.Name -join ', ')" -ForegroundColor Gray
Write-Host ""
Write-Host "To perform actor analysis, the dataset would need to include:" -ForegroundColor Yellow
Write-Host "  - Cast/Actor names" -ForegroundColor Gray
Write-Host "  - Director information" -ForegroundColor Gray
Write-Host "  - Production company details" -ForegroundColor Gray
Write-Host ""

# ============================================
# ANALYSIS 3: GENRES BY COUNTRY
# ============================================
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "FAVORITE GENRES BY COUNTRY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Language to country mapping
$languageMap = @{
    'en' = 'USA/UK (English)'
    'es' = 'Spain/Latin America (Spanish)'
    'fr' = 'France (French)'
    'ja' = 'Japan (Japanese)'
    'ko' = 'South Korea (Korean)'
    'hi' = 'India (Hindi)'
    'ru' = 'Russia (Russian)'
    'de' = 'Germany (German)'
    'th' = 'Thailand (Thai)'
    'tr' = 'Turkey (Turkish)'
    'it' = 'Italy (Italian)'
    'zh' = 'China (Chinese)'
    'pt' = 'Portugal/Brazil (Portuguese)'
}

# Group by language
$byLanguage = $recentMovies | Group-Object Original_Language | Sort-Object Count -Descending

foreach ($langGroup in $byLanguage) {
    $country = if ($languageMap.ContainsKey($langGroup.Name)) { $languageMap[$langGroup.Name] } else { "Other ($($langGroup.Name))" }
    
    Write-Host "$country" -ForegroundColor Yellow
    Write-Host "  Total movies: $($langGroup.Count)" -ForegroundColor Gray
    
    # Count genres
    $genreCounts = @{}
    foreach ($movie in $langGroup.Group) {
        if ($movie.Genre) {
            $genres = $movie.Genre -split ',' | ForEach-Object { $_.Trim() }
            foreach ($genre in $genres) {
                if ($genre) {
                    if ($genreCounts.ContainsKey($genre)) {
                        $genreCounts[$genre]++
                    } else {
                        $genreCounts[$genre] = 1
                    }
                }
            }
        }
    }
    
    # Show top 5 genres
    Write-Host "  Top 5 genres:" -ForegroundColor Gray
    $topGenres = $genreCounts.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 5
    foreach ($genre in $topGenres) {
        $percentage = ($genre.Value / $langGroup.Count) * 100
        Write-Host "    - $($genre.Key): $($genre.Value) movies ($($percentage.ToString('F1'))%)" -ForegroundColor DarkGray
    }
    Write-Host ""
}

# ============================================
# STATISTICAL SUMMARY
# ============================================
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "STATISTICAL SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$avgRating = ($recentMovies | Measure-Object Vote_Average -Average).Average
$avgVotes = ($recentMovies | Measure-Object Vote_Count -Average).Average
$avgPopularity = ($recentMovies | Measure-Object Popularity -Average).Average

Write-Host "Average Rating: $($avgRating.ToString('F2'))" -ForegroundColor Green
Write-Host "Average Vote Count: $($avgVotes.ToString('F0'))" -ForegroundColor Green
Write-Host "Average Popularity: $($avgPopularity.ToString('F2'))" -ForegroundColor Green
Write-Host ""

# Movies by year
Write-Host "Movies by Year:" -ForegroundColor Yellow
$byYear = $recentMovies | ForEach-Object {
    try {
        $date = [DateTime]::ParseExact($_.Release_Date, 'd/M/yyyy', $null)
        [PSCustomObject]@{ Year = $date.Year }
    } catch {}
} | Group-Object Year | Sort-Object Name

foreach ($yearGroup in $byYear) {
    Write-Host "  $($yearGroup.Name): $($yearGroup.Count) movies" -ForegroundColor Gray
}
Write-Host ""

# Overall genre distribution
Write-Host "Top 10 Most Common Genres Overall:" -ForegroundColor Yellow
$allGenres = @{}
foreach ($movie in $recentMovies) {
    if ($movie.Genre) {
        $genres = $movie.Genre -split ',' | ForEach-Object { $_.Trim() }
        foreach ($genre in $genres) {
            if ($genre) {
                if ($allGenres.ContainsKey($genre)) {
                    $allGenres[$genre]++
                } else {
                    $allGenres[$genre] = 1
                }
            }
        }
    }
}

$topGenresOverall = $allGenres.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 10
$totalGenreCount = ($allGenres.Values | Measure-Object -Sum).Sum
foreach ($genre in $topGenresOverall) {
    $percentage = ($genre.Value / $totalGenreCount) * 100
    Write-Host "  $($genre.Key): $($genre.Value) ($($percentage.ToString('F1'))%)" -ForegroundColor Gray
}
Write-Host ""

# ============================================
# SAVE TO FILE
# ============================================
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Saving detailed report..." -ForegroundColor Yellow

$reportPath = "movie_analysis_report.txt"
$report = @"
================================================================================
MOVIE DATABASE ANALYSIS REPORT
Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
================================================================================

ANALYSIS PERIOD: Last 5 Years
From: $($fiveYearsAgo.ToString('yyyy-MM-dd'))
To: $(Get-Date -Format 'yyyy-MM-dd')
Total movies analyzed: $($recentMovies.Count)

================================================================================
1. TOP 20 MOST VIEWED MOVIES (by Vote Count)
================================================================================

"@

$rank = 1
foreach ($movie in $topByVotes) {
    $report += "$rank. $($movie.Title)`n"
    $report += "   Release: $($movie.Release_Date) | Votes: $($movie.Vote_Count) | Rating: $($movie.Vote_Average)`n"
    $report += "   Language: $($movie.Original_Language) | Genres: $($movie.Genre)`n`n"
    $rank++
}

$report += @"

================================================================================
2. TOP 20 MOST POPULAR MOVIES (by Popularity Score)
================================================================================

"@

$rank = 1
foreach ($movie in $topByPopularity) {
    $report += "$rank. $($movie.Title)`n"
    $report += "   Popularity: $($movie.Popularity) | Votes: $($movie.Vote_Count) | Rating: $($movie.Vote_Average)`n`n"
    $rank++
}

$report += @"

================================================================================
3. FAVORITE GENRES BY COUNTRY (Based on Original Language)
================================================================================

"@

foreach ($langGroup in $byLanguage) {
    $country = if ($languageMap.ContainsKey($langGroup.Name)) { $languageMap[$langGroup.Name] } else { "Other ($($langGroup.Name))" }
    $report += "`n$country`n"
    $report += "  Total movies: $($langGroup.Count)`n"
    
    $genreCounts = @{}
    foreach ($movie in $langGroup.Group) {
        if ($movie.Genre) {
            $genres = $movie.Genre -split ',' | ForEach-Object { $_.Trim() }
            foreach ($genre in $genres) {
                if ($genre) {
                    if ($genreCounts.ContainsKey($genre)) {
                        $genreCounts[$genre]++
                    } else {
                        $genreCounts[$genre] = 1
                    }
                }
            }
        }
    }
    
    $report += "  Top genres:`n"
    $topGenres = $genreCounts.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 10
    foreach ($genre in $topGenres) {
        $percentage = ($genre.Value / $langGroup.Count) * 100
        $report += "    - $($genre.Key): $($genre.Value) movies ($($percentage.ToString('F1'))%)`n"
    }
}

$report += @"

================================================================================
4. STATISTICAL SUMMARY
================================================================================

Average Rating: $($avgRating.ToString('F2'))
Average Vote Count: $($avgVotes.ToString('F0'))
Average Popularity: $($avgPopularity.ToString('F2'))

Movies by Year:
"@

foreach ($yearGroup in $byYear) {
    $report += "  $($yearGroup.Name): $($yearGroup.Count) movies`n"
}

$report += "`nTop Genres Overall:`n"
foreach ($genre in $topGenresOverall) {
    $percentage = ($genre.Value / $totalGenreCount) * 100
    $report += "  $($genre.Key): $($genre.Value) ($($percentage.ToString('F1'))%)`n"
}

$report | Out-File -FilePath $reportPath -Encoding UTF8

Write-Host "Report saved to: $reportPath" -ForegroundColor Green
Write-Host ""
Write-Host "Analysis complete!" -ForegroundColor Cyan

# Made with Bob
