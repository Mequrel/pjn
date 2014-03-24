cat $1 | tr '[[:upper:]]' '[[:lower:]]' | tr -s '[[:punct:][:space:]]' '\n' | sort | uniq -c | sort -n -r
