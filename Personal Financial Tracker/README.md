Kode ini adalah aplikasi **Personal Finance Tracker** berbasis terminal. Fungsinya untuk mencatat pemasukan dan pengeluaran, menyimpan data ke **SQLite**, mengekspor data ke **Excel**, dan membuat **grafik bulanan**.

**1. Import library**

```python
import sqlite3
from pathlib import Path
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
```

Fungsinya:

| Library      | Fungsi                             |
| ------------ | ---------------------------------- |
| `sqlite3`    | Mengelola database SQLite          |
| `Path`       | Mengelola path file Excel          |
| `datetime`   | Mengisi tanggal otomatis           |
| `pandas`     | Membaca data dari SQLite dan Excel |
| `matplotlib` | Membuat grafik bulanan             |

**2. Nama database**

```python
DB_NAME = "finance_tracker.db"
```

Program akan membuat atau menggunakan database bernama `finance_tracker.db`.

**3. Input file Excel**

```python
def input_excel_file():
```

Fungsi ini meminta user memasukkan path file Excel.

Contoh:

```text
Personal Financial Tracker\financial.xlsx
```

Bagian ini:

```python
file_input = input(...).strip().strip('"').strip("'")
```

berguna untuk menghapus spasi dan tanda kutip.

Bagian ini:

```python
if excel_path.suffix.lower() != ".xlsx":
```

memastikan file yang dipakai harus berformat `.xlsx`.

**4. Koneksi database**

```python
def connect_db():
    return sqlite3.connect(DB_NAME)
```

Fungsi ini membuka koneksi ke database SQLite.

Jadi setiap kali program ingin membaca atau menulis data, fungsi ini dipakai.

**5. Membuat tabel transaksi**

```python
def create_table():
```

Fungsi ini membuat tabel bernama `transactions`.

Struktur tabelnya:

| Kolom         | Tipe    | Fungsi                          |
| ------------- | ------- | ------------------------------- |
| `id`          | INTEGER | ID otomatis                     |
| `date`        | TEXT    | Tanggal transaksi               |
| `type`        | TEXT    | Jenis transaksi: income/expense |
| `category`    | TEXT    | Kategori transaksi              |
| `amount`      | REAL    | Nominal uang                    |
| `description` | TEXT    | Keterangan transaksi            |

Kode SQL-nya:

```sql
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    type TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    description TEXT
)
```

`IF NOT EXISTS` artinya tabel hanya dibuat jika belum ada.

**6. Menyimpan data SQLite ke Excel**

```python
def save_to_excel(excel_path):
```

Fungsi ini mengambil seluruh data dari database:

```python
df = pd.read_sql_query("""
    SELECT * FROM transactions
    ORDER BY date DESC
""", conn)
```

Lalu menyimpannya ke Excel:

```python
df.to_excel(excel_path, index=False)
```

Jadi ketika ada transaksi baru, data di SQLite bisa disalin ke file Excel.

**7. Mengambil data dari Excel ke SQLite**

```python
def import_from_excel(excel_path):
```

Fungsi ini membaca file Excel jika file-nya sudah ada.

```python
df = pd.read_excel(excel_path)
```

Lalu dicek apakah kolom wajib tersedia:

```python
required_columns = ["date", "type", "category", "amount", "description"]
```

Artinya Excel harus punya kolom:

| date | type | category | amount | description |
| ---- | ---- | -------- | -----: | ----------- |

Jika salah satu tidak ada, program menampilkan pesan error.

Setelah itu, setiap baris Excel dimasukkan ke database SQLite:

```python
INSERT INTO transactions (date, type, category, amount, description)
VALUES (?, ?, ?, ?, ?)
```

Tanda `?` digunakan agar data dimasukkan lebih aman dan rapi.

**8. Menambah transaksi baru**

```python
def add_transaction(excel_path):
```

Fungsi ini meminta input dari user:

```text
Tanggal
Tipe
Kategori
Jumlah uang
Deskripsi
```

Jika tanggal dikosongkan:

