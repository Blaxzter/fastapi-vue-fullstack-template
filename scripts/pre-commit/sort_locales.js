#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

// Path to the locales directory
const localesDir = path.join(__dirname, "../../frontend/src/locales");

// Function to sort a JSON object recursively
function sortJsonObject(jsonObj) {
    if (typeof jsonObj !== "object" || jsonObj === null) {
        return jsonObj;
    }

    if (Array.isArray(jsonObj)) {
        return jsonObj.map(sortJsonObject);
    }

    const sortedObj = {};
    const keys = Object.keys(jsonObj).sort();

    for (const key of keys) {
        sortedObj[key] = sortJsonObject(jsonObj[key]);
    }

    return sortedObj;
}

// Function to recursively find all JSON files in a directory
function findJsonFiles(dir) {
    const jsonFiles = [];
    const items = fs.readdirSync(dir);

    for (const item of items) {
        const itemPath = path.join(dir, item);
        const stats = fs.statSync(itemPath);

        if (stats.isDirectory()) {
            // Recursively search subdirectories
            jsonFiles.push(...findJsonFiles(itemPath));
        } else if (stats.isFile() && item.endsWith(".json")) {
            jsonFiles.push(itemPath);
        }
    }

    return jsonFiles;
}

// Function to detect the line ending style of a file
function detectLineEnding(content) {
    // Default to LF if we can't determine
    if (!content || content.length === 0) return "\n";

    const indexOfLF = content.indexOf("\n");
    if (indexOfLF === -1) return "\n"; // No line breaks found

    // Check if there's a CR before the LF
    if (indexOfLF > 0 && content[indexOfLF - 1] === "\r") {
        return "\r\n"; // CRLF
    } else {
        return "\n"; // LF
    }
}

// Main function to read, sort, and write back JSON files
function sortLocaleFiles() {
    try {
        const jsonFiles = findJsonFiles(localesDir);

        for (const filePath of jsonFiles) {
            const relativePath = path.relative(localesDir, filePath);
            console.log(`Sorting ${relativePath}...`);

            // Read file content as buffer to prevent automatic line ending normalization
            const content = fs.readFileSync(filePath, "utf8");

            // Detect original line ending style
            const lineEnding = detectLineEnding(content);

            // Parse JSON
            const jsonData = JSON.parse(content);

            // Sort JSON
            const sortedJsonData = sortJsonObject(jsonData);

            // Write sorted JSON back to file, preserving original line ending style
            // JSON.stringify uses \n for line breaks
            const jsonString = JSON.stringify(sortedJsonData, null, 4);

            // Ensure we use the original line ending style
            const formattedString =
                lineEnding === "\r\n"
                    ? jsonString.replace(/\n/g, "\r\n")
                    : jsonString;

            // Check if original file ended with a line break
            const endsWithLineBreak =
                content.endsWith("\n") || content.endsWith("\r\n");

            fs.writeFileSync(
                filePath,
                endsWithLineBreak
                    ? formattedString + lineEnding
                    : formattedString,
                "utf8",
            );

            console.log(`✓ Sorted ${relativePath}`);
        }

        console.log("All locale files sorted successfully!");
        return true;
    } catch (error) {
        console.error("Error sorting locale files:", error);
        return false;
    }
}

// Execute the sort function
const success = sortLocaleFiles();
process.exit(success ? 0 : 1);
