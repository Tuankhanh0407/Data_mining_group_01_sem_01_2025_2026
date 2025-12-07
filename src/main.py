# Import necessary libraries
from bi_logging import append_metric
from config import AppConfig
from data_pipeline import build_dataset
from embedding_index import EmbeddingIndex
from pptx_builder import build_presentation
from rag_generator import generate_slides_with_notes
from time import perf_counter
from tts_service import synthesize_slide_audio

def run_pipeline() -> None:
    """ 
    Execute the end-to-end pipeline to produce a presentation and narration. 
    """
    cfg = AppConfig()
    cfg.ensure_dirs()
    t_0 = perf_counter()
    dataset_path = build_dataset(data_dir = cfg.data_dir, min_samples = cfg.min_samples)
    t_1 = perf_counter()
    index = EmbeddingIndex()
    index.build(dataset_path = dataset_path)
    t_2 = perf_counter()
    topic = "Khai phá dữ liệu"
    intent = "giảng dạy"
    audience = "sinh viên"
    slides = generate_slides_with_notes(index = index, topic = topic, intent = intent, audience = audience, n_slides = 10)
    t_3 = perf_counter()
    pptx_path = cfg.outputs_dir / "presentation_auto_generated.pptx"
    build_presentation(slides = slides, out_path = pptx_path, title = cfg.presentation_title)
    t_4 = perf_counter()
    audio_dir = cfg.outputs_dir / "audio"
    synthesize_slide_audio(slides = slides, out_dir = audio_dir, language = cfg.language)
    t_5 = perf_counter()
    append_metric(cfg.logs_dir, "pipeline_times.csv", {
        "dataset_seconds": round(t_1 - t_0, 3),
        "index_seconds": round(t_2 - t_1, 3),
        "generation_seconds": round(t_3 - t_2, 3),
        "pptx_seconds": round(t_4 - t_3, 3),
        "tts_seconds": round(t_5 - t_4, 3),
        "total_seconds": round(t_5 - t_0, 3)
    })
    append_metric(cfg.logs_dir, "presentation_stats.csv", {
        "topic": topic,
        "intent": intent,
        "audience": audience,
        "slides_count": len(slides),
        "avg_notes_len_words": round(sum(len(s['notes'].split()) for s in slides) / len(slides), 2)
    })
    print(f"Presentation saved to: {pptx_path}")
    print(f"Audio saved to: {audio_dir}")

def main() -> None:
    """ 
    Main function that coordinates the program. 
    """
    run_pipeline()

if __name__ == "__main__":
    main()