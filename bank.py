import random
import string

datanasabah = {}
datatransfer = {}


def getNasabah():
    nasabah_Txt = open("nasabah.txt")
    for data in nasabah_Txt:
        p = data.split(',')
        rek = {}
        rek['nama'] = p[1]
        rek['saldo'] = int(p[2])
        datanasabah[p[0]] = rek
    nasabah_Txt.close()
    print(datanasabah)


def updateNasabah():
    nasabah_Txt = open("nasabah.txt", "w+")
    for data in datanasabah:
        rekening = str(data)
        nama = str(datanasabah[data]['nama'])
        saldo = str(datanasabah[data]['saldo'])
        nasabah_Txt.write(rekening + ',' + nama + ',' + saldo + '\n')
    nasabah_Txt.close()


def updateTransfer():
    transfer_txt = open("transfer.txt", "a+")
    for transfer in datatransfer:
        nomerTransfer = str(datatransfer[transfer]['nomorTransfer'])
        rekening_pengirim = str(datatransfer[transfer]['pengirim'])
        rekening_penerima = str(datatransfer[transfer]['penerima'])
        nominal = str(datatransfer[transfer]['nominal'])
        transfer_txt.write(nomerTransfer + ',' + rekening_pengirim + ',' +
                           rekening_penerima + ',' + nominal + '\n')
    transfer_txt.close()


def getTransfer():
    transfer_txt = open("transfer.txt")
    for data in transfer_txt:
        q = data.split(',')
        trf = {}
        trf['pengirim'] = q[1]
        trf['penerima'] = q[2]
        trf['nominal'] = int(q[3])
        datatransfer[q[0]] = trf
    transfer_txt.close()


def bukaRekening():
    getNasabah()
    print("*** BUKA REKENING ***")
    nomorRek = "REK" + ''.join(random.choice(string.digits) for _ in range(3))

    while nomorRek in datanasabah.keys():
        nomorRek = "REK" + ''.join(random.choice(string.digits)
                                   for _ in range(3))
    nama = input("Masukan nama : ")
    setoran = int(input("Masukan setoran awal (minimal Rp.100.000) : "))

    if setoran >= 100000:
        datanasabah[nomorRek] = {
            'nama': nama,
            'saldo': setoran
        }
        print("-----------------------------------------------",
              "\n" + "Pembukaan rekening dengan nomor",
              nomorRek, "atas nama", nama, "berhasil.")
    else:
        print("-----------------------------------------------",
              "\n" + "Setoran awal kurang", "\n" + "Program selesai", "\n")
    updateNasabah()


def setor():
    getNasabah()
    print("*** SETOR TUNAI ***")
    nomorRek = input("masukkan nomor rekening anda : ").upper()
    jmlSetor = int(
        input("masukkan jumlah yang akan disimpan (Minimal Rp.100.000) : "))

    if nomorRek in datanasabah.keys():
        if jmlSetor >= 100000:
            datanasabah[nomorRek]['saldo'] += jmlSetor
            updateNasabah()
            print("-----------------------------------------------",
                  "\n" + "Setor sebesar", str(jmlSetor), "berhasil.\n" + "Saldo anda : Rp." + str(datanasabah[nomorRek]['saldo']), "\n")
        else:
            print("-----------------------------------------------",
                  "\n" + "Jumlah setoran anda kurang", "\n" + "Setor Tunai Gagal", "\n")
    else:
        print("-----------------------------------------------",
              "\n" + "Anda Bukan Nasabah, proses gagal", "\n" + "Setor Tunai Gagal", "\n")


def tarik():
    getNasabah()
    print("*** TARIK TUNAI ***")
    nomorRek = input("masukkan nomor rekening anda : ").upper()
    jmlTarik = int(
        input("masukkan jumlah yang akan ditarik (Minimal Rp.50.000) : "))

    if nomorRek in datanasabah.keys():
        if (jmlTarik <= (datanasabah[nomorRek]['saldo'] - 50000)) and (datanasabah[nomorRek]['saldo'] > 100000):
            datanasabah[nomorRek]['saldo'] -= jmlTarik
            updateNasabah()
            print("-----------------------------------------------",
                  "\n" + "Proses penarikan sebesar Rp." +
                  str(jmlTarik) + " berhasil!", "\n" + "Saldo anda : Rp." + str(datanasabah[nomorRek]['saldo']), "\n")
        else:
            print("-----------------------------------------------",
                  "\n" + "Jumlah saldo tidak boleh kurang dari Rp.50000", "\n", "Penarikan Gagal", "\n")
    else:
        print("-----------------------------------------------",
              "\n" + "Anda Bukan Nasabah, proses gagal", "\n", "Penarikan Gagal", "\n")


