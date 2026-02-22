@login_required(login_url='login')
def index(request):

    query = request.GET.get("q")

    if query:
        url = (
            "https://www.googleapis.com/youtube/v3/search"
            f"?key={AIzaSyBWgyxeGE5exdHS8Xj-IzyLEZvJ0KgqO0E}"
            f"&q={query}"
            "&part=snippet,id"
            "&type=video"
            "&maxResults=12"
        )
    else:
        url = (
            "https://www.googleapis.com/youtube/v3/search"
            f"?key={AIzaSyBWgyxeGE5exdHS8Xj-IzyLEZvJ0KgqO0E}"
            f"&channelId={https://www.youtube.com/@nopgon-studio}"
            "&part=snippet,id"
            "&order=date"
            "&maxResults=12"
        )

    res = requests.get(url)
    data = res.json()

    videos = []

    for item in data["items"]:
        if item["id"]["kind"] == "youtube#video":
            video_id = item["id"]["videoId"]

            videos.append({
                "title": item["snippet"]["title"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
                "video_url": f"https://www.youtube.com/watch?v={video_id}"
            })

    return render(request, "index.html", {"videos": videos})
