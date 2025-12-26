# Real vs Fake Face API - Quickstart

This guide shows two ways to run the FastAPI service that serves predictions from `models/best_model.pth`.

## 1) Run with Docker

Prereqs: Docker installed.

Build and start:

```bash
# From repo root
docker compose up --build
```

Then call the API:

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your_image.jpg"
```

Stop:

```bash
docker compose down
```

Notes:
- Port `8000` is exposed by default.
- The `models/` folder is mounted read-only into the container so updates to `best_model.pth` are picked up without rebuild.
- The image uses CPU wheels for torch/torchvision. For GPU builds, adjust the Dockerfile (base image + torch index URL).

## 2) Run locally with Uvicorn

Prereqs: Python 3.10+, a working torch install matching your platform (CPU or CUDA), and the model at `models/best_model.pth`.

Install dependencies (CPU example):

```bash
pip install --upgrade pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
pip install git+https://github.com/openai/CLIP.git
```

Start the server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Predict request example (same as above):

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your_image.jpg"
```

Troubleshooting:
- If CLIP fails to import, reinstall with `pip install git+https://github.com/openai/CLIP.git`.
- If torch/torchvision fail to install, use the wheel index URL that matches your CUDA version from https://download.pytorch.org/whl/torch_stable.html.
