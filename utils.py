from pathlib import Path

IMAGE_DIR = Path("data/images")

def save_uploaded_image(uploaded_file):
    if uploaded_file is None:
        return None

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    file_path = IMAGE_DIR / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return str(file_path)