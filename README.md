# BTL-Deep-Learning

A deep learning project focused on face detection and image processing using the CelebA dataset.

## What I've Done

### 📁 Project Structure Setup
- Created a well-organized project structure with separate folders for:
  - `src/`: Source code modules
  - `data/`: Dataset storage (raw, processed, augmented)
  - `models/`: Model checkpoints and saved models
  - `notebooks/`: Jupyter notebooks for experimentation
  - `configs/`: Configuration files and logging setup

### 📊 Dataset Integration
- Implemented Kaggle API integration for dataset downloading
- Created `download_from_kaggle.py` module for easy dataset management
- Successfully downloaded CelebA dataset (Celebrity Faces Attributes Dataset)
- Set up data pipeline in `notebooks/download_data.ipynb`

### 🚀 Quick Start

1. **Setup Environment**:
   ```bash
   pip install -r requirements.txt
   # Or use conda, uv, env...
   ```

2. **Configure Kaggle API**:
   - Download `kaggle.json` from your Kaggle account
   - Place it in the project root or Kaggle config directory
   - See: https://www.kaggle.com/discussions/general/74235

3. **Download Dataset**:
   - Open `notebooks/download_data.ipynb`
   - Run the cells to download CelebA dataset to `data/raw/celeba/`

### 📋 Development Guidelines
- Use separate branches for new features
- Follow the established folder structure
- Test changes before merging to main branch

## Next Steps
- Model training and evaluation
- Face detection implementation
- Web interface development
