#!/usr/bin/env python3
"""Watch a YouTube video or Instagram Reel with Gemini and print a timestamped
transcript + scene breakdown.

Usage:
    python3 scripts/watch_video.py <url> [--prompt "custom instruction"]

Requires GEMINI_API_KEY (or GOOGLE_API_KEY) in the environment. Get a free key
from Google AI Studio: https://aistudio.google.com/apikey

YouTube URLs are handed to Gemini directly (native URL ingestion). Instagram
Reel/post URLs are downloaded locally first (via yt-dlp) and the video file is
uploaded to Gemini's Files API, since Gemini cannot fetch Instagram URLs
itself. This requires yt-dlp to be installed (see requirements.txt) and only
works on public content you have the right to view — private or
login-gated posts will fail with a clear error rather than being guessed at.
"""

import argparse
import os
import sys
import tempfile
import time
from urllib.parse import urlparse

YOUTUBE_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "youtu.be",
}

INSTAGRAM_HOSTS = {
    "instagram.com",
    "www.instagram.com",
}

DEFAULT_PROMPT = """Watch this video closely and produce a markdown walkthrough with:

1. A timestamped transcript of everything spoken (mm:ss - text).
2. A timestamped scene breakdown: for each distinct visual scene or on-screen
   change, give the mm:ss range, what is shown on screen (UI, actions, text
   overlays, code, demonstrations), and what is being said during it.
3. A short summary of the overall procedure or workflow being demonstrated,
   as an ordered list of concrete steps someone could follow to reproduce it.

Be precise about timestamps and be concrete about on-screen details (exact
menu items, commands, file names, URLs) since this will be used to turn the
video into step-by-step instructions."""

MODEL = "gemini-2.5-flash"


def classify_host(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if host in YOUTUBE_HOSTS:
        return "youtube"
    if host in INSTAGRAM_HOSTS:
        return "instagram"
    return ""


def download_instagram_video(url: str, dest_dir: str) -> str:
    try:
        import yt_dlp
    except ImportError:
        print(
            "Error: the yt-dlp package is not installed.\n"
            "Install it with: pip install -r scripts/requirements.txt",
            file=sys.stderr,
        )
        raise SystemExit(1)

    ydl_opts = {
        "outtmpl": os.path.join(dest_dir, "%(id)s.%(ext)s"),
        "format": "mp4/best",
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
    except yt_dlp.utils.DownloadError as e:
        print(
            f"Error: could not download this Instagram post: {e}\n"
            "This usually means the post is private, login-gated, age-restricted, "
            "or was removed. Only public Reels/posts you have the right to view "
            "can be watched this way.",
            file=sys.stderr,
        )
        raise SystemExit(1)


def upload_and_wait(client, path: str):
    uploaded = client.files.upload(file=path)
    while uploaded.state.name == "PROCESSING":
        time.sleep(2)
        uploaded = client.files.get(name=uploaded.name)
    if uploaded.state.name == "FAILED":
        print(f"Error: Gemini failed to process the uploaded video: {uploaded.error}", file=sys.stderr)
        raise SystemExit(1)
    return uploaded


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Full YouTube video/Shorts URL or Instagram Reel/post URL")
    parser.add_argument(
        "--prompt",
        default=DEFAULT_PROMPT,
        help="Override the analysis instruction sent to Gemini",
    )
    parser.add_argument("--model", default=MODEL, help="Gemini model to use")
    args = parser.parse_args()

    platform = classify_host(args.url)
    if not platform:
        host = urlparse(args.url).netloc.lower()
        print(
            f"Error: unsupported URL host '{host or args.url}'.\n"
            "Supported: YouTube (youtube.com, youtu.be) and Instagram "
            "(instagram.com) Reels/posts. TikTok, X/Twitter video, Vimeo, "
            "and other platforms are not supported.",
            file=sys.stderr,
        )
        return 1

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print(
            "Error: set GEMINI_API_KEY (or GOOGLE_API_KEY) in the environment.\n"
            "Get a free key at https://aistudio.google.com/apikey",
            file=sys.stderr,
        )
        return 1

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print(
            "Error: the google-genai package is not installed.\n"
            "Install it with: pip install -r scripts/requirements.txt",
            file=sys.stderr,
        )
        return 1

    client = genai.Client(api_key=api_key)

    if platform == "youtube":
        contents = types.Content(
            parts=[
                types.Part(file_data=types.FileData(file_uri=args.url)),
                types.Part(text=args.prompt),
            ]
        )
        response = client.models.generate_content(model=args.model, contents=contents)
        print(response.text)
        return 0

    # platform == "instagram": download locally, then upload the file to
    # Gemini's Files API, since Gemini can't fetch Instagram URLs directly.
    with tempfile.TemporaryDirectory() as tmp_dir:
        video_path = download_instagram_video(args.url, tmp_dir)
        uploaded = upload_and_wait(client, video_path)
        contents = types.Content(
            parts=[
                types.Part(file_data=types.FileData(file_uri=uploaded.uri, mime_type=uploaded.mime_type)),
                types.Part(text=args.prompt),
            ]
        )
        response = client.models.generate_content(model=args.model, contents=contents)
        print(response.text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
