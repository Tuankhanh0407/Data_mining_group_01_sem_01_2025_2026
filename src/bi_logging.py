# Import necessary libraries
import csv
from pathlib import Path
from typing import Dict

def append_metric(log_dir: Path, filename: str, row: Dict) -> None:
    """ 
    Append a metric row to a CSV file, creating headers if needed.
    @param log_dir (Path): Directory to store logs.
    @param filename (str): CSV filename.
    @param row (Dict): Metric data as key-value mapping. 
    """
    path = log_dir / filename
    path.parent.mkdir(parents = True, exist_ok = True)
    write_header = not path.exists()
    with path.open("a", encoding = "utf-8", newline = "") as f:
        writer = csv.DictWriter(f, fieldnames = list(row.keys()))
        if write_header:
            writer.writeheader()
        writer.writerow(row)