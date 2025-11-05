# 📅 Setting Up the Daily Scheduler for Buongiorno

The scheduled task will run automatically every day at **8:00 AM** to generate fresh gold price predictions.

## ⚡ Quick Setup (Requires Administrator)

### Option 1: PowerShell Script (Recommended)

1. **Right-click** on **PowerShell** and select **"Run as Administrator"**
2. Navigate to the project folder:
   ```powershell
   cd C:\Users\danie\Desktop\Python\buon_giorno
   ```
3. Run the setup script:
   ```powershell
   .\setup_scheduler.ps1
   ```

✅ **Done!** The task will now run daily at 8:00 AM.

---

### Option 2: Manual Setup via Task Scheduler GUI

1. Press **Windows Key + R** and type: `taskschd.msc` then press Enter
2. Click **"Create Basic Task..."** in the right panel
3. Fill in the wizard:

   **Name**: `Buongiorno_Daily_Update`
   **Description**: `Runs the Buongiorno gold price prediction pipeline daily`

4. **Trigger**: Select **"Daily"**, then click **Next**
5. **Time**: Set to **8:00 AM**, click **Next**
6. **Action**: Select **"Start a program"**, click **Next**
7. **Program/script**: Browse and select:
   ```
   C:\Users\danie\Desktop\Python\buon_giorno\run_update.bat
   ```
8. **Start in (optional)**: Enter:
   ```
   C:\Users\danie\Desktop\Python\buon_giorno
   ```
9. Click **Finish**

---

### Option 3: Command Line (Run CMD as Administrator)

1. **Right-click** on **Command Prompt** and select **"Run as Administrator"**
2. Run this command:
   ```cmd
   schtasks /Create /TN "Buongiorno_Daily_Update" /TR "C:\Users\danie\Desktop\Python\buon_giorno\run_update.bat" /SC DAILY /ST 08:00 /RL HIGHEST /F
   ```

---

## 🧪 Testing the Scheduled Task

After creating the task, test it manually:

### Using Task Scheduler GUI:
1. Open Task Scheduler (`taskschd.msc`)
2. Find **"Buongiorno_Daily_Update"** in the task list
3. **Right-click** → **Run**
4. Check the logs folder: `logs/update_YYYYMMDD.log`

### Using PowerShell:
```powershell
Start-ScheduledTask -TaskName "Buongiorno_Daily_Update"
```

### Using Command Prompt:
```cmd
schtasks /Run /TN "Buongiorno_Daily_Update"
```

---

## 📊 Verifying the Task

Check if the task was created successfully:

### PowerShell:
```powershell
Get-ScheduledTask -TaskName "Buongiorno_Daily_Update"
```

### Command Prompt:
```cmd
schtasks /Query /TN "Buongiorno_Daily_Update"
```

---

## 🔧 Task Settings

The scheduled task is configured with:
- **Schedule**: Daily at 8:00 AM
- **Execution Time Limit**: 30 minutes
- **Run on battery**: Yes (for laptops)
- **Wake computer to run**: No (by default)
- **Network required**: Yes
- **Run whether user is logged on or not**: No (runs only when logged in)

---

## 📝 What Happens Each Day

1. At **8:00 AM**, the task runs `run_update.bat`
2. The batch file activates the conda environment
3. It executes `update_daily.py`
4. The pipeline:
   - Fetches latest gold price data from Yahoo Finance
   - Processes the data
   - Engineers features
   - Trains both ARIMA and Moving Average models
   - Generates prediction for the next day
   - Saves results to CSV files
5. All output is logged to `logs/update_YYYYMMDD.log`
6. The API automatically serves the new prediction

---

## 🗑️ Removing the Scheduled Task

If you need to remove the task:

### PowerShell (as Administrator):
```powershell
Unregister-ScheduledTask -TaskName "Buongiorno_Daily_Update" -Confirm:$false
```

### Command Prompt (as Administrator):
```cmd
schtasks /Delete /TN "Buongiorno_Daily_Update" /F
```

---

## 🔍 Troubleshooting

**Task doesn't run:**
- Check that the conda environment path in `run_update.bat` is correct
- Ensure you're logged in at the scheduled time
- Check Windows Event Viewer for errors

**Permission errors:**
- Make sure you ran the setup as Administrator
- Verify the user account has access to the project folder

**Script fails:**
- Check the log file in `logs/` folder
- Manually run `run_update.bat` to see errors

---

## 📞 Need Help?

If you encounter issues, check:
1. Log files in `logs/update_YYYYMMDD.log`
2. Task Scheduler history (enable it in Task Scheduler Library)
3. Windows Event Viewer → Windows Logs → Application
