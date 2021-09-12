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


def run_workflow(target_url: str, api_check_url: str, reset: bool = False) -> None:
    if reset and CHECKPOINT_FILE.exists():
        CHECKPOINT_FILE.unlink()

    state = load_checkpoint(CHECKPOINT_FILE)
    metrics: List[Dict[str, Any]] = []
    ARTIFACT_DIR.mkdir(exist_ok=True)

    steps = ["api_preflight", "open_page", "extract_heading", "verify_content"]

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        for step_name in steps:
            if step_name in state["completed_steps"]:
                print("[SKIP] already done:", step_name)
                continue

            t0 = time.time()
            try:
                if step_name == "api_preflight":
                    resp = httpx.get(api_check_url, timeout=5.0)
                    state["context"]["api_status"] = resp.status_code
                elif step_name == "open_page":
                    page.goto(target_url, wait_until="domcontentloaded", timeout=10000)
                    state["context"]["page_title"] = page.title()
                elif step_name == "extract_heading":
                    h1 = page.locator("h1").first
                    h1.wait_for(state="visible", timeout=5000)
                    state["context"]["h1"] = h1.inner_text()
                elif step_name == "verify_content":
                    body_len = len(page.inner_text("body"))
                    if body_len == 0:
                        raise RuntimeError("page body is empty")
                    state["context"]["body_len"] = body_len

