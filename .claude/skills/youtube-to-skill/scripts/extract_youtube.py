#!/usr/bin/env python3
"""
YouTube Transcript Extractor

Extracts transcripts and metadata from YouTube videos or playlists.
Supports YouTube captions and falls back to Whisper for audio transcription.

Usage:
    python extract_youtube.py <video_or_playlist_url>
    python extract_youtube.py <url> --whisper  # Force Whisper transcription

Output:
    JSON to stdout with video metadata and transcript(s)

Dependencies:
    pip install youtube-transcript-api yt-dlp
    # Optional for Whisper fallback: pip install openai-whisper
"""

import argparse
import json
import sys
import re
from datetime import datetime
from typing import Optional

def check_dependencies():
    """Check and report missing dependencies."""
    missing = []

    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        missing.append("youtube-transcript-api")

    try:
        import yt_dlp
    except ImportError:
        missing.append("yt-dlp")

    if missing:
        print(json.dumps({
            "error": "Missing dependencies",
            "install": f"pip install {' '.join(missing)}",
            "missing": missing
        }))
        sys.exit(1)

check_dependencies()

from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp


def extract_video_id(url: str) -> Optional[str]:
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r'(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:embed/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def extract_playlist_id(url: str) -> Optional[str]:
    """Extract playlist ID from YouTube URL."""
    match = re.search(r'list=([a-zA-Z0-9_-]+)', url)
    return match.group(1) if match else None


def get_video_metadata(video_id: str) -> dict:
    """Fetch video metadata using yt-dlp."""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)

            # Parse upload date
            upload_date = info.get("upload_date", "")
            if upload_date and len(upload_date) == 8:
                formatted_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"
            else:
                formatted_date = upload_date or "Unknown"

            return {
                "video_id": video_id,
                "title": info.get("title", "Unknown"),
                "channel": info.get("channel", info.get("uploader", "Unknown")),
                "publish_date": formatted_date,
                "duration_seconds": info.get("duration", 0),
                "description": info.get("description", ""),
                "url": f"https://www.youtube.com/watch?v={video_id}"
            }
    except Exception as e:
        return {
            "video_id": video_id,
            "title": "Unknown",
            "channel": "Unknown",
            "publish_date": "Unknown",
            "duration_seconds": 0,
            "description": "",
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "metadata_error": str(e)
        }


def get_transcript_from_captions(video_id: str) -> Optional[dict]:
    """Try to get transcript from YouTube captions using new API (v1.0+)."""
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)

        # Convert to list for easier handling
        available = list(transcript_list)

        if not available:
            return None

        # Prefer manually created English transcripts
        selected = None
        for t in available:
            if t.language_code in ['en', 'en-US', 'en-GB']:
                if not t.is_generated:
                    selected = t
                    break
                elif selected is None or selected.is_generated:
                    selected = t

        # Fall back to any available transcript
        if selected is None:
            selected = available[0]

        # Fetch the transcript
        transcript_data = selected.fetch()

        # Build full text and segments
        full_text = ""
        segments = []

        for snippet in transcript_data.snippets:
            segments.append({
                "start": snippet.start,
                "duration": snippet.duration,
                "text": snippet.text
            })
            full_text += snippet.text + " "

        return {
            "source": "youtube_captions",
            "language": selected.language,
            "language_code": selected.language_code,
            "is_generated": selected.is_generated,
            "full_text": full_text.strip(),
            "segments": segments
        }

    except Exception as e:
        error_str = str(e)
        if "disabled" in error_str.lower() or "no transcript" in error_str.lower():
            return None
        return {"error": f"Caption extraction failed: {error_str}"}


def get_transcript_from_whisper(video_id: str) -> Optional[dict]:
    """Download audio and transcribe with Whisper (if available)."""
    try:
        import whisper
        import tempfile
        import os

        # Download audio only
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'outtmpl': os.path.join(tempfile.gettempdir(), f'{video_id}.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])

        audio_path = os.path.join(tempfile.gettempdir(), f"{video_id}.mp3")

        # Transcribe with Whisper
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)

        # Clean up
        os.remove(audio_path)

        segments = [{
            "start": seg["start"],
            "duration": seg["end"] - seg["start"],
            "text": seg["text"]
        } for seg in result["segments"]]

        return {
            "source": "whisper",
            "language": result.get("language", "en"),
            "is_generated": True,
            "full_text": result["text"],
            "segments": segments
        }

    except ImportError:
        return {"error": "Whisper not installed. Install with: pip install openai-whisper"}
    except Exception as e:
        return {"error": f"Whisper transcription failed: {str(e)}"}


def get_playlist_videos(playlist_id: str) -> list:
    """Get all video IDs from a playlist."""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
        'playlistend': 50,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(
                f"https://www.youtube.com/playlist?list={playlist_id}",
                download=False
            )

            videos = []
            for entry in playlist_info.get("entries", []):
                if entry:
                    videos.append({
                        "video_id": entry.get("id"),
                        "title": entry.get("title", "Unknown"),
                        "duration": entry.get("duration", 0)
                    })

            return videos
    except Exception as e:
        return [{"error": str(e)}]


def process_video(video_id: str, use_whisper: bool = False) -> dict:
    """Process a single video: get metadata and transcript."""
    result = get_video_metadata(video_id)

    # Try captions first (unless whisper forced)
    if not use_whisper:
        transcript = get_transcript_from_captions(video_id)
        if transcript and "error" not in transcript:
            result["transcript"] = transcript
            return result

    # Fall back to Whisper or if forced
    if use_whisper or not result.get("transcript"):
        transcript = get_transcript_from_whisper(video_id)
        if transcript:
            result["transcript"] = transcript
        else:
            result["transcript"] = {
                "error": "No transcript available. Video may not have captions and Whisper is not installed."
            }

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Extract transcripts from YouTube videos or playlists"
    )
    parser.add_argument("url", help="YouTube video or playlist URL")
    parser.add_argument(
        "--whisper",
        action="store_true",
        help="Force Whisper transcription instead of YouTube captions"
    )
    parser.add_argument(
        "--playlist-info-only",
        action="store_true",
        help="For playlists, only list videos without extracting transcripts"
    )

    args = parser.parse_args()

    # Determine if URL is video or playlist
    playlist_id = extract_playlist_id(args.url)
    video_id = extract_video_id(args.url)

    output = {
        "extracted_at": datetime.utcnow().isoformat() + "Z",
        "source_url": args.url
    }

    if playlist_id and "watch" not in args.url:
        # It's a playlist URL
        output["type"] = "playlist"
        output["playlist_id"] = playlist_id

        videos = get_playlist_videos(playlist_id)
        output["video_count"] = len(videos)

        if args.playlist_info_only:
            output["videos"] = videos
        else:
            output["videos"] = []
            for i, video_info in enumerate(videos, 1):
                if "error" in video_info:
                    output["videos"].append(video_info)
                    continue

                print(f"Processing video {i}/{len(videos)}: {video_info['title']}", file=sys.stderr)
                result = process_video(video_info["video_id"], args.whisper)
                output["videos"].append(result)

    elif video_id:
        output["type"] = "video"
        output["video"] = process_video(video_id, args.whisper)

    else:
        output["error"] = "Could not extract video or playlist ID from URL"

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
