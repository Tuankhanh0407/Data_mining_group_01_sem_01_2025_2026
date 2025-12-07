# Import necessary libraries
from gtts import gTTS
from pathlib import Path
from typing import Dict, List
from utils import normalize_vi_text

def synthesize_slide_audio(slides: List[Dict], out_dir: Path, language: str = "vi") -> None:
    """ 
    Create MP3 audio files for each slide's speaker notes.
    @param slides (List[Dict]): Slides with 'notes' key.
    @param out_dir (Path): Directory to store audio files.
    @param language (str): Language code for TTS. 
    """
    out_dir.mkdir(parents = True, exist_ok = True)
    for i, s in enumerate(slides, start = 1):
        text = normalize_vi_text(s["notes"])
        tts = gTTS(text = text, lang = language, slow = False)
        mp3_path = out_dir / f"slide_{i}.mp3"
        tts.save(str(mp3_path))