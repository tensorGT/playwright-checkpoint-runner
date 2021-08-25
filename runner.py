import argparse
import json
import time
from pathlib import Path
from typing import Any, Dict, List

import httpx
from playwright.sync_api import sync_playwright

CHECKPOINT_FILE = Path("checkpoint.json")
METRICS_FILE = Path("metrics.json")
ARTIFACT_DIR = Path("failure_artifacts")


def load_checkpoint(path: Path) -> Dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"completed_steps": [], "context": {}}


def save_checkpoint(path: Path, state: Dict[str, Any]) -> None:
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")


def save_metrics(path: Path, metrics: List[Dict[str, Any]]) -> None:
    path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")


