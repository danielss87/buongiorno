# Buongiorno - Setup Windows Task Scheduler
# This script creates a scheduled task to run the pipeline daily at 8:00 AM

$taskName = "Buongiorno_Daily_Update"
$taskDescription = "Runs the Buongiorno gold price prediction pipeline daily to generate fresh predictions"
$scriptPath = "C:\Users\danie\Desktop\Python\buon_giorno\run_update.bat"
$workingDirectory = "C:\Users\danie\Desktop\Python\buon_giorno"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Buongiorno - Task Scheduler Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "Task already exists. Removing it..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create the action (what to run)
$action = New-ScheduledTaskAction -Execute $scriptPath -WorkingDirectory $workingDirectory

# Create the trigger (when to run - daily at 8:00 AM)
$trigger = New-ScheduledTaskTrigger -Daily -At 8:00AM

# Create the settings
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 30)

# Create the principal (run as current user)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest

# Register the task
try {
    Register-ScheduledTask -TaskName $taskName -Description $taskDescription -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force | Out-Null

    Write-Host "Task created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Task Details:" -ForegroundColor White
    Write-Host "  Name: $taskName" -ForegroundColor Gray
    Write-Host "  Schedule: Daily at 8:00 AM" -ForegroundColor Gray
    Write-Host "  Script: $scriptPath" -ForegroundColor Gray
    Write-Host ""
    Write-Host "The pipeline will run automatically every day at 8:00 AM" -ForegroundColor Green
    Write-Host ""

    # Show the created task
    Get-ScheduledTask -TaskName $taskName | Format-List TaskName, State, Description

} catch {
    Write-Host "Error creating task: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "You can manage this task in Task Scheduler (taskschd.msc)" -ForegroundColor Cyan
Write-Host ""
