from pathlib import Path
import shutil

# Folder yang ingin dirapikan
folder_input = input("Masukkan path folder yang ingin dirapikan: ").strip('"')
TARGET_FOLDER = Path(folder_input)

# Kategori ekstensi file
FILE_TYPES = {
    "PDF": [".pdf"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Music": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".7z"],
    "Programs": [".exe", ".msi"],
    "Python": [".py"],
}


def get_folder_name(extension):
    for folder_name, extensions in FILE_TYPES.items():
        if extension.lower() in extensions:
            return folder_name
    return "Others"


def organize_files():
    if not TARGET_FOLDER.exists():
        print("Folder tidak ditemukan.")
        return

    for file_path in TARGET_FOLDER.iterdir():
        if file_path.is_file():
            extension = file_path.suffix
            folder_name = get_folder_name(extension)

            destination_folder = TARGET_FOLDER / folder_name
            destination_folder.mkdir(exist_ok=True)

            destination_path = destination_folder / file_path.name

            # Jika nama file sudah ada, tambahkan angka
            counter = 1
            while destination_path.exists():
                new_name = f"{file_path.stem}_{counter}{file_path.suffix}"
                destination_path = destination_folder / new_name
                counter += 1

            shutil.move(str(file_path), str(destination_path))
            print(f"Memindahkan: {file_path.name} -> {folder_name}")


organize_files()