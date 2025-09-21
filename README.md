# dist_sys

## Project Overview

Repositori ini mendemonstrasikan berbagai **pola komunikasi dan implementasi** dalam sistem terdistribusi menggunakan Python. Setiap bagian memiliki contoh server dan kliennya masing-masing.

---

### 1. REST (Representational State Transfer)

Komunikasi berbasis **RESTful API** menggunakan Flask. Server menyediakan berbagai endpoint untuk operasi matematika, dan klien memanggilnya melalui permintaan HTTP GET.

- **REST Server (`REST/server.py`)**  
  Server Flask berjalan di port **5151**. Mengimplementasikan endpoint:
  - `/add`, `/mul`, `/sub`, `/div`, `/pow`, `/mod` – menerima dua parameter (a dan b) untuk operasi matematika.
  - `/fact` – menerima satu parameter (a) untuk menghitung faktorial.

- **REST Client (`REST/client.py`)**  
  Klien menggunakan pustaka `requests` untuk memanggil endpoint server dan mencetak hasilnya. Dapat memanggil satu atau semua operasi yang tersedia.

---

### 2. SOAP (Simple Object Access Protocol)

Komunikasi berbasis **pesan XML** untuk memanggil layanan web.

- **SOAP Server (`SOAP/server.py`)**  
  Dibuat dengan pustaka `spyne` dan mengekspos dua layanan:
  - `CalculatorService` (metode `add`)
  - `StringService` (metode `word_count`)  
  Server berjalan di port **8080**.

- **SOAP Client (`SOAP/client.py`)**  
  Klien menggunakan pustaka `zeep` untuk terhubung ke server SOAP dan memanggil metode `word_count` untuk menghitung jumlah kata dalam sebuah string.

---

### 3. ZeroMQ (ØMQ)

Implementasi berbagai pola komunikasi tingkat tinggi yang disediakan oleh **ZeroMQ**.

- **REQ/REP (Request/Reply)**  
  `serverzmq.py` menjawab dengan pesan “World” untuk setiap permintaan “Hello”.

- **PUB/SUB (Publish/Subscribe)**  
  `pubzmq.py` memublikasikan pesan waktu yang di-subscribe oleh `subzmq.py`.

- **PUSH/PULL (Pipeline)**  
  `pushzmq.py` menghasilkan beban kerja acak dan mengirimkannya, sementara `pullzmq.py` menerima dan memprosesnya.

---

### 4. Proses & Threads / ICE

Mendemonstrasikan perbedaan antara **proses** dan **threads** di Python, serta penggunaan **ZeroC Ice** sebagai kerangka kerja RPC.

- **Multiprocessing (`code_process/multiprcs.py`)**  
  Menjalankan dua proses terpisah (`eve` dan `bob`) yang tidur selama waktu acak untuk menunjukkan perilaku proses yang independen.

- **Multithreading (`code_process/multithreads.py`)**  
  Menjalankan beberapa thread dalam satu proses, memperlihatkan bagaimana thread dapat memanipulasi variabel bersama (`shared_x`).

- **Ice RPC (`code_process/ice_server.py`, `ice_client.py`)**  
  `Demo.ice` mendefinisikan antarmuka `Printer`, yang diimplementasikan oleh server Ice (`ice_server.py`). Klien (`ice_client.py`) berinteraksi dengan server dengan memanggil metode `printString`.

---

### 5. Docker Compose

File `docker-compose.yml` bertindak sebagai cetak biru untuk setiap pola komunikasi.  
Setiap file mendefinisikan layanan (server, klien, atau broker) dan mengaturnya agar berinteraksi di dalam jaringan virtual terisolasi. Hal ini memungkinkan setiap demo berjalan secara mandiri tanpa memengaruhi sistem host. Klien dan server berkomunikasi menggunakan nama layanan yang ditentukan dalam file Compose (misalnya `rest-server` atau `soap-server`).

---
