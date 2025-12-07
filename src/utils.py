# Import necessary libraries
import json
from pathlib import Path
import random
import re
import string
from typing import Dict
from unidecode import unidecode

def set_seed(seed: int = 42) -> None:
    """ 
    Set deterministic random seed for reproducibility.
    @param seed (int): Seed value for randomness control. 
    """
    random.seed(seed)

def safe_write_json(path: Path, obj: Dict) -> None:
    """ 
    Safely write a JSON object to a file.
    @param path (Path): Target file path.
    @param obj (Dict): JSON-serializable object to store. 
    """
    path.parent.mkdir(parents = True, exist_ok = True)
    with path.open("w", encoding = "utf-8") as f:
        json.dump(obj, f, ensure_ascii = False, indent = 2)

def safe_write_text(path: Path, text: str) -> None:
    """ 
    Safely write plain text to a file.
    @param path (Path): Target file path.
    @param text (str): Text content to store. 
    """
    path.parent.mkdir(parents = True, exist_ok = True)
    with path.open("w", encoding = "utf-8") as f:
        f.write(text)

def normalize_vi_text(text: str) -> str:
    """ 
    Normalize Vietnamese text for text-to-speech and presentation.
    @param text (str): Input Vietnamese text.
    @return (str): Cleaned and normalized text. 
    """
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    # Keep Vietnamese accents but normalize punctuation spacing
    text = text.replace(" ,", ",").replace(" .", ".").replace(" :", ":").replace(" ;", ";")
    return text

def slugify(text: str, max_len: int = 60) -> str:
    """ 
    Create filesystem-safe from a title.
    @param text (str): Title or arbitrary string.
    @param max_len (int): Maximu length for slug.
    @return (str): Safe slug string.
    """
    text_ascii = unidecode(text).lower()
    text_ascii = re.sub(r"[^a-z0-9]+", "-", text_ascii).strip("-")
    return text_ascii[:max_len]

def random_title_suffix(n: int = 6) -> str:
    """ 
    Generate a random suffix for filenames.
    @param n (int): Number of random characters.
    @return (str): Random alphanumeric suffix. 
    """
    return "".join(random.choices(string.ascii_lowercase + string.digits, k = n))