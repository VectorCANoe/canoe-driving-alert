param(
    [Parameter(Mandatory = $true)]
    [string]$ReportPath,

    [Parameter(Mandatory = $true)]
    [string]$OutputJson,

    [Parameter(Mandatory = $true)]
    [string]$AssemblyDir
)

$ErrorActionPreference = "Stop"

function Read-PropValue {
    param(
        [object]$Target,
        [string]$Name
    )
    try {
        return $Target.$Name
    }
    catch {
        return $null
    }
}

function Read-StringValue {
    param(
        [object]$Target,
        [string]$Name
    )
    $value = Read-PropValue -Target $Target -Name $Name
    if ($null -eq $value) {
        return ""
    }
    try {
        return $value.ToString()
    }
    catch {
        return ""
    }
}

function Read-BoolValue {
    param(
        [object]$Target,
        [string]$Name
    )
    $value = Read-PropValue -Target $Target -Name $Name
    if ($null -eq $value) {
        return $false
    }
    return [bool]$value
}

function Read-IntValue {
    param(
        [object]$Target,
        [string]$Name
    )
    $value = Read-PropValue -Target $Target -Name $Name
    if ($null -eq $value) {
        return $null
    }
    try {
        return [int64]$value
    }
    catch {
        return $null
    }
}

function Read-Enumerable {
    param([object]$Value)
    $items = @()
    if ($null -eq $Value) {
        return $items
    }
    foreach ($item in $Value) {
        $items += $item
    }
    return $items
}

if (-not (Test-Path $ReportPath)) {
    throw "Report file not found: $ReportPath"
}

if (-not (Test-Path $AssemblyDir)) {
    throw "Assembly directory not found: $AssemblyDir"
}

$resolveDir = (Resolve-Path $AssemblyDir).Path
[System.AppDomain]::CurrentDomain.add_AssemblyResolve({
    param($sender, $eventArgs)
    $shortName = ($eventArgs.Name -split ",")[0] + ".dll"
    $candidate = Join-Path $resolveDir $shortName
    if (Test-Path $candidate) {
        return [System.Reflection.Assembly]::LoadFrom($candidate)
    }
    return $null
}) | Out-Null

Get-ChildItem $resolveDir -Filter *.dll | ForEach-Object {
    try {
        [void][System.Reflection.Assembly]::LoadFrom($_.FullName)
    }
    catch {
    }
}

$apiDll = Join-Path $resolveDir "Vector.ReportViewer.DataApi.dll"
[void][System.Reflection.Assembly]::LoadFrom($apiDll)
$rvApiType = [System.Type]::GetType("Vector.ReportViewer.DataApi.RvAPI, Vector.ReportViewer.DataApi")
if ($null -eq $rvApiType) {
    throw "Vector.ReportViewer.DataApi.RvAPI type not found."
}

$rvApi = $rvApiType.GetProperty("Instance").GetValue($null)
$report = $rvApiType.GetMethod("OpenTestReport", [type[]]@([string])).Invoke($rvApi, @($ReportPath))

$testcases = @()
foreach ($child in (Read-Enumerable (Read-PropValue -Target $report -Name "Children"))) {
    $testcases += [pscustomobject]@{
        title             = Read-StringValue -Target $child -Name "Title"
        test_case_id      = Read-StringValue -Target $child -Name "TestCaseId"
        ident             = Read-StringValue -Target $child -Name "Ident"
        number            = Read-IntValue -Target $child -Name "Number"
        verdict           = Read-StringValue -Target $child -Name "Verdict"
        resulting_verdict = Read-StringValue -Target $child -Name "ResultingVerdict"
        description       = Read-StringValue -Target $child -Name "Description"
        begin_time        = Read-StringValue -Target $child -Name "BeginTime"
        end_time          = Read-StringValue -Target $child -Name "EndTime"
        is_skipped        = Read-BoolValue -Target $child -Name "IsSkipped"
        child_count       = (Read-Enumerable (Read-PropValue -Target $child -Name "Children")).Count
    }
}

$payload = [ordered]@{
    schema         = "vector.reportviewer.dataapi.snapshot.v1"
    report_path    = (Resolve-Path $ReportPath).Path
    assembly_dir   = $resolveDir
    generated_at   = [DateTime]::Now.ToString("o")
    report         = [ordered]@{
        title              = Read-StringValue -Target $report -Name "Title"
        verdict            = Read-StringValue -Target $report -Name "Verdict"
        resulting_verdict  = Read-StringValue -Target $report -Name "ResultingVerdict"
        report_state       = Read-StringValue -Target $report -Name "ReportState"
        report_type        = Read-StringValue -Target $report -Name "ReportType"
        verdict_concept    = Read-StringValue -Target $report -Name "VerdictConcept"
        measurement_id     = Read-StringValue -Target $report -Name "MeasurementId"
        unique_id          = Read-StringValue -Target $report -Name "UniqueId"
        begin_time         = Read-StringValue -Target $report -Name "BeginTime"
        end_time           = Read-StringValue -Target $report -Name "EndTime"
        child_count        = (Read-Enumerable (Read-PropValue -Target $report -Name "Children")).Count
    }
    testcase_count = $testcases.Count
    testcases      = $testcases
}

$outputPath = [System.IO.Path]::GetFullPath($OutputJson)
$outputDir = [System.IO.Path]::GetDirectoryName($outputPath)
if (-not [string]::IsNullOrWhiteSpace($outputDir)) {
    New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
}

$payload | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 -Path $outputPath
