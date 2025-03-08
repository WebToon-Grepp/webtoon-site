def format_weekday(day, complete):
    weekdays = ["월요", "화요", "수요", "목요", "금요", "토요", "일요", "완결"]
    if complete:
        day = 7
    return weekdays[day]

def format_number(num):
    if num and num >= 10000:
        return f"{int(num) / 10000:.1f}만" 
    return check_number(num)

def check_number(num):
    try: 
        return f"{int(num):,}"
    except:
        return "집계안됨"

def generate_title_html(title_data):
    platform, id, title, author, image_url, views, likes, comments, release_day, is_completed = title_data[0]

    thumbnail_url = f"{image_url}.png" if platform == 'kakao' else image_url
    platform_icon_url = "static/images/kakao.ico" if platform == 'kakao' else "static/images/naver.ico"
    url = f"https://webtoon.kakao.com/content/{id}/{id}" \
          if platform == 'kakao' else \
          f"https://comic.naver.com/webtoon/list?titleId={id}"

    title_content = f"""
    <div class="title-item">
        <div class="title-item-info">
            <a class="thumbnail-container" href="{url}">
                <img class="thumbnail" src="{thumbnail_url}">
                <div class="weekday">{format_weekday(release_day, is_completed)} 웹툰</div>
            </a>
            <div>
            <div class="title-item-detail">
                <div class="title">{title}</div>
                <img class="platform" src="{platform_icon_url}">
            </div>
            <div class="title-item-detail">
                <div class="author">{author}</div>
            </div>
            <ul class="info">
                <li>
                    <img src="static/images/views.png">
                    <p>{format_number(views)}</p>
                </li>
                <li>
                    <img src="static/images/likes.png">
                    <p>{format_number(likes)}</p>
                </li>
                <li>
                    <img src="static/images/comments.png">
                    <p>{format_number(comments)}</p>
                </li>
            <ul>
            </div>
        </div>
    </div>
    """
    
    return title_content

def generate_episode_html(episode_data):
    episode_content = ""
    
    seen_episodes = []
    for episode in episode_data:
        platform, title_id, id, title, likes, comments, image_url, updated_data = episode
        if (title_id, id) in seen_episodes:
            continue
        seen_episodes.append((title_id, id))

        thumbnail_url = f"{image_url}.jpg" if platform == 'kakao' else image_url
        url = f"https://webtoon.kakao.com/viewer/{title_id}/{id}" \
              if platform == 'kakao' else \
              f"https://comic.naver.com/webtoon/detail?titleId={title_id}&no={id}"

        episode_content += f"""
        <li class="episode-item">
            <a href="{url}" class="episode-item-link">
                <div style="display: flex;">
                    <img class="thumbnail" src="{thumbnail_url}">
                    <div class="episode-item-info">
                        <div class="title">{title}</div>
                        <div class="author">{updated_data}</div>
                    </div>
                </div>
                <div class="episode-item-detail">
                    <div class="author">좋아요수 {check_number(likes)}</div>
                    <div class="author">댓글수 {check_number(comments)}</div>
                </div>
            </a>
        </li>
        """
    
    return episode_content

def generate_html(webtoon_data):
    grid_content, list_content = "", ""
    
    seen_webtoons = []
    for webtoon in webtoon_data:
        platform, id, title, author, image_url, views, likes, comments, release_day, is_completed = webtoon
        if (platform, id) in seen_webtoons:
            continue
        seen_webtoons.append((platform, id))

        thumbnail_url = f"{image_url}.png" if platform == 'kakao' else image_url
        platform_icon_url = "static/images/kakao.ico" if platform == 'kakao' else "static/images/naver.ico"
        data_filter = f"{platform}_{id}_{views}_"

        grid_content += f"""
        <a class="grid-item-link" href="episode?platform={platform}&id={id}">
            <div class="grid-item">
                <img class="thumbnail" src="{thumbnail_url}">
                <div class="grid-item-info">
                    <img class="platform" src="{platform_icon_url}">
                    <div class="title">{title.replace(',', ',<br>')
                                             .replace(':', ':<br>')
                                             .replace('[', '<br>[').strip()}</div>
                    <div class="author">{author.split('/')[0].strip()}</div>
                </div>
            </div>
        </a>
        """

        list_content += f"""
        <li class="list-item">
            <a class="list-item-link" href="episode?platform={platform}&id={id}">
                <img class="thumbnail" src="{thumbnail_url}">
                <div class="list-item-info">
                    <div class="list-item-detail">
                        <div class="title">{title}</div>
                        <img class="platform" src="{platform_icon_url}">
                    </div>
                    <div class="author">{author}</div>
                </div>
            </a>
        </li>
        """
    
    return grid_content, list_content
