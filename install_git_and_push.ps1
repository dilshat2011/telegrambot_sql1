# Git o'rnatish va GitHub ga yuklash skripti
# PowerShell da Run as Administrator sifatida ishga tushiring

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   Git yuklab o'rnatish boshlandi..." -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

$gitInstaller = "$env:TEMP\GitInstaller.exe"
$gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-64-bit.exe"

Write-Host "`n[1/4] Git installer yuklab olinmoqda..." -ForegroundColor Yellow
Invoke-WebRequest -Uri $gitUrl -OutFile $gitInstaller -UseBasicParsing
Write-Host "[OK] Yuklab olindi!" -ForegroundColor Green

Write-Host "`n[2/4] Git o'rnatilmoqda (silent)..." -ForegroundColor Yellow
Start-Process -FilePath $gitInstaller -Args "/VERYSILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /COMPONENTS=icons,ext\reg\shellhere,assoc,assoc_sh" -Wait
Write-Host "[OK] Git o'rnatildi!" -ForegroundColor Green

# PATH ni yangilash
$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")

Write-Host "`n[3/4] Git versiyasi tekshirilmoqda..." -ForegroundColor Yellow
& "C:\Program Files\Git\bin\git.exe" --version

Write-Host "`n[4/4] Loyiha papkasiga o'tilmoqda..." -ForegroundColor Yellow
$projectPath = "c:\Users\TexnoPark\Downloads\telegram bot"
Set-Location $projectPath

# Git sozlamalari (o'zingizniki bilan almashtiring)
Write-Host "`n Git foydalanuvchi ma'lumotlarini kiriting:" -ForegroundColor Cyan
$gitName  = Read-Host "Ismingiz (GitHub username)"
$gitEmail = Read-Host "Email (GitHub email)"

& "C:\Program Files\Git\bin\git.exe" config --global user.name  $gitName
& "C:\Program Files\Git\bin\git.exe" config --global user.email $gitEmail

# Git reponi boshlash
& "C:\Program Files\Git\bin\git.exe" init
& "C:\Program Files\Git\bin\git.exe" add .
& "C:\Program Files\Git\bin\git.exe" commit -m "feat: initial commit - telegram bot with PostgreSQL"

Write-Host "`n============================================" -ForegroundColor Green
Write-Host " MUVAFFAQIYATLI! Endi quyidagilarni bajaring:" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host " 1. GitHub.com ga kiring" -ForegroundColor White
Write-Host " 2. 'New Repository' tugmasini bosing" -ForegroundColor White
Write-Host " 3. Repo nomini kiriting (masalan: telegram-bot)" -ForegroundColor White
Write-Host " 4. 'Create repository' tugmasini bosing" -ForegroundColor White
Write-Host " 5. Quyidagi buyruqlarni ishga tushiring:" -ForegroundColor White
Write-Host ""
Write-Host '   $repoUrl = Read-Host "GitHub repo URL ni kiriting (https://github.com/username/repo.git)"' -ForegroundColor Yellow
Write-Host '   & "C:\Program Files\Git\bin\git.exe" remote add origin $repoUrl' -ForegroundColor Yellow
Write-Host '   & "C:\Program Files\Git\bin\git.exe" branch -M main' -ForegroundColor Yellow
Write-Host '   & "C:\Program Files\Git\bin\git.exe" push -u origin main' -ForegroundColor Yellow
Write-Host ""

pause
