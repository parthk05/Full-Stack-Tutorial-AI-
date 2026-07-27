# 6.5 / Lesson 02 — Manual smoke test for MySQL + Mongo routes.
# Start server first: uvicorn main:app --reload
# Ensure .env is set and both DBs are running.

$base = "http://127.0.0.1:8000"

Write-Host "`n=== HEALTH ===" -ForegroundColor Cyan
Invoke-RestMethod -Method Get -Uri "$base/health" | ConvertTo-Json

$createBody = @{
    title = "The Hobbit"
    genre = "Fantasy"
    published_year = 1937
    price = 12.99
    in_stock = $true
} | ConvertTo-Json

foreach ($prefix in @("mysql", "mongo")) {
    Write-Host "`n=== $prefix CREATE ===" -ForegroundColor Cyan
    $created = Invoke-RestMethod -Method Post -Uri "$base/$prefix/books/" -ContentType "application/json" -Body $createBody
    $created | ConvertTo-Json
    $bookId = $created.id

    Write-Host "`n=== $prefix LIST ===" -ForegroundColor Cyan
    Invoke-RestMethod -Method Get -Uri "$base/$prefix/books/?skip=0&limit=10" | ConvertTo-Json -Depth 5

    Write-Host "`n=== $prefix GET ===" -ForegroundColor Cyan
    Invoke-RestMethod -Method Get -Uri "$base/$prefix/books/$bookId" | ConvertTo-Json

    Write-Host "`n=== $prefix UPDATE ===" -ForegroundColor Cyan
    $updateBody = @{ price = 9.99; in_stock = $false } | ConvertTo-Json
    Invoke-RestMethod -Method Put -Uri "$base/$prefix/books/$bookId" -ContentType "application/json" -Body $updateBody | ConvertTo-Json

    Write-Host "`n=== $prefix DELETE ===" -ForegroundColor Cyan
    Invoke-WebRequest -Method Delete -Uri "$base/$prefix/books/$bookId" | Select-Object StatusCode
}

Write-Host "`nDone." -ForegroundColor Green
