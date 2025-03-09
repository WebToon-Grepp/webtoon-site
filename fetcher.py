import os
import psycopg2

CONFIG = {
    "dbname": os.getenv("FLASK_DBNAME"),
    "host": os.getenv("FLASK_HOST"),
    "port": os.getenv("FLASK_PORT"),
    "password": os.getenv("FLASK_PASSWORD"),
    "user": os.getenv("FLASK_USER")
}

def get_database_connection():
    try:
        conn = psycopg2.connect(**CONFIG)
        conn.set_client_encoding('UTF8')
        return conn
    except Exception as e:
        print(f"Error connecting to Database: {e}")
        return None

def execute_query(query):
    try:
        print(f"Executing query: {query}")
        conn = get_database_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
            conn.close()
            return rows
        else:
            print("Connection failed")
            return None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None

def build_where_filter(filter=None, platform="all", genre="all"):
    where_conditions = []

    day_mapping = {
        "mon": 0, "tue": 1, "wed": 2, "thu": 3, 
        "fri": 4, "sat": 5, "sun": 6
    }
    
    if filter in day_mapping:
        where_conditions.append(f"release_day = {day_mapping[filter]}")

    if platform != "all":
        where_conditions.append(f"platform = '{platform}'")

    if genre != "all":
        genre_conditions = []
        for genre_name in genre.split(' '):
            genre_conditions.append(f"genre_name LIKE '%{genre_name}%'")
        where_conditions.append(f"({" OR ".join(genre_conditions)})")

    is_completed = filter == "completed"
    where_conditions.append(f"is_completed = {str(is_completed).upper()}")

    return " AND ".join(where_conditions)

def fetch_title_data(platform, id):
    query = f"""
        SELECT 
            platform, 
            id, 
            title, 
            author, 
            image_url, 
            views, 
            likes, 
            comments, 
            release_day, 
            is_completed,
            STRING_AGG(genre_name, '/') AS genre_names
        FROM site.dim_webtoon_titles 
        WHERE platform = '{platform}'
            AND id = {id}
        GROUP BY 
            platform, 
            id, 
            title, 
            author, 
            image_url, 
            views, 
            likes, 
            comments, 
            release_day, 
            is_completed
        LIMIT 1;
    """
    
    return execute_query(query)

def fetch_episode_data(platform, id, sort, limit=100):
    query = f"""
        SELECT 
            * 
        FROM site.fct_webtoon_episodes 
        WHERE platform = '{platform}'
            AND title_id = {id}
        ORDER BY {sort} DESC
        LIMIT {limit};
    """
    return execute_query(query)

def fetch_genres():
    query = f"""
        SELECT 
            genre_name,
            COUNT(*) AS count
        FROM site.dim_webtoon_titles 
        GROUP BY genre_name
        ORDER BY count DESC
        LIMIT 50;
    """
    
    return execute_query(query)


def fetch_data(filter, platform, genre, sort, limit=100):
    where_clause = build_where_filter(filter, platform, genre)
    query = f"""
        SELECT
            * 
        FROM site.dim_webtoon_titles 
        WHERE {where_clause} 
        ORDER BY {sort} DESC 
        LIMIT {limit};
    """
    
    return execute_query(query)
