package main
import (
	"database/sql"
	"fmt"
	"log"
	"os"
	"os/user"
	"path/filepath"
	"time"
	"github.com/xuri/excelize/v2"
	_ "github.com/mattn/go-sqlite3"
)
func main() {
	// Get the current user
	usr, err := user.Current()
	if err != nil {
		log.Fatal(err)
	}
	// Path to the Chrome History file
	chromeHistoryPath := filepath.Join(usr.HomeDir, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "History")
	// Copy the History file to avoid locking issues
	tempPath := filepath.Join(os.TempDir(), "ChromeHistoryCopy")
	err = copyFile(chromeHistoryPath, tempPath)
	if err != nil {
		log.Fatalf("Failed to copy history file: %v", err)
	}
	defer os.Remove(tempPath)
	// Open SQLite database
	db, err := sql.Open("sqlite3", tempPath)
	if err != nil {
		log.Fatalf("Failed to open database: %v", err)
	}
	defer db.Close()
	// Query to get the browsing history
	query := `SELECT url, title, visit_count, last_visit_time FROM urls ORDER BY last_visit_time DESC`
	rows, err := db.Query(query)
	if err != nil {
		log.Fatalf("Failed to execute query: %v", err)
	}
	defer rows.Close()
	// Create a new Excel file
	f := excelize.NewFile()
	sheet := "History"
	f.NewSheet(sheet)
	f.SetSheetRow(sheet, "A1", &[]interface{}{"URL", "Title", "Visit Count", "Last Visit Time"})
	// Write the browsing history to the Excel file
	rowIndex := 2
	for rows.Next() {
		var url, title string
		var visitCount int
		var lastVisitTime int64
		// Scan the row data into variables (use pointers)
		err := rows.Scan(&url, &title, &visitCount, &lastVisitTime)
		if err != nil {
			log.Fatalf("Failed to scan row: %v", err)
		}
		// Convert Chrome's last visit time (Webkit time) to a human-readable format
		convertedTime := chromeTimeToUnix(lastVisitTime)
		// Write the data to the Excel file
		row := fmt.Sprintf("A%d", rowIndex)
		f.SetSheetRow(sheet, row, &[]interface{}{url, title, visitCount, convertedTime})
		rowIndex++
	}
	if err = rows.Err(); err != nil {
		log.Fatalf("Failed during rows iteration: %v", err)
	}
	// Save the Excel file
	excelFileName := "ChromeHistory.xlsx"
	if err := f.SaveAs(excelFileName); err != nil {
		log.Fatalf("Failed to save Excel file: %v", err)
	}
	fmt.Printf("Browsing history exported to %s\n", excelFileName)
}
// copyFile copies the file from source to destination
func copyFile(source, destination string) error {
	srcFile, err := os.Open(source)
	if err != nil {
		return err
	}
	defer srcFile.Close()
	dstFile, err := os.Create(destination)
	if err != nil {
		return err
	}
	defer dstFile.Close()
	_, err = dstFile.ReadFrom(srcFile)
	return err
}
// chromeTimeToUnix converts Chrome/Webkit timestamp to Unix timestamp
func chromeTimeToUnix(webkitTime int64) string {
	// Webkit/Chrome time is in microseconds since January 1, 1601
	const webkitEpochStart = 11644473600000000
	// Convert Webkit time to Unix time
	unixTime := (webkitTime - webkitEpochStart) / 1000000
	return time.Unix(unixTime, 0).Format("2006-01-02 15:04:05")
}
