# BTL-Deep-Learning

Binary classifier for real vs. fake face images using a frozen CLIP ViT-L/14 backbone with a lightweight linear head. Training and evaluation are driven from the notebook notebooks/train-real-vs-fake-face-classifier.ipynb.

## Data
- Real: CelebA subset under data/processed/sample_1pct/celeba/ (label 0)
- Fake: three sources under data/processed/sample_1pct/ — fairfacegen/, person_face_dataset/, stable_diffusion_faces/ (label 1)
- Allowed extensions: .jpg, .jpeg, .png, .webp, .bmp

## Environment
- Python 3.10+ recommended, GPU strongly suggested
- Install deps: `pip install -r requirements.txt`
- Kaggle access: place kaggle.json in project root or your Kaggle config dir to run download notebooks

## Training (Notebook)
Open notebooks/train-real-vs-fake-face-classifier.ipynb and run top-to-bottom:
- Paths: adjust DATA_ROOT and MODEL_SAVE_PATH (defaults target Kaggle /kaggle/input/... and /kaggle/working/; set to local data/processed/sample_1pct if training locally)
- Model: CLIP ViT-L/14 frozen encoder + 3-layer MLP head with sigmoid
- Augmentation: resize→random crop 224, flip, rotation 15°, color jitter, Gaussian blur; val/test use center crop
- Splits: per-source train/val/test, then merged and shuffled
- Training: BCELoss, Adam (lr 1e-3), ReduceLROnPlateau, batch size 32, early stopping patience 5
- Outputs: best_model.pth and final_model.pth stored at MODEL_SAVE_PATH; history and metrics saved with checkpoints

## Evaluation & Visualization
- Validation/test metrics logged each epoch; test evaluation runs after loading best_model.pth
- Section “Visualize Predictions” in the notebook plots sample predictions with confidence
- Section “Plot Training History” renders loss/accuracy curves and prints best val acc and final test acc

## Development Notes
- Keep folder layout intact (src/, data/, models/, notebooks/, configs/)
- Use feature branches and run notebook or unit checks before merging
