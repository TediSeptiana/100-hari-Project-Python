Kode ini adalah program otomatisasi pengelolaan file yang akan memindahkan file ke folder berdasarkan ekstensi file-nya. Misalnya file PDF akan masuk ke folder `PDF`, gambar ke folder `Images`, dan seterusnya.

**1. Import library**

```python
from pathlib import Path
import shutil
```

* `Path` digunakan untuk mengelola path/folder dengan cara yang lebih modern dibanding `os.path`.
* `shutil` digunakan untuk memindahkan file (`move`).

**2. Meminta input folder**

```python
folder_input = input("Masukkan path folder yang ingin dirapikan: ").strip('"')
TARGET_FOLDER = Path(folder_input)
```

Contoh input:

```text
C:\Users\ASUS\Downloads
```

atau

```text
"C:\Users\ASUS\Downloads"
```

Fungsi `.strip('"')` menghapus tanda kutip di awal dan akhir jika ada.

Kemudian:

```python
TARGET_FOLDER = Path(folder_input)
```

mengubah string menjadi objek Path.



**3. Daftar kategori file**

```python
FILE_TYPES = {
    "PDF": [".pdf"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    ...
}
```

Dictionary ini berfungsi sebagai aturan.

Misalnya:

```python
".pdf" -> PDF
".jpg" -> Images
".mp4" -> Videos
```

Jika ada file:

```text
laporan.pdf
```

maka akan dipindahkan ke:

```text
PDF/laporan.pdf
```



**4. Menentukan folder tujuan**

```python
def get_folder_name(extension):
```

Fungsi ini menerima ekstensi file.

Contoh:

```python
get_folder_name(".pdf")
```

Proses:

```python
for folder_name, extensions in FILE_TYPES.items():
```

Loop seluruh kategori.

Contoh iterasi pertama:

```python
folder_name = "PDF"
extensions = [".pdf"]
```

Lalu dicek:

```python
if extension.lower() in extensions:
```

Jika cocok:

```python
return folder_name
```

Maka hasilnya:

```python
"PDF"
```

Jika tidak ditemukan:

```python
return "Others"
```

Contoh:

```python
file.xyz
```

akan masuk ke folder:

```text
Others
```



**5. Fungsi utama**

```python
def organize_files():
```

Fungsi ini melakukan seluruh proses perapihan.



### Cek folder ada atau tidak

```python
if not TARGET_FOLDER.exists():
    print("Folder tidak ditemukan.")
    return
```

Misalnya user memasukkan:

```text
C:\FolderSalah
```

Karena tidak ada:

```python
return
```

Program berhenti.



### Membaca isi folder

```python
for file_path in TARGET_FOLDER.iterdir():
```

Contoh isi Downloads:

```text
laporan.pdf
foto.jpg
musik.mp3
folder_lama/
```

Loop akan membaca semuanya satu per satu.



### Hanya proses file

```python
if file_path.is_file():
```

Jika item adalah folder:

```text
folder_lama/
```

maka dilewati.

Yang diproses hanya:

```text
laporan.pdf
foto.jpg
musik.mp3
```



### Ambil ekstensi file

```python
extension = file_path.suffix
```

Contoh:

```python
laporan.pdf
```

hasil:

```python
".pdf"
```



### Tentukan folder tujuan

```python
folder_name = get_folder_name(extension)
```

Misalnya:

```python
".pdf"
```

hasil:

```python
"PDF"
```



### Membuat folder tujuan

```python
destination_folder = TARGET_FOLDER / folder_name
```

Misalnya:

```python
C:\Users\ASUS\Downloads\PDF
```

Kemudian:

```python
destination_folder.mkdir(exist_ok=True)
```

Jika folder belum ada:

```text
PDF/
```

dibuat otomatis.

Jika sudah ada:

```python
exist_ok=True
```

mencegah error.



### Menentukan lokasi file baru

```python
destination_path = destination_folder / file_path.name
```

Contoh:

```python
laporan.pdf
```

menjadi:

```text
C:\Users\ASUS\Downloads\PDF\laporan.pdf
```



### Mengatasi nama file yang sama

Misalnya sudah ada:

```text
PDF/laporan.pdf
```

dan ada file lain bernama:

```text
laporan.pdf
```

Maka bagian ini bekerja:

```python
counter = 1

while destination_path.exists():
```

Selama file tujuan sudah ada:

```python
new_name = f"{file_path.stem}_{counter}{file_path.suffix}"
```

Hasil:

```text
laporan_1.pdf
```

Kalau masih ada:

```text
laporan_2.pdf
```

dan seterusnya.

Ini mencegah file lama tertimpa.



### Memindahkan file

```python
shutil.move(str(file_path), str(destination_path))
```

Contoh:

Dari:

```text
Downloads/laporan.pdf
```

Ke:

```text
Downloads/PDF/laporan.pdf
```



### Menampilkan log

```python
print(f"Memindahkan: {file_path.name} -> {folder_name}")
```

Contoh output:

```text
Memindahkan: laporan.pdf -> PDF
Memindahkan: foto.jpg -> Images
Memindahkan: musik.mp3 -> Music
```



**7. Menjalankan program**

```python
organize_files()
```

Baris ini memanggil fungsi utama sehingga seluruh proses dimulai.

**Contoh sebelum dijalankan**

```text
Downloads/
├── laporan.pdf
├── foto.jpg
├── video.mp4
├── script.py
```

**Setelah dijalankan**

```text
Downloads/
├── PDF/
│   └── laporan.pdf
├── Images/
│   └── foto.jpg
├── Videos/
│   └── video.mp4
├── Python/
│   └── script.py
```