```python
date_input = datetime.now().strftime("%Y-%m-%d")
```

maka otomatis memakai tanggal hari ini.

Bagian ini mengecek tipe transaksi:

```python
if transaction_type not in ["income", "expense"]:
```

Jadi user hanya boleh mengisi:

```text
income
```

atau:

```text
expense
```

Bagian ini mencegah error kalau nominal bukan angka:

```python
try:
    amount = float(input("Jumlah uang: "))
except ValueError:
    print("Jumlah uang harus berupa angka.")
    return
```

Setelah valid, transaksi dimasukkan ke SQLite, lalu langsung disimpan ke Excel:

```python
save_to_excel(excel_path)
```

**9. Menampilkan transaksi**

```python
def show_transactions():
```

Fungsi ini membaca data dari SQLite dan menampilkannya di terminal.

Query-nya:

```sql
SELECT * FROM transactions
ORDER BY date DESC
```

Artinya transaksi terbaru ditampilkan paling atas.

**10. Membuat grafik bulanan**

```python
def monthly_chart():
```

Fungsi ini membaca seluruh transaksi, lalu mengubah kolom `date` menjadi format tanggal:

```python
df["date"] = pd.to_datetime(df["date"])
```

Kemudian mengambil bulan:

```python
df["month"] = df["date"].dt.to_period("M").astype(str)
```

Contoh:

```text
2026-01-15
```

menjadi:

```text
2026-01
```

Lalu data dikelompokkan berdasarkan bulan dan tipe transaksi:

```python
monthly_summary = df.groupby(["month", "type"])["amount"].sum().unstack(fill_value=0)
```

Hasilnya kira-kira seperti:

| month   | expense |  income |
| ------- | ------: | ------: |
| 2026-01 |  870000 | 5250000 |
| 2026-02 |  745000 | 5750000 |
| 2026-03 | 1190000 | 5800000 |

Lalu dibuat grafik batang:

```python
monthly_summary.plot(kind="bar")
```

**11. Ringkasan keuangan**

```python
def show_summary():
```

Fungsi ini menghitung:

```python
total_income = df[df["type"] == "income"]["amount"].sum()
total_expense = df[df["type"] == "expense"]["amount"].sum()
balance = total_income - total_expense
```

Artinya:

```text
Saldo akhir = total pemasukan - total pengeluaran
```

Output-nya:

```text
Total Pemasukan   : Rp5,000,000
Total Pengeluaran : Rp1,000,000
Saldo Akhir       : Rp4,000,000
```

**12. Menu utama**

```python
def menu():
```

Fungsi ini menjalankan program secara keseluruhan.

Pertama membuat tabel:

```python
create_table()
```

Lalu meminta file Excel:

```python
excel_path = input_excel_file()
```

Kemudian membaca data Excel ke SQLite:

```python
import_from_excel(excel_path)
```

Setelah itu program menampilkan menu berulang:

```text
1. Tambah Transaksi
2. Lihat Transaksi
3. Ringkasan Keuangan
4. Simpan ke Excel
5. Grafik Bulanan
6. Keluar
```

Loop ini berjalan terus sampai user memilih:

```text
6
```

**13. Menjalankan program**

```python
if __name__ == "__main__":
    menu()
```

Bagian ini memastikan fungsi `menu()` hanya berjalan saat file Python dijalankan langsung.

Misalnya:

```bash
python main.py
```

**Kesimpulan alur program**

```text
User menjalankan program
        ↓
Input path Excel
        ↓
Program membuat tabel SQLite
        ↓
Jika Excel ada, data diimport ke SQLite
        ↓
User memilih menu
        ↓
Tambah / lihat / ringkasan / export / grafik
        ↓
Data tersimpan di SQLite dan bisa disimpan ke Excel
```

Catatan penting: kode ini masih punya potensi data dobel. Setiap program dijalankan, data dari Excel akan dimasukkan lagi ke SQLite. Solusi lanjutannya adalah menghapus data lama sebelum import, atau memakai sistem pengecekan duplikat.
