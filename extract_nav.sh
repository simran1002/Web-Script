#!/bin/bash

# File to save raw data
curl -s "https://www.amfiindia.com/spages/NAVAll.txt" -o nav.txt

# Output TSV file
output_file="scheme_nav.tsv"
echo -e "Scheme Name\tAsset Value" > "$output_file"

# Extract and format
awk -F ';' '
BEGIN { OFS="\t" }
/^[0-9]+;/ {
    scheme = $4
    nav = $5
    if (scheme && nav) {
        print scheme, nav
    }
}' nav.txt >> "$output_file"

echo "✅ Extracted Scheme Name and NAV into $output_file"
