## Syarat

- GPG key anda harus tanpa password

  GPG key yang ada password-nya belum pernah dicoba. Tidak tahu apakah script ini juga tetap akan bekerja atau tidak.


  <br>

## cara memasang script ini

Silahkan copy script tersebut ke dalam file: `/home/<username_anda>/_script_penting/_checksum_updater.sh`

<br><br>

#### Berikut ini caranya mencopy script tersebut ke directory tersebut:

```
cd '/home/<username_anda>'

mkdir '_script_penting'

cd _script_penting

nano _checksum_updater.sh
```

Setelah itu copy paste kode tersebut, lalu tekan ctrl+o untuk save, dan ctrl+x untuk keluar setelah save. Jangan lupa mengubah beberapa variabel dari script tersebut sesuai kebutuhan. Biasanya cuman perlu mengubah variabel username



<br><br>



#### Setelah itu kita perlu mengaktifkan izin untuk menjalankan file bash tersebut dengan cara:



```
cd '/home/<username_anda>/_script_penting'
chmod +x _checksum_updater.sh
```



<br><br>

#### Setelah itu kita perlu mendaftarkan script tersebut supaya otomatis dijalankan oleh linux setiap 1 menit sekali. Berikut ini caranya:
`crontab -e`

Akan ada banyak kalimat yang diawali #. Silahkan move cursor ke paling bawah dan tambahkanlah dua baris ini:

```
# checksum updater and signer
*/1 * * * * /home/<username_anda>/_script_penting/_checksum_updater.sh
```


Jika tidak bisa mengedit, mungkin kalian sedang menggunakan text editor vi. Jika dalam editor vi, coba tekan i untuk mengaktifkan mode mengedit.
Jika sudah, silahkan save dan keluar dari situ. Caranya, untuk editor vi, tekan escape > titik dua > w > q > enter. Untuk nano, tekan ctrl+o > enter > ctrl+x.


<br><br>


Jika sudah, program kalian siap digunakan. Perhatikan bahwa program hanya berfungsi ketika linux kalian sedang dijalankan dan sedang login pada akun tersebut. Silahkan coba lakukan perubahan pada git anda, commit, dan push. Lalu tunggu 1 atau 2 menit, biarkan linux anda tetap berjalan. Lalu cek `https://github.com/<username_github_anda>/os212/commits/` dan lihat apakah ada commit terbaru yang formatnya seperti tanggal atau tidak (contoh `18/09/2021 01:41:01`). Jika ada, maka program sudah berjalan dengan baik. Selamat mencoba! 

:D

<br><br>

(Jika ada kendala/bug, mungkin boleh pc gw melalui line)