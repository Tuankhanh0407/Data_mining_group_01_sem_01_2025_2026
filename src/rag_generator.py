# Import necessary libraries
from embedding_index import EmbeddingIndex
from prompt_templates import build_slide_plan, build_speaker_notes
from typing import Dict, List

def generate_slides_with_notes(index: EmbeddingIndex, topic: str, intent: str, audience: str, n_slides: int = 8) -> List[Dict]:
    """ 
    Generate slides and speaker notes grounded by RAG.
    @param index (EmbeddingIndex): Built embedding index for retrieval.
    @param topic (str): Topic for the presentation.
    @param intent (str): Intent (in example, 'giảng dạy').
    @param audience (str): Target audience.
    @param n_slides (int): Number of slides to generate.
    @return (List[Dict]): List of slides with 'title', 'bullets', 'notes'. 
    """
    query = f"{topic} {intent} {audience}"
    results = index.search(query = query, top_k = 10)
    rag_chunks = [r["chunk"] for r in results]
    outline = build_slide_plan(topic = topic, intent = intent, audience = audience)
    # Extend outline to 'n_slides' by repeating thematic pattern
    while len(outline) < n_slides:
        outline.append({"title": f"Ví dụ thực tế về {topic}", "bullets": ["Bài học", "Kết quả", "Tác động", "Khuyến nghị"]})
    slides: List[Dict] = []
    for item in outline[:n_slides]:
        notes = build_speaker_notes(slide_title = item["title"], bullets = item["bullets"], rag_chunks = rag_chunks, audience = audience)
        slides.append({"title": item["title"], "bullets": item["bullets"], "notes": notes})
    return slides