# Function to get Chrome extensions
function Get-ChromeExtensions {
    param([string]$Username)

    # Path to Chrome's user data directory
    $UserDataPath = "C:\Users\$Username\AppData\Local\Google\Chrome\User Data\Default"
    
    # Check if the directory exists
    if (-not (Test-Path $UserDataPath -PathType Container)) {
        Write-Host "Chrome user data directory not found."
        return
    }

    # Connect to Chrome's Extensions SQLite database
    try {
        $ExtensionsDbPath = Join-Path $UserDataPath "Extensions"

        # Get extensions data
        $ExtensionsData = Invoke-SqliteQuery -DataSource $ExtensionsDbPath -Query "SELECT * FROM extensions"
        if ($ExtensionsData -eq $null) {
            Write-Host "No extensions found."
            return
        }

        # Output extensions data
        $ExtensionsData

    } catch {
        Write-Host "Error accessing Chrome extensions data: $_"
    }
}

# Function to execute SQLite query
function Invoke-SqliteQuery {
    param(
        [string]$DataSource,
        [string]$Query
    )

    try {
        $ConnectionString = "Data Source=$DataSource"
        $Connection = New-Object -TypeName System.Data.SQLite.SQLiteConnection -ArgumentList $ConnectionString
        $Command = $Connection.CreateCommand()
        $Command.CommandText = $Query
        $Connection.Open()
        $Reader = $Command.ExecuteReader()

        $Table = New-Object System.Data.DataTable
        $Table.Load($Reader)

        $Reader.Close()
        $Connection.Close()

        return $Table

    } catch {
        Write-Host "SQLite error: $_"
        return $null
    }
}

# Prompt user to enter username
$Username = Read-Host "Enter the username"

# Call the function to get Chrome extensions
Get-ChromeExtensions -Username $Username