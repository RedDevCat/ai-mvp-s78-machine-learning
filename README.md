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

## Other:
Here are the **step-by-step commands** to process each dataset, train or retrain your model based on the processed data, and general notes for running your project smoothly:

***

### Step 1: Activate your Python environment (if not already active)

```bash
source .venv/bin/activate   # On Linux/macOS
# OR
.venv\Scripts\activate      # On Windows
```

***

### Step 2: Preprocess each dataset CSV folder

Run this command for each dataset folder under `datasets/` (e.g., `devign`, `BADS`, `kaggle_student_code`, `linevul`, `vulfix`):

```bash
python -c "from utils.train_process import preprocess_all_csvs_in_folder; preprocess_all_csvs_in_folder('datasets/dataset_folder_name', out_csv='datasets/processed/dataset_folder_name_train.csv')"
```

For your datasets tree:

```bash
python -c "from utils.train_process import preprocess_all_csvs_in_folder; preprocess_all_csvs_in_folder('datasets/BADS', out_csv='datasets/processed/BADS_train.csv')"

python -c "from utils.train_process import preprocess_all_csvs_in_folder; preprocess_all_csvs_in_folder('datasets/devign', out_csv='datasets/processed/devign_train.csv')"

python -c "from utils.train_process import preprocess_all_csvs_in_folder; preprocess_all_csvs_in_folder('datasets/kaggle_student_code', out_csv='datasets/processed/kaggle_student_code_train.csv')"

python -c "from utils.train_process import preprocess_all_csvs_in_folder; preprocess_all_csvs_in_folder('datasets/linevul', out_csv='datasets/processed/linevul_train.csv')"

python -c "from utils.train_process import preprocess_all_csvs_in_folder; preprocess_all_csvs_in_folder('datasets/vulfix', out_csv='datasets/processed/vulfix_train.csv')"
```

You can repeat these whenever you add or update raw CSVs for that dataset.

***

### Step 3: Train or retrain your LightGBM model on a chosen processed CSV

For example, to train on the `devign` dataset processed CSV:

```bash
python utils/train_model.py datasets/processed/devign_train.csv
```

Do the same for any other processed dataset CSV you want to use.

***

### Step 4: Use your app normally

Run your Streamlit app. It will **load the latest trained model from** `models/risk_model.txt` and apply risk scoring during file scans.

```bash
streamlit run app.py
```

***

### Notes:

- You run the preprocessing **only once after adding/updating datasets** to generate ML-ready CSVs.
- You train or retrain **every time your processed data changes** to update the model.
- You **do NOT need to rerun preprocessing or retrain the model every time** you launch or use the app—only when your underlying training data changes.
- Store all processed CSVs under `datasets/processed/` to keep things organized.

***

This sequence ensures your ML risk model stays up to date with your datasets, and your app always uses the latest model for analysis.

If you want, I can help you automate batching all dataset preprocessing and training in one script or recommend best practices for versioning and retraining.

