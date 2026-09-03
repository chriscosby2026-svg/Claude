#!/usr/bin/env python3
"""Watch a YouTube video with Gemini and print a timestamped transcript + scene breakdown.

Usage:
    python3 scripts/watch_video.py <youtube-url> [--prompt "custom instruction"]

Requires GEMINI_API_KEY (or GOOGLE_API_KEY) in the environment. Get a free key
from Google AI Studio: https://aistudio.google.com/apikey
"""

import argparse
import os
import sys
from urllib.parse import urlparse

YOUTUBE_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "youtu.be",
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

MODEL = "gemini-3.6-flash"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Full YouTube video or Shorts URL")
    parser.add_argument(
        "--prompt",
        default=DEFAULT_PROMPT,
        help="Override the analysis instruction sent to Gemini",
    )
    parser.add_argument("--model", default=MODEL, help="Gemini model to use")
    args = parser.parse_args()

    host = urlparse(args.url).netloc.lower()
    if host not in YOUTUBE_HOSTS:
        print(
            f"Error: this script only supports YouTube video/Shorts URLs.\n"
            f"Got a URL on '{host or args.url}', which Gemini's direct video-URL "
            "ingestion does not support (e.g. Instagram Reels, TikTok, X/Twitter "
            "video, and other platforms are not supported this way).",
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

    response = client.models.generate_content(
        model=args.model,
        contents=types.Content(
            parts=[
                types.Part(file_data=types.FileData(file_uri=args.url)),
                types.Part(text=args.prompt),
            ]
        ),
    )

    print(response.text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
