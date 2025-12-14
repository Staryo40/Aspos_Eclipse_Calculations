# Tugas Kelompok Astronomi Posisi: Menghitung Gerhana Matahari dan Bulan

Program ini dibuat untuk menghitung dan memvisualisasikan gerhana Matahari dan gerhana Bulan berdasarkan metode Astronomi Posisi, termasuk pencarian gerhana pertama, seluruh gerhana dalam rentang tahun, serta pembuatan laporan dan grafik.

## Requirements
**Wajib:**
- Python **3.9+**

**Library yang digunakan:**
- `math`
- `datetime`
- `os`
- `collections`
- `matplotlib`

Instal `matplotlib` jika belum tersedia:
```bash
pip install matplotlib
```

## Clone Repository
```bash
git clone https://github.com/Staryo40/Aspos_Eclipse_Calculations.git
cd Aspos_Eclipse_Calculations
```

Struktur Proyek
```bash
.
|-- README.md
|-- output/
`-- src/
    |-- eclipse_end.py
    |-- enum_types.py
    |-- intermediate_var.py
    |-- main.py
    |-- models.py
    |-- simple_intermediate_var.py
    `-- utils.py
```

## Cara menjalankan program
Pastikan sudah clone repository sebelumnya

1. Menjalankan program main
    ```bash
    python src/main.py
    ```

2. Pilih opsi yang ingin digunakan (1-10)
    ```bash
    === Pilih Mode ===
    1. Gerhana Matahari Detail
    2. Gerhana Bulan Detail
    3. Gerhana Bulan dan Matahari Detail
    4. Gerhana Matahari Short
    5. Gerhana Bulan Short
    6. Gerhana Bulan dan Matahari Short
    7. Export Gerhana Matahari (Semua dalam rentang tahun)
    8. Export Gerhana Matahari (Gerhana pertama tiap tahun)
    9. Export Gerhana Bulan (Semua dalam rentang tahun)
    10. Export Gerhana Bulan (Gerhana pertama tiap tahun)
    Input mode: 
    ```

3. Input nilai tanggal (contoh: 1997-07-01)
    ```bash
    === Konversi Tanggal ke Year Fraction ===
    Masukkan tanggal dengan format: YYYY-MM-DD
    Contoh: 2022-11-08
    Masukkan tanggal: 
    ```

    Program akan lalu mengeluarkan output sesuai mode yang dipilih di awal

## Contoh Output Program
```bash
output/
├── solar_eclipse_all_2030_10/
│   ├── solar_eclipses_timeline.png
│   └── solar_eclipse_types.png
├── lunar_eclipse_first_2030_10/
│   ├── first_lunar_eclipse_timeline.png
│   └── first_lunar_eclipse_types.png
└── lunar_eclipse_1997-07-01/
    └── lunar_eclipse_report.png

```

## Contributor
| No | Nama | NIM |
|----|------|------|
| 1 |Aryo Wisanggeni | 13523100|
| 2 |Jethro Bezaliel Wijaya | 13123113|
