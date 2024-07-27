# Set the path to your Python script
$pythonScriptPath = "C:\Path\To\Script.py"

# Check if the Python script exists
if (-Not (Test-Path $pythonScriptPath)) {
    Write-Error "Python script not found at $pythonScriptPath"
    exit
}

# Run the Python script with PowerShell hidden
Start-Process -FilePath "pythonw" -ArgumentList $pythonScriptPath -WindowStyle Hidden
