from flask import Flask, render_template, request, jsonify
from fetcher import (
    fetch_data, fetch_genres, fetch_title_data, fetch_episode_data
)
from generator import (
    generate_html, generate_genre_option, generate_title_html, generate_episode_html
)

APP = Flask(__name__)

@APP.route("/episode/content")
def get_episode_content():
    try:
        title_id = request.args.get("id", None)
        title_platform = request.args.get("platform", None)
        sort_type = request.args.get("sort", "id")

        if not title_id and title_platform:
            print("Error occurred: Missing title_id or title_platform")
            return jsonify({"error": "Missing title_id or title_platform"}), 404

        episode_data = fetch_episode_data(title_platform, title_id, sort_type)

        episode_content = generate_episode_html(episode_data)

        return jsonify({
            "episode": episode_content
        }), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "No episode data available"}), 404

@APP.route("/title/content")
def get_title_content():
    try:
        title_id = request.args.get("id", None)
        title_platform = request.args.get("platform", None)

        if not title_id and title_platform:
            print("Error occurred: Missing title_id or title_platform")
            return jsonify({"error": "Missing title_id or title_platform"}), 404

        title_data = fetch_title_data(title_platform, title_id)

        title_content = generate_title_html(title_data)

        return jsonify({
            "title": title_content
        }), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "No title data available"}), 404
    
@APP.route("/genres")
def get_genres():
    try:
        genre_data = fetch_genres()
        genre_option = generate_genre_option(genre_data)

        return jsonify({
            "genres": genre_option
        }), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "No data available"}), 404
    
@APP.route("/content")
def get_content():
    try:
        filter_type = request.args.get("filter", "all")
        platform_type = request.args.get("platform", "all")
        genre_type = request.args.get("genre", "all")
        sort_type = request.args.get("sort", "views")

        webtoon_data = fetch_data(filter_type, platform_type, genre_type, sort_type)

        grid_content, list_content = generate_html(webtoon_data)

        return jsonify({
            "grid": grid_content,
            "list": list_content
        }), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "No data available"}), 404

@APP.route("/episode")
def episode():
    title_id = request.args.get("id", None)
    title_platform = request.args.get("platform", None)
    return render_template("episode.html", data={
        "id": title_id,
        "platform": title_platform
    })

@APP.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    APP.run(host="0.0.0.0")
