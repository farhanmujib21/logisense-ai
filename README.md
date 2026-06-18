# LogiSense AI

## Deskripsi Singkat Aplikasi

LogiSense AI merupakan aplikasi berbasis web yang dirancang untuk membantu perusahaan logistik dan manufaktur dalam mengelola data perawatan kendaraan dan alat berat secara digital. Sistem ini memanfaatkan teknologi Artificial Intelligence (AI) untuk melakukan validasi data, mendeteksi anomali, serta memberikan prediksi jadwal perawatan berdasarkan data historis.

Dengan adanya LogiSense AI, proses pencatatan maintenance yang sebelumnya dilakukan secara manual dapat menjadi lebih cepat, akurat, dan mudah dipantau secara real-time.

---

# Tujuan Pengembangan Aplikasi

1. Melakukan digitalisasi proses pencatatan maintenance kendaraan dan alat berat.
2. Mengurangi kesalahan pencatatan data melalui validasi otomatis.
3. Meningkatkan akurasi dan konsistensi data perawatan kendaraan.
4. Membantu perusahaan memantau kondisi armada secara real-time.
5. Menyediakan prediksi jadwal servis berdasarkan histori maintenance.
6. Mendukung pengambilan keputusan berbasis data.

---

# Daftar Fitur yang Tersedia

## Fitur Teknisi

- Login dan autentikasi pengguna
- Input data maintenance kendaraan
- Form perawatan digital
- Validasi data secara real-time
- Notifikasi kesalahan atau anomali data
- Riwayat perawatan kendaraan

## Fitur Manajer/Admin

- Dashboard monitoring armada
- Monitoring histori maintenance
- Prediksi jadwal servis kendaraan
- Manajemen data kendaraan
- Export laporan maintenance
- Pengelolaan pengguna sistem

## Fitur AI

- Rule-Based Anomaly Detection
- Validasi data maintenance otomatis
- Deteksi data tidak wajar
- Prediksi jadwal perawatan berdasarkan histori data

---

# Teknologi, Framework, Library, dan Komponen yang Digunakan

| Komponen | Teknologi |
|-----------|------------|
| Frontend | Django Templates |
| Styling | Bootstrap 5 |
| Backend | Django 4.x |
| Bahasa Pemrograman | Python 3 |
| Database | SQLite3 |
| AI Engine | Rule-Based Anomaly Detection |
| Web Server | Django Development Server |

---

# Struktur Database

Database yang digunakan adalah SQLite3.

## Tabel Asset

Digunakan untuk menyimpan data kendaraan atau alat berat.

| Field | Tipe Data |
|---------|---------|
| id | Integer |
| kode_aset | Varchar |
| nama_kendaraan | Varchar |
| kategori | Varchar |
| status | Varchar |

## Tabel Maintenance

Digunakan untuk menyimpan data perawatan kendaraan.

| Field | Tipe Data |
|---------|---------|
| id | Integer |
| asset_id | Foreign Key |
| tanggal_servis | Date |
| jenis_perawatan | Varchar |
| km_servis | Integer |
| catatan | Text |
| teknisi | Varchar |

## Tabel Activity Log

Digunakan untuk menyimpan aktivitas pengguna.

| Field | Tipe Data |
|---------|---------|
| id | Integer |
| user | Varchar |
| aktivitas | Text |
| waktu | DateTime |

---

# Panduan Instalasi dan Menjalankan Aplikasi

## 1. Clone Repository

```bash
git clone https://github.com/farhanmujib21/logisense-ai.git
cd logisense-ai
```

## 2. Membuat Virtual Environment

```bash
python -m venv venv
```

Aktifkan virtual environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux/MacOS

```bash
source venv/bin/activate
```

## 3. Install Dependency

```bash
pip install django
```

atau jika tersedia file requirements.txt:

```bash
pip install -r requirements.txt
```

## 4. Jalankan Migrasi Database

```bash
python manage.py migrate
```

## 5. Menjalankan Server

```bash
python manage.py runserver
```

Buka browser dan akses:

```text
http://127.0.0.1:8000
```

---

# Struktur Project

```text
logisense-ai/
│
├── logisense/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── maintenance/
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   └── migrations/
│
├── db.sqlite3
├── manage.py
└── README.md
```

---

# Screenshot Tampilan Aplikasi

## 1. Halaman Login

![Login]

## 2. Halaman Form Perawatan

![Form Perawatan](screenshots/form-perawatan.png)

## 3. Halaman Dashboard

![Dashboard](screenshots/dashboard.png)

## 4. Halaman Riwayat Perawatan

![Riwayat](screenshots/riwayat.png)

## 5. Halaman Admin

![Admin](screenshots/admin.png)

---

# Tim Pengembang

| Nama | NPM | Peran |
|--------|--------|--------|
| Farhan Mujiburrahman | Project Manager & AI Engineer |
| Nur Shadiqah |  Frontend Developer & UI/UX |
| Razian Sabri |  Backend & Database Engineer |

---

