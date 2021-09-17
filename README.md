# playwright-checkpoint-runner

automation script with Playwright and `httpx` that run multi-step browser + API workflow and save checkpoint after every step.

## features
- saves progress to `checkpoint.json` so if it crash halfway, next run resume from where it stopped
- takes screenshot + HTML snapshot inside `failure_artifacts/` when a step fail
- writes timing metrics to `metrics.json`

## usage
```bash
pip install -r requirements.txt
