from urllib.parse import urlparse, parse_qs

def get_youtube_video_id(url):
    """
    Extract the video ID from a YouTube URL (both standard and short formats).

    Args:
        url (str): The YouTube URL.

    Returns:
        str: The video ID if found, otherwise None.
    """
    parsed_url = urlparse(url)

    # Handle standard YouTube URLs
    if parsed_url.netloc in ("www.youtube.com", "youtube.com"):
        query_params = parse_qs(parsed_url.query)
        return query_params.get("v", [None])[0]

    # Handle youtu.be short URLs
    if parsed_url.netloc in ("youtu.be",):
        return parsed_url.path.lstrip("/")  # Video ID is the path

    return None
