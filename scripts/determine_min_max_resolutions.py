import csv

# the resolutions.txt file can be generated with the following command (on unix)
# find <samples folder> -type f | xargs -d "\n" identify | cut -d "/" -f4 | cut -d " " -f3 | sed -r 's/x/, /g' > resolutions.txt
min_res = 1e12
min_res_detail = None
max_res = 0
max_res_detail = None
with open("./resolutions.txt") as f:
    csv = csv.reader(f, delimiter=",")
    for row in csv:
        res = int(row[0]) * int(row[1])
        if res < min_res:
            min_res = res
            min_res_detail = (int(row[0]), int(row[1]))
        if res > max_res:
            max_res = res
            max_res_detail = (int(row[0]), int(row[1]))
print(min_res_detail, max_res_detail)
