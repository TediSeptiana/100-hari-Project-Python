import sqlite3
from pathlib import Path
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt


DB_NAME = "finance_tracker.db"


def input_excel_file():
    file_input = input("Masukkan path file Excel untuk tracking: ").strip().strip('"').strip("'")
    excel_path = Path(file_input)

    if excel_path.suffix.lower() != ".xlsx":
        print("File harus berformat .xlsx")
        return None

    return excel_path


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_to_excel(excel_path):
    conn = connect_db()

    df = pd.read_sql_query("""
        SELECT * FROM transactions
        ORDER BY date DESC
    """, conn)

    conn.close()

    if df.empty:
        print("Belum ada data untuk disimpan ke Excel.")
        return

    df.to_excel(excel_path, index=False)
    print(f"Data berhasil disimpan ke Excel: {excel_path}")


def import_from_excel(excel_path):
    if not excel_path.exists():
        print("File Excel belum ada. Data baru akan dibuat setelah transaksi ditambahkan.")
        return

    df = pd.read_excel(excel_path)

    required_columns = ["date", "type", "category", "amount", "description"]

    for column in required_columns:
        if column not in df.columns:
            print(f"Kolom '{column}' tidak ditemukan di file Excel.")
            return

    conn = connect_db()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO transactions (date, type, category, amount, description)
            VALUES (?, ?, ?, ?, ?)
        """, (
            str(row["date"])[:10],
            row["type"],
            row["category"],
            float(row["amount"]),
            row["description"]
        ))

    conn.commit()
    conn.close()

    print("Data dari Excel berhasil dimasukkan ke SQLite.")


def add_transaction(excel_path):
    print("\n=== Tambah Transaksi ===")

    date_input = input("Tanggal (YYYY-MM-DD), kosongkan untuk hari ini: ")

    if date_input.strip() == "":
        date_input = datetime.now().strftime("%Y-%m-%d")

    transaction_type = input("Tipe (income/expense): ").lower()

    if transaction_type not in ["income", "expense"]:
        print("Tipe harus income atau expense.")
        return

    category = input("Kategori: ")

    try:
        amount = float(input("Jumlah uang: "))
    except ValueError:
        print("Jumlah uang harus berupa angka.")
        return

    description = input("Deskripsi: ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (date, type, category, amount, description)
        VALUES (?, ?, ?, ?, ?)
    """, (date_input, transaction_type, category, amount, description))

    conn.commit()
    conn.close()

    save_to_excel(excel_path)

    print("Transaksi berhasil ditambahkan.")


def show_transactions():
    conn = connect_db()

    df = pd.read_sql_query("""
        SELECT * FROM transactions
        ORDER BY date DESC
    """, conn)

    conn.close()

    if df.empty:
        print("Belum ada data transaksi.")
    else:
        print("\n=== Daftar Transaksi ===")
        print(df)


def monthly_chart():
    conn = connect_db()

    df = pd.read_sql_query("SELECT * FROM transactions", conn)

    conn.close()

    if df.empty:
        print("Belum ada data untuk dibuat grafik.")
        return

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)

    monthly_summary = df.groupby(["month", "type"])["amount"].sum().unstack(fill_value=0)

    monthly_summary.plot(kind="bar")

    plt.title("Grafik Keuangan Bulanan")
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Uang")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def show_summary():
    conn = connect_db()

    df = pd.read_sql_query("SELECT * FROM transactions", conn)

    conn.close()

    if df.empty:
        print("Belum ada data transaksi.")
        return

    total_income = df[df["type"] == "income"]["amount"].sum()
    total_expense = df[df["type"] == "expense"]["amount"].sum()
    balance = total_income - total_expense

    print("\n=== Ringkasan Keuangan ===")
    print(f"Total Pemasukan   : Rp{total_income:,.0f}")
    print(f"Total Pengeluaran : Rp{total_expense:,.0f}")
    print(f"Saldo Akhir       : Rp{balance:,.0f}")


def menu():
    create_table()

    excel_path = input_excel_file()

    if excel_path is None:
        return

    import_from_excel(excel_path)

    while True:
        print("\n=== Personal Finance Tracker ===")
        print("1. Tambah Transaksi")
        print("2. Lihat Transaksi")
        print("3. Ringkasan Keuangan")
        print("4. Simpan ke Excel")
        print("5. Grafik Bulanan")
        print("6. Keluar")

        choice = input("Pilih menu: ")

        if choice == "1":
            add_transaction(excel_path)
        elif choice == "2":
            show_transactions()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            save_to_excel(excel_path)
        elif choice == "5":
            monthly_chart()
        elif choice == "6":
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    menu()