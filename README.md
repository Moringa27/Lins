# Lins

**README - Simulator Komputasi Tomografi**

**Deskripsi**

Simulator Komputasi Tomografi adalah aplikasi berbasis GUI yang dikembangkan menggunakan Python dan Tkinter. Aplikasi ini memungkinkan pengguna untuk membuka gambar, melakukan transformasi Radon, serta merekonstruksi gambar menggunakan algoritma inverse Radon. Selain itu, pengguna dapat melihat histogram awal dan rekonstruksi serta profil intensitas gambar.

**Fitur Utama**

- Membuka dan menampilkan gambar.

- Melakukan transformasi Radon pada gambar.

- Menampilkan hasil proyeksi (sinogram).

- Merekonstruksi gambar menggunakan berbagai filter.

- Menampilkan histogram awal dan histogram setelah rekonstruksi.

- Menampilkan profil intensitas horizontal dan vertikal.

- Antarmuka berbasis Tkinter untuk pengalaman yang interaktif.

**Prasyarat**

Sebelum menjalankan aplikasi ini, pastikan bahwa Python telah terinstal bersama dengan pustaka berikut:

- tkinter

- numpy

- Pillow

- scikit-image

- matplotlib

Untuk menginstal pustaka yang dibutuhkan, jalankan perintah berikut di terminal atau command prompt:

`pip install numpy pillow scikit-image matplotlib`

**Cara Menjalankan**

1. Jalankan script Python dengan perintah:

`python nama_script.py`

2. Pilih tema tampilan (light atau dark) dengan memasukkan kode yang diminta di terminal.

3. Gunakan tombol "Buka Gambar" untuk memilih gambar yang akan diproses.

4. Gunakan tombol berikut sesuai kebutuhan:

- "Histogram Awal" untuk melihat distribusi intensitas gambar asli.

- "Hasil Proyeksi" untuk melihat sinogram hasil transformasi Radon.

- "Rekonstruksi Citra" untuk mengembalikan gambar dari sinogram menggunakan filter tertentu.

- "Histogram Rekon" untuk melihat histogram gambar yang telah direkonstruksi.

- "Profile Intensity" untuk membandingkan profil intensitas gambar asli dan rekonstruksi.

**Catatan**

- Gambar yang digunakan harus dalam format `.bmp, .jpg, atau .png`.

- Proses rekonstruksi dapat memerlukan waktu tergantung pada jumlah proyeksi dan ukuran gambar.

**Kontributor**

Pengembang: Lina Nurroin dan Nur Ma'rifatud Diniyah

**Lisensi**

Proyek ini tidak memiliki lisensi khusus. Pengguna dapat menggunakan, memodifikasi, dan mendistribusikan proyek ini. 

**Terima kasih telah menggunakan Simulator Komputasi Tomografi!**
