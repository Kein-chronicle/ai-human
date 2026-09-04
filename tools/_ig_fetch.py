
import urllib.request, json, re, sys
handle = sys.argv[1]
url = "https://www.instagram.com/{}/media/?__a=1".format(handle)
req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36","Accept":"application/json"})
try:
    resp = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
    j = json.loads(resp)
    items = j.get("items", [])
    if not items:
        print("none")
        sys.exit(0)
    item = items[0]
    post_id = str(item.get("pk", ""))
    shortcode = item.get("code", "")
    caption_list = item.get("caption", {})
    caption_text = ""
    if isinstance(caption_list, dict):
        caption_text = caption_list.get("text", "")[:200]
    likes = item.get("like_count", 0)
    comments = item.get("comment_count", 0)
    timestamp = item.get("taken_at", 0)
    print(json.dumps({"id": post_id, "shortcode": shortcode, "caption": caption_text, "likes": likes, "comments": comments, "timestamp": timestamp}))
except Exception as e:
    print("none")
