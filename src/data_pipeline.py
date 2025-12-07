# Import necessary libraries
import json
from pathlib import Path
import requests
from typing import List
from utils import normalize_vi_text, set_seed

class DatasetRecord:
    """ 
    Represent a single dataset sample for the presentation generator.

    Attributes:
    - topic (str): The topic of the content (in example, 'Chuyển đổi số').
    - intent (str): The intent (in example, 'giảng dạy', 'bán hàng').
    - audience (str): Target audience (in example, 'sinh viên', 'quản lý').
    - text (str): Raw Vietnamese text content.
    - chunks (List[str]): Chunked segments for RAG retrieval.
    """

    def __init__(self, topic: str, intent: str, audience: str, text: str, chunks: List[str]) -> None:
        self.topic = topic
        self.intent = intent
        self.audience = audience
        self.text = text
        self.chunks = chunks

def chunk_text(text: str, max_len: int = 400) -> List[str]:
    """ 
    Split text into chunks with approximate maximum length.
    @param text (str): Input text to split.
    @param max_len (int): Maximum characters per chunk.
    @return (List[str]): List of text chunks. 
    """
    sentences = text.split(". ")
    chunks: List[str] = []
    current = ""
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        if len(current) + len(s) + 1 <= max_len:
            current = (current + " " + s).strip()
        else:
            if current:
                chunks.append(normalize_vi_text(current + "."))
            current = s
    if current:
        chunks.append(normalize_vi_text(current + "."))
    return chunks

def synthesize_samples(n: int = 120) -> List[DatasetRecord]:
    """ 
    Create synthetic Vietnamese samples across multiple topics, intents, and audiences.
    @param n (int): Number of samples to synthesize.
    @return (List[DatasetRecord]): Generated dataset records. 
    """
    set_seed(42)
    topics = ["Chuyển đổi số", "Khởi nghiệp", "AI trong giáo dục", "Marketing số", "Thương mại điện tử", "Phân tích dữ liệu"]
    intents = ["giảng dạy", "thuyết minh", "bán hàng"]
    audiences = ["sinh viên", "quản lý", "công chúng"]
    records: List[DatasetRecord] = []
    for i in range(n):
        topic = topics[i % len(topics)]
        intent = intents[i % len(intents)]
        audience = audiences[i % len(audiences)]
        text = (
            f"{topic} tại Việt Nam đang phát triển mạnh mẽ. "
            f"Đối với {audience}, việc hiểu đúng khái niệm và ứng dụng là rất quan trọng. "
            f"Mục tiêu của nội dung này là {intent} và làm rõ các lợi ích, thách thức, cùng ví dụ thực tế. "
            f"Chúng ta sẽ xem xét chiến lược, công cụ, dữ liệu, và cách đánh giá hiệu quả."
        )
        chunks = chunk_text(text, max_len = 350)
        records.append(DatasetRecord(topic, intent, audience, text, chunks))
    return records

def download_uits_vienews(limit: int = 150) -> List[DatasetRecord]:
    """ 
    Attempt to download UIT ViNews dataset via Hugging Face API (public). Fallback if not available.
    @param limit (int): Max number of samples to fetch.
    @return (List[DatasetRecord]): Parsed dataset records. 
    """
    url = "https://datasets-server.huggingface.co/rows?dataset=uitnlp%2Fuit-vienews&config=default&split=train&offset=0&length=200"
    records: List[DatasetRecord] = []
    try:
        resp = requests.get(url, timeout = 30)
        resp.raise_for_status()
        data = resp.json()
        rows = data.get("rows", [])[:limit]
        for r in rows:
            obj = r.get("row", {})
            text = obj.get("text", "")
            text = normalize_vi_text(text)
            # Heuristics for topic/intent/audience
            topic = "Tin tức tổng hợp"
            intent = "thuyết minh"
            audience = "công chúng"
            chunks = chunk_text(text, max_len = 400)
            if chunks:
                records.append(DatasetRecord(topic, intent, audience, text, chunks))
    except Exception:
        # Return empty to signal fallback
        return []
    return records

def build_dataset(data_dir: Path, min_samples: int = 100) -> Path:
    """ 
    Build or download the dataset and persist as JSONL.
    @param data_dir (Path): Directory to store dataset file.
    @param min_samples (int): Minimum required samples.
    @return (Path): Path to the JSONL dataset file.
    """
    out_path = data_dir / "viet_presentation_dataset.jsonl"
    records = download_uits_vienews(limit = max(min_samples, 150))
    if len(records) < min_samples:
        synth = synthesize_samples(n = max(min_samples, 120))
        records = synth
    with out_path.open("w", encoding = "utf-8") as f:
        for rec in records:
            f.write(json.dumps({
                "topic": rec.topic,
                "intent": rec.intent,
                "audience": rec.audience,
                "text": rec.text,
                "chunks": rec.chunks
            }, ensure_ascii = False) + "\n")
    return out_path