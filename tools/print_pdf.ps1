# Prints HTML pages to PDF with Microsoft Edge (headless) - no extra packages needed.
# Usage:  powershell -ExecutionPolicy Bypass -File tools\print_pdf.ps1            (all brochures + company profiles)
$edge = "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edge)) { $edge = "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe" }
$root = Split-Path -Parent $PSScriptRoot
$jobs = @(
  @('tools\brochures\sello.html', 'downloads\brochures\Anqah-SELLO-Brochure.pdf'),
  @('tools\brochures\sello-lite.html', 'downloads\brochures\Anqah-SELLO-Lite-Brochure.pdf'),
  @('tools\brochures\sello-retail.html', 'downloads\brochures\Anqah-SELLO-Retail-Brochure.pdf'),
  @('tools\brochures\automatic-bell.html', 'downloads\brochures\Anqah-Automatic-Bell-Brochure.pdf'),
  @('tools\brochures\sello-ar.html', 'downloads\brochures\Anqah-SELLO-Brochure-AR.pdf'),
  @('tools\brochures\sello-lite-ar.html', 'downloads\brochures\Anqah-SELLO-Lite-Brochure-AR.pdf'),
  @('tools\brochures\sello-retail-ar.html', 'downloads\brochures\Anqah-SELLO-Retail-Brochure-AR.pdf'),
  @('tools\brochures\automatic-bell-ar.html', 'downloads\brochures\Anqah-Automatic-Bell-Brochure-AR.pdf'),
  @('tools\profile\profile.html', 'downloads\Anqah-Tech-Company-Profile.pdf'),
  @('tools\profile\profile-ar.html', 'downloads\Anqah-Tech-Company-Profile-AR.pdf')
)
foreach ($j in $jobs) {
  $src = Join-Path $root $j[0]; $out = Join-Path $root $j[1]
  if (-not (Test-Path $src)) { continue }
  if ($args.Count -gt 0 -and -not ($args | Where-Object { $j[0] -like "*$_*" })) { continue }
  $url = 'file:///' + ($src -replace '\\', '/')
  & $edge --headless=new --disable-gpu --no-pdf-header-footer --run-all-compositor-stages-before-draw `
    --virtual-time-budget=15000 --print-to-pdf="$out" $url 2>$null | Out-Null
  Write-Output "wrote $($j[1])"
}
