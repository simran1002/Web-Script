curl -s "https://www.amfiindia.com/spages/NAVAll.txt" -o nav.txt


output_file="scheme_nav.tsv"
echo -e "Scheme Name\tAsset Value" > "$output_file"

awk -F ';' '
BEGIN { OFS="\t" }
/^[0-9]+;/ {
    scheme = $4
    nav = $5
    if (scheme && nav) {
        print scheme, nav
    }
}' nav.txt >> "$output_file"

echo "Extracted Scheme Name and NAV into $output_file"
