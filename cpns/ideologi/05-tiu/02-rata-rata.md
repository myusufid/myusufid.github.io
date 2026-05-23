# TIU — Menentukan Nilai Baru agar Rata-rata Berubah

Termasuk aplikasi di Saham (Average Cost).

---

## 1. Konsep Dasar Rata-rata (Mean)

$$\text{Rata-rata} = \frac{\text{Jumlah semua nilai}}{\text{Banyaknya data}}$$

**Contoh:**
Kamu sudah belajar 3 kali, nilainya 70, 80, 90 → Rata-rata = (70+80+90) / 3 = **80**

---

## 2. Rumus Utama

Kalau kamu sudah punya **n data** dengan rata-rata **A**, dan ingin rata-rata menjadi **B** setelah menambah 1 data baru (nilai **x**):

$$x = (B \times (n + 1)) - (A \times n)$$

Bentuk yang lebih mudah dihitung cepat:

$$\boxed{x = n(B - A) + B}$$

---

## 3. Penurunan Rumus (dari panjang ke singkat)

**Mulai dari:**
$$x = (B \times (n + 1)) - (A \times n)$$

**Distribusikan B:**
$$x = Bn + B - An$$

**Kelompokkan n:**
$$x = Bn - An + B$$

**Faktorkan n:**
$$x = n(B - A) + B$$

---

## 4. Cara Baca Rumus

- **n(B − A)** → total "selisih" yang harus ditanggung n data lama agar rata-rata naik dari A ke B
- **+ B** → tambahkan nilai target rata-rata baru

---

## 5. Contoh Soal

### Soal Ujian
> Seorang siswa mengikuti tes n kali, rata-rata 80. Nilai berapa yang harus diperoleh agar rata-rata menjadi 82?

A = 80, B = 82

$$x = n(82 - 80) + 82 = 2n + 82$$

**Jawaban: 2n + 82**

---

### Soal Saham (Average Cost)
> Seorang investor beli saham n kali, rata-rata Rp80.000/lembar. Harga beli ke-(n+1) agar rata-rata jadi Rp82.000?

A = 80.000, B = 82.000

$$x = n(82.000 - 80.000) + 82.000 = 2n + 82.000$$

**Jawaban: 2n + 82.000**

---

## 6. Contoh Angka Konkret

> 10 data (n=10), rata-rata 70 (A), ingin jadi 75 (B):

$$x = 10(75 - 70) + 75 = 50 + 75 = 125$$

Verifikasi: total lama = 700, total baru harus = 75 × 11 = 825. Nilai baru = 825 − 700 = **125** ✅

---

## 7. Jebakan Umum — "Kenapa bukan nilainya 82 saja?"

> n = 10, rata-rata lama = 80 → total = 800

Kalau nilai tes berikutnya = 82:

$$\frac{800 + 82}{11} = \frac{882}{11} = 80{,}18 \neq 82 \quad \text{(salah)}$$

Yang benar — hitung dulu total yang dibutuhkan:

$$82 \times 11 = 902 \quad \leftarrow \text{total yang dibutuhkan}$$

$$902 - 800 = 102 \quad \leftarrow \text{nilai yang harus didapat}$$

$$\frac{800 + 102}{11} = \frac{902}{11} = 82 \quad \checkmark$$

**Kuncinya:** supaya rata-rata naik, nilai tes berikutnya harus **di atas target rata-rata**. Kalau nilainya sama dengan target (82), rata-rata tidak akan naik — karena data lama masih menarik ke bawah.

Formula **2n + 82** = 2(10) + 82 = **102**, itulah yang benar.