def transfer():
    getNasabah()
    print("*** TRANSFER UANG ***")
    rekening_pengirim = input("Masukkan nomor rekening pengirim: ").upper()
    rekening_penerima = input("Masukkan nomor rekening penerima: ").upper()
    nominal = int(input("Masukkan nominal transfer: "))
    if rekening_pengirim in datanasabah.keys():
        if rekening_penerima in datanasabah.keys():
            if nominal <= int(datanasabah[rekening_pengirim]['saldo']):
                datanasabah[rekening_pengirim]['saldo'] -= nominal
                datanasabah[rekening_penerima]['saldo'] += nominal
                nomorTransfer = "TRF" + \
                    ''.join(random.choice(string.digits) for _ in range(3))
                while nomorTransfer in datatransfer.keys():
                    nomorTransfer = "TRF" + \
                        ''.join(random.choice(string.digits) for _ in range(3))
                datatransfer['transfer'] = {
                    'nomorTransfer': nomorTransfer,
                    'pengirim': rekening_pengirim,
                    'penerima': rekening_penerima,
                    'nominal': nominal
                }
                updateTransfer()
                updateNasabah()
                print("-----------------------------------------------",
                      "\n" + "Transfer sebesar", str(nominal), "berhasil.\n")
                print("Nomor Transfer :", nomorTransfer, "\n" + "Pengirim :",
                      rekening_pengirim, "\n" + "Penerima :", rekening_penerima, "\n" + "Nominal :", nominal)
            else:
                print("-----------------------------------------------",
                      "\n" + "Saldo anda tidak mencukupi. Masukkan nominal transfer yang lebih kecil.\n", "Transfer Gagal.\n")
        else:
            print("-----------------------------------------------",
                  "\n" + "Nomor rekening penerima tidak terdaftar. Silakan masukkan nomor rekening yang valid.\n", "Transfer Gagal.\n")
    else:
        print("-----------------------------------------------",
              "\n" + "Nomor rekening anda tidak terdaftar. Proses transfer selesai.\n", "Transfer Gagal.\n")


def listTransfer():
    getNasabah()
    getTransfer()
    print("*** LIST DATA TRANSFER ***")
    rekening = input("masukkan nomor rekening : ").upper()
    rekPengirim = []

    for data in datatransfer.keys():
        rekPengirim.append(str(datatransfer[data]['pengirim']))
    if (rekening in datanasabah.keys()) and (rekening not in rekPengirim):
        print("-----------------------------------------------",
              "\n" + "Rekening belum melakukan transaksi apapun")
    elif (rekening in datanasabah.keys()) and (rekening in rekPengirim):
        print("-----------------------------------------------",
              "\n" + "List transfer dengan nomor rekening", rekening, ":")
        for pengirim in datatransfer.keys():
            if rekening in datatransfer[pengirim]['pengirim']:
                print("-", pengirim, datatransfer[pengirim]['pengirim'],
                      datatransfer[pengirim]['penerima'], datatransfer[pengirim]['nominal'])
    else:
        print("-----------------------------------------------",
              "\n" + "Nomor rekening tidak terdaftar", "\n" + "Proses selesai..")


def cekSaldo():
    getNasabah()
    print("*** CEK SALDO ***")
    rekening = input("masukkan nomor rekening : ").upper()
    print("-----------------------------------------------",
          "\n" + "Saldo rekening Anda sebesar : Rp." + str(datanasabah[rekening]['saldo']))


lagi = 'y'
while lagi == 'y':
    print("******* SELAMAT DATANG DI NF BANK *******", "\n" + "MENU: ", "\n" +
          "[1] Buka Rekening", "\n" + "[2] Setor Tunai", "\n" + "[3] Tarik Tunai", "\n" + "[4] Transfer", "\n" + "[5] Lihat Data Transfer", "\n" + "[6] Cek Saldo", "\n" + "[7] Keluar")
    pilihan = input("Masukkan menu pilihan Anda : ")

    if pilihan == '1':
        bukaRekening()
    elif pilihan == '2':
        setor()
    elif pilihan == '3':
        tarik()
    elif pilihan == '4':
        transfer()
    elif pilihan == '5':
        listTransfer()
    elif pilihan == '6':
        cekSaldo()
    elif pilihan == '7':
        break
    else:
        print("Anda memasukkan input yang salah", "\n" +
              "Program Selesai", "\n" + "Terima kasih atas kunjungan Anda...")
    lagi = input("Ingin melakukan transaksi lagi?? (y/n) :").lower()
print("-----------------------------------------------",
      "\n" + "Program Selesai", "\n" + "Terima kasih atas kunjungan Anda...")
