# save as load-env.ps1 in the same folder as your .env
param(
    [string]$EnvFile = ".env"
)

if (-Not (Test-Path $EnvFile)) {
    Write-Error "File '$EnvFile' not found."
    exit 1
}

Get-Content $EnvFile | ForEach-Object {
    # Remove whitespace at start/end
    $line = $_.Trim()

    # Skip empty lines or comments
    if ($line -eq "" -or $line.StartsWith("#")) { return }

    # Match KEY=VALUE
    if ($line -match "^\s*([^=]+?)\s*=\s*(.*)$") {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()

        # Remove surrounding quotes if present
        if (($value.StartsWith('"') -and $value.EndsWith('"')) -or
            ($value.StartsWith("'") -and $value.EndsWith("'"))) {
            $value = $value.Substring(1, $value.Length - 2)
        }

        # Set environment variable for current process
        [System.Environment]::SetEnvironmentVariable($key, $value, "Process")
        Write-Host "Loaded $key=$value"
    } else {
        Write-Warning "Skipping invalid line: $line"
    }
}
