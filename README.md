# Tucil Strategi Algoritma 1

## Valentino Daniel Kusumo - 13524104

## Deskripsi Program
Program ini ditujukan untuk mencari solusi dari *game* Queens LinkedIn dengan menggunakan algoritma Brute Force, tetapi juga ada kemungkinan permainan tidak memiliki solusi jika tidak ada konfigurasi yang memenuhi.

## Batasan Permainan
- Setiap baris dan kolom maksimal memiliki 1 *queen*
- Dalam 1 daerah, maksimal hanya boleh terdapat 1 *queen*
- *Queen* tidak boleh bersebelahan secara horizontal, vertikal, maupun diagonal (jarak dekat)

## Cara Menjalankan GUI
1. Pastikan Python sudah terinstall (disarankan Python 3.10 atau lebih baru).

2. Install *library* yang dibutuhkan
    ```
    pip install flet pillow
    ```
    
3. Lakukan clone repository

4. Masuk ke folder utama project

5. Jalankan perintah berikut
    ```
    python src/maingui.py
    ```
    
6. Upload file *input* atau memasukkan kasus langsung pada *board* sebelah kiri
   
7. Menentukan apakah akan menggunakan optimalisasi *backtracking* atau tidak yang disediakan pada *checkbox* di bawah **(backtracking sangat disarankan)**

8. Menekan tombol *solve*
    
9. Hasil akhir akan ditampilkan pada *board* sebelah kanan
    
10. Jika ingin menyimpan solusi, dapat menekan tombol *Export TXT* (sebagai file .txt) atau *Export Image* (sebagai image)

## Cara Menjalankan Program (tanpa GUI -- *tidak selengkap GUI*)

1. Pastikan Python sudah terinstall (disarankan Python 3.10 atau lebih baru).

2. Install *library* yang dibutuhkan
    ```
    pip install flet pillow
    ```
    
3. Lakukan clone repository

4. Masuk ke folder utama project
   
5. Jalankan perintah berikut
   ```
   python src/maincli.py
   ```
   
6. Masukkan nama file yang akan menjadi *input* dalam permainan *(tanpa menuliskan .txt)*
   
7. Menentukan apakah akan menggunakan optimalisasi *backtracking* atau tidak **(backtracking sangat disarankan)**
   
8. Hasil akhir akan ditampilkan pada terminal

![cover](cover.png)
