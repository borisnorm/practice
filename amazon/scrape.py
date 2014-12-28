import requests, lxml.html, re, csv
from dateutil.parser import parse

posts = []

regex = re.compile(r"Set (\d+)")
other_counter = 1

for i in range(12, 0, -1):
    response = requests.get("http://www.geeksforgeeks.org/tag/amazon/page/%d/" % i)
    doc = lxml.html.fromstring(response.content)
    # post-date
    for item in doc.cssselect(".post-info"):
        title = item.cssselect('.post-title a')[0].text.replace("Amazon interview Experience", "").replace("Amazon Interview Experience", "").replace("Amazon Interview Questions", "").replace("Amazon Interview", "").replace(" | ", "").strip()
        url = item.cssselect('.post-title a')[0].get('href')
        title_url = "[%s](%s)" % (title, url)
        date = item.cssselect('.post-date')[0].text
        try:
            pydate = parse(date)
        except:
            pass
        matches = re.findall(regex, title)
        if matches:
            posts.append(("set" + str(matches[0]).zfill(3), title_url, date, pydate))
        else:
            posts.append(("other" + str(other_counter).zfill(3), title_url, date, pydate))
            other_counter += 1
        print(posts[-1])

posts = sorted(posts, key=lambda x: x[3], reverse=True)

f = open("posts.csv", "w")
writer = csv.writer(f)
writer.writerow(["Title", "Date"])
for post in posts:
    writer.writerow(post[1:3])
f.close()