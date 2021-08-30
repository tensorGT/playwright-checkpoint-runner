# playwright-checkpoint-runner

automation script with Playwright and `httpx` that run multi-step browser + API workflow and save checkpoint after every step.

## features
- saves progress to `checkpoint.json` so if it crash halfway, next run resume from where it stopped
