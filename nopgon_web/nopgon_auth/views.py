import random
import requests

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages

from .models import Profile


# ======================
# 유튜브 설정
# ======================
API_KEY = "AIzaSyBWgyxeGE5exdHS8Xj-IzyLEZvJ0KgqO0E"
CHANNEL_ID = "UCN3kFn3Sbx9JY3QYhd5fvvA"


# ======================
# 메인 페이지 (영상 + 검색 + 추천)
# ======================
def index(request):

    if not request.user.is_authenticated:
        return redirect('login')

    query = request.GET.get('q', '').lower()
    shuffle = request.GET.get('shuffle')

    url = (
        "https://www.googleapis.com/youtube/v3/search"
        f"?key={API_KEY}"
        f"&channelId={CHANNEL_ID}"
        "&part=snippet,id"
        "&order=date"
        "&maxResults=20"
    )

    res = requests.get(url)
    data = res.json()

    videos = []

    for item in data.get("items", []):
        if item["id"]["kind"] != "youtube#video":
            continue

        title = item["snippet"]["title"]

        # 🔍 검색 필터
        if query and query not in title.lower():
            continue

        video_id = item["id"]["videoId"]

        videos.append({
            "title": title,
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
            "video_url": f"https://www.youtube.com/watch?v={video_id}",
        })

    # ⭐ 추천 영상 (검색 안 할 때만)
    recommended = []
    if not query:
        recommended = random.sample(videos, min(len(videos), 6))

    return render(request, "nopgon_auth/index.html", {
        "videos": videos,
        "recommended": recommended,
        "query": query,
    })

#shop
def shop(request):

    if not request.user.is_authenticated:
        return redirect('login')

    products = [
        {
            "name": "NOGON Hoodie",
            "price": "39,000₩",
            "image": "/static/img/sample1.jpg",
        },
        {
            "name": "NOGON T-shirt",
            "price": "29,000₩",
            "image": "/static/img/sample2.jpg",
        },
    ]

    return render(request, 'nopgon_auth/shop.html', {
        "products": products
    })

# ======================
# 로그인
# ======================
def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            if not user.is_active:
                messages.error(request, '비활성 계정입니다')
                return redirect('login')

            login(request, user)
            return redirect('index')

        messages.error(request, '아이디 또는 비밀번호가 틀렸습니다')
        return redirect('login')

    return render(request, 'nopgon_auth/login.html')


# ======================
# 회원가입
# ======================
def signup_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, '이미 존재하는 아이디입니다')
            return redirect('signup')

        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            password=password
        )

        # ⭐ 프로필 자동 생성
        Profile.objects.create(
            user=user,
            role='user'
        )

        messages.success(request, '회원가입 완료')
        return redirect('login')

    return render(request, 'nopgon_auth/signup.html')


# ======================
# 로그아웃
# ======================
def logout_view(request):
    logout(request)
    return redirect('login')


# ======================
# 프로필 페이지
# ======================
def profile_view(request):

    if not request.user.is_authenticated:
        return redirect('login')

    profile, _ = Profile.objects.get_or_create(user=request.user)

    return render(request, 'nopgon_auth/profile.html', {
        'profile': profile
    })
