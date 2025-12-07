# Import necessary libraries
from dataclasses import dataclass
from pathlib import Path

@dataclass
class AppConfig:
    """ 
    Configuration holder for paths and runtime flags.

    Attributes:
    - data_dir (Path): Directory to store datasets.
    - outputs_dir (Path): Directory to store generated outputs (pptx, audio, logs).
    - logs_dir (Path): Directory to store pipeline logs.
    - min_samples (int): Minimum number of samples required in the dataset.
    - language (str): Language code for processing and text-to-speech.
    - presentation_title (str): Default presentation title.
    """
    data_dir: Path = Path("data")
    outputs_dir: Path = Path("outputs")
    logs_dir: Path = outputs_dir / "logs"
    min_samples: int = 100
    language: str = "vi"
    presentation_title: str = "Tự động tạo bài thuyết trình tiếng Việt"

    def ensure_dirs(self) -> None:
        """ 
        Ensure required directories exist.
        """
        self.data_dir.mkdir(parents = True, exist_ok = True)
        self.outputs_dir.mkdir(parents = True, exist_ok = True)
        (self.outputs_dir / "audio").mkdir(parents = True, exist_ok = True)
        self.logs_dir.mkdir(parents = True, exist_ok = True)