package main

import (
    "database/sql"
    "encoding/csv"
    "fmt"
    "log"
    "os"
    "strings"

    _ "github.com/mattn/go-sqlite3"
)

func main() {
    // Path to the SRUM.db file
    dbPath := "C:\\Windows\\System32\\sru\\SRUM.db"
    
    // Connect to the SQLite database
    db, err := sql.Open("sqlite3", dbPath)
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    // Retrieve the list of tables in the database
    tables, err := getTables(db)
    if err != nil {
        log.Fatal(err)
    }

    // Create a single CSV file
    csvFile, err := os.Create("SRUM.csv")
    if err != nil {
        log.Fatal(err)
    }
    defer csvFile.Close()

    writer := csv.NewWriter(csvFile)
    defer writer.Flush()

    // Export each table to the single CSV file
    for _, table := range tables {
        if err := exportTableToSingleCSV(db, table, writer); err != nil {
            log.Printf("Failed to export table %s: %v", table, err)
        } else {
            fmt.Printf("Successfully exported table %s\n", table)
        }
    }
}

// getTables retrieves the list of tables in the SQLite database
func getTables(db *sql.DB) ([]string, error) {
    query := `SELECT name FROM sqlite_master WHERE type='table';`
    rows, err := db.Query(query)
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    var tables []string
    for rows.Next() {
        var table string
        if err := rows.Scan(&table); err != nil {
            return nil, err
        }
        tables = append(tables, table)
    }
    return tables, rows.Err()
}

// exportTableToSingleCSV exports the specified table to a single CSV file
func exportTableToSingleCSV(db *sql.DB, table string, writer *csv.Writer) error {
    query := fmt.Sprintf("SELECT * FROM %s", table)
    rows, err := db.Query(query)
    if err != nil {
        return err
    }
    defer rows.Close()

    // Get column names
    columns, err := rows.Columns()
    if err != nil {
        return err
    }

    // Write table name as a header
    if err := writer.Write([]string{fmt.Sprintf("Table: %s", table)}); err != nil {
        return err
    }

    // Write column names to CSV
    if err := writer.Write(columns); err != nil {
        return err
    }

    // Write rows to CSV
    for rows.Next() {
        columns := make([]interface{}, len(columns))
        columnPointers := make([]interface{}, len(columns))
        for i := range columns {
            columnPointers[i] = &columns[i]
        }

        if err := rows.Scan(columnPointers...); err != nil {
            return err
        }

        record := make([]string, len(columns))
        for i, col := range columns {
            if col != nil {
                record[i] = fmt.Sprintf("%v", col)
            }
        }

        if err := writer.Write(record); err != nil {
            return err
        }
    }

    // Add an empty line to separate tables in the CSV
    if err := writer.Write([]string{}); err != nil {
        return err
    }

    return rows.Err()
}
