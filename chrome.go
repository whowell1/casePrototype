package main
import (
	"database/sql"
	"fmt"
	"io"
	"log"
	"os"
	"os/user"
	"path/filepath"
	"time"
	"github.com/xuri/excelize/v2"
	_ "github.com/mattn/go-sqlite3"
)
func main() {
	// Get the current user to locate the Chrome history file
	usr, err := user.Current()
	if err != nil {
		log.Fatalf("Error getting user: %v", err)
	}
	// Define the path to the Chrome History file
	chromeHistoryPath := filepath.Join(usr.HomeDir, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "History")
	// Introduce a small delay to ensure the file is not being written to by Chrome
	time.Sleep(2 * time.Second)
	// Make a temporary copy of the History file to avoid locking issues
	tempPath := filepath.Join(os.TempDir(), "ChromeHistoryCopy")
	err = copyFile(chromeHistoryPath, tempPath)
	if err != nil {
		log.Fatalf("Failed to copy history file: %v", err)
	}
	defer os.Remove(tempPath)
	// Open the copied SQLite database
	db, err := sql.Open("sqlite3", tempPath)
	if err != nil {
		log.Fatalf("Error opening database: %v", err)
	}
	defer db.Close()
	// Query to fetch URL, title, visit count, and last visit time
	query := `SELECT url, title, visit_count, last_visit_time FROM urls ORDER BY last_visit_time DESC`
	rows, err := db.Query(query)
	if err != nil {
		log.Fatalf("Error executing query: %v", err)
	}
	defer rows.Close()
	// Create a new Excel file using excelize
	f := excelize.NewFile()
	sheet := "History"
	f.NewSheet(sheet)
	// Set the header row in the Excel file
	f.SetSheetRow(sheet, "A1", &[]interface{}{"URL", "Title", "Visit Count", "Last Visit Time"})
	// Write rows from the query result to the Excel file
	rowIndex := 2
	for rows.Next() {
		var url, title string
		var visitCount int
		var lastVisitTime int64
		// Scan the database row into Go variables
		err := rows.Scan(&url, &title, &visitCount, &lastVisitTime)
		if err != nil {
			log.Fatalf("Error scanning row: %v", err)
		}
		// Convert the WebKit timestamp to a readable time
		convertedTime := chromeTimeToUnix(lastVisitTime)
		// Write the data to the Excel sheet
		row := fmt.Sprintf("A%d", rowIndex)
		f.SetSheetRow(sheet, row, &[]interface{}{url, title, visitCount, convertedTime})
		rowIndex++
	}
	if err := rows.Err(); err != nil {
		log.Fatalf("Error after scanning rows: %v", err)
	}
	// Save the Excel file
	excelFileName := "ChromeHistory.xlsx"
	if err := f.SaveAs(excelFileName); err != nil {
		log.Fatalf("Error saving Excel file: %v", err)
	}
	fmt.Printf("Browsing history successfully exported to %s\n", excelFileName)
}
// copyFile copies the file from source to destination using io.Copy for more reliable copying
func copyFile(source, destination string) error {
	srcFile, err := os.Open(source)
	if err != nil {
		return fmt.Errorf("Error opening source file: %v", err)
	}
	defer srcFile.Close()
	dstFile, err := os.Create(destination)
	if err != nil {
		return fmt.Errorf("Error creating destination file: %v", err)
	}
	defer dstFile.Close()
	_, err = io.Copy(dstFile, srcFile)
	if err != nil {
		return fmt.Errorf("Error copying file: %v", err)
	}
	return nil
}
// chromeTimeToUnix converts Chrome/Webkit timestamp to Unix timestamp
func chromeTimeToUnix(webkitTime int64) string {
	// Webkit/Chrome time is in microseconds since January 1, 1601
	const webkitEpochStart = 11644473600000000
	// Convert Webkit time to Unix time (seconds since 1970)
	unixTime := (webkitTime - webkitEpochStart) / 1000000
	return time.Unix(unixTime, 0).Format("2006-01-02 15:04:05")
}




















