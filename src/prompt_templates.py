# Import necessary libraries
from typing import Dict, List

def build_slide_plan(topic: str, intent: str, audience: str) -> List[Dict]:
    """ 
    Create a slide outline for a given topic.
    @param topic (str): Topic of the presentation.
    @param intent (str): Intent (in example, 'giảng dạy').
    @param audience (str): Target audience.
    @return (List[Dict]): List of slide dicts with 'title' and 'bullets'. 
    """
    outline = [
        {"title": f"Giới thiệu về {topic}", "bullets": ["Bối cảnh", "Mục tiêu", "Lợi ích chính", "Phạm vi"]},
        {"title": f"Khái niệm và nền tảng", "bullets": ["Định nghĩa", "Các thành phần", "Ví dụ", "Ứng dụng"]},
        {"title": f"Chiến lược và triển khai", "bullets": ["Quy trình", "Công cụ", "Dữ liệu", "Tiêu chí"]},
        {"title": f"Thách thức và giải pháp", "bullets": ["Khó khăn", "Rủi ro", "Giải pháp", "Kinh nghiệm"]},
        {"title": f"Kết luận và hướng phát triển", "bullets": ["Tổng kết", "Giá trị", "Hạn chế", "Tiềm năng"]}
    ]
    return outline

def build_speaker_notes(slide_title: str, bullets: List[str], rag_chunks: List[str], audience: str) -> str:
    """ 
    Generate natural Vietnamese speaker notes for a slide.
    @param slide_title (str): Title of the slide.
    @param bullets (List[str]): Bullet points for the slide.
    @param rag_chunks (List[str]): RAG retrieved text chunks to ground the notes.
    @param audience (str): Target audience to tailor tone.
    @return (str): Speaker notes paragraph (120 - 180 words approx). 
    """
    base = f"Trong phần '{slide_title}', chúng ta sẽ đi qua các ý chính: " + ", ".join(bullets) + ". "
    grounding = " ".join(rag_chunks[:2]) if rag_chunks else ""
    tone = "ngắn gọn, dễ hiểu" if audience == "sinh viên" else "chuyên nghiệp, súc tích"
    note = (
        f"{base}Dựa trên nội dung truy hồi, phần trình bày sẽ {tone}, nêu bối cảnh, ví dụ minh họa, "
        f"và lý do các ý này quan trọng đối với {audience}. {grounding} "
        f"Hãy chú ý cách các khái niệm liên kết với nhau để tạo nên một bức tranh đầy đủ."
    )
    # Bound length roughly by trimming excess
    words = note.split()
    if len(words) > 180:
        words = words[:180]
    return " ".join(words)