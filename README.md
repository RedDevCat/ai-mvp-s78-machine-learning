### debian:
sudo apt-get update
sudo apt-get install -y \
  build-essential \
  libfuzzy-dev \
  libmagic-dev \
  libffi-dev \
  python3-dev \
  gcc \
  g++ \
  libssl-dev \
  pkg-config \
  file \
  libreadline-dev \
  libsqlite3-dev

### pacman:
sudo pacman -Sy
sudo pacman -S --needed base-devel gcc gcc-libs ssdeep libmagic python python-pip file

### How to Use and Train Your ML Module
Get or download datasets (like SARD, Kaggle student code, OWASP vulnerable apps) and save under datasets/.

Label your data with a Python label function, for example:

python
def label_func(text, path):
    # Example: simplistic labeling by presence of secrets or suspicious keywords
    if "AWS" in text or "eval(" in text:
        return 1.0  # unsafe
    return 0.0  # safe
Preprocess to CSV for training:

bash
python -c "from utils.train_process import preprocess_dataset; preprocess_dataset('datasets/sard/raw', label_func, 'datasets/processed/sard.csv')"
Train LightGBM model from CSV:

bash
python utils/train_model.py datasets/processed/sard.csv
Start the app and upload files—model will predict risk scores live and output policy flags.

