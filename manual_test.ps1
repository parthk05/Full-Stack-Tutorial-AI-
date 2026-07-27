# 6.5 -> Manual smoke test (PowerShell). Start server first:
#   uvicorn main:app --reload
#
# Then run these one by one (or: .\manual_test.ps1).

$base = "http://127.0.0.1:8000"

Write-Host "`n=== CREATE ===" -ForegroundColor Cyan
$createBody = @{
    title = "The Hobbit"
    genre = "Fantasy"
    published_year = 1937
    price = 12.99
    in_stock = $true
} | ConvertTo-Json
$created = Invoke-RestMethod -Method Post -Uri "$base/books/" -ContentType "application/json" -Body $createBody
$created | ConvertTo-Json
$bookId = $created.id

Write-Host "`n=== LIST ===" -ForegroundColor Cyan
Invoke-RestMethod -Method Get -Uri "$base/books/" | ConvertTo-Json -Depth 5

Write-Host "`n=== GET ONE ===" -ForegroundColor Cyan
Invoke-RestMethod -Method Get -Uri "$base/books/$bookId" | ConvertTo-Json

Write-Host "`n=== UPDATE ===" -ForegroundColor Cyan
$updateBody = @{ price = 9.99; in_stock = $false } | ConvertTo-Json
Invoke-RestMethod -Method Put -Uri "$base/books/$bookId" -ContentType "application/json" -Body $updateBody | ConvertTo-Json

Write-Host "`n=== GET 404 (expected error) ===" -ForegroundColor Cyan
try {
    Invoke-RestMethod -Method Get -Uri "$base/books/99999"
} catch {
    Write-Host $_.Exception.Message
}

Write-Host "`n=== DELETE (204) ===" -ForegroundColor Cyan
Invoke-WebRequest -Method Delete -Uri "$base/books/$bookId" | Select-Object StatusCode

Write-Host "`n=== GET after delete (expected 404) ===" -ForegroundColor Cyan
try {
    Invoke-RestMethod -Method Get -Uri "$base/books/$bookId"
} catch {
    Write-Host $_.Exception.Message
}

Write-Host "`nDone." -ForegroundColor Green
