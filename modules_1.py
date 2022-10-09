from sqlite3 import *
from time import *
from datetime import *
from xlrd import *


con = connect("db.db")
c = con.cursor()
# Tablo oluşturuyoru
c.execute("""CREATE TABLE IF NOT EXISTS ogrenciler(ogrenci text, no integer)""")
c.execute("""CREATE TABLE IF NOT EXISTS kitaplar(kitap text, barkod integer)""")
c.execute("CREATE TABLE IF NOT EXISTS kitaplarvar(barkod integer)")
c.execute("CREATE TABLE IF NOT EXISTS kitaplarverildi(barkod integer, no integer, tarih text, tarih2 integer)")
c.execute("""CREATE TABLE IF NOT EXISTS sifre (kadi text, sifre text)""")
con.commit()


def baslangic_sifre_olustur(admin, admin_sifre, nobetci, nobetci_sifre):
    
    c.execute("""INSERT INTO sifre VALUES(?, ?)""", (admin, admin_sifre))
    c.execute("""INSERT INTO sifre VALUES(?, ?)""", (nobetci, nobetci_sifre))
    con.commit()
    
def sifre_degistir(kadi, ksifre):

    c.execute("""UPDATE sifre SET sifre= (?) WHERE kadi= (?)""", (ksifre, kadi))
    con.commit()
    

def sifre_kontrol(kadi, sifre):
    sayac = 0
    c.execute("SELECT * FROM sifre")
    con.commit()
    girisler = c.fetchall()
    anahtar = False
    for giris in girisler:
        if anahtar == False:
            sayac += 1
        if giris[0] == kadi and giris[1] == sifre:
            anahtar = True
        else:
            pass
    
    return anahtar, sayac

def ogr_ekle(ogrenci, no):
    
    c.execute("""INSERT INTO ogrenciler VALUES (?, ?)""", (ogrenci, no))
    con.commit()

def ogr_sil(no):
    c.execute("""DELETE FROM ogrenciler WHERE no = ?""", (no,))
    con.commit()

def kitap_ekle(kitap, barkod):
    c.execute("""INSERT INTO kitaplar VALUES (?,?)""", (kitap, barkod))
    c.execute("""INSERT INTO kitaplarvar VALUES (?)""", (barkod,))
    con.commit()

def kitap_sil(barkod):
    c.execute("""DELETE FROM kitaplar WHERE rowid = (SELECT rowid FROM kitaplar WHERE barkod = ?)""", (barkod,))
    c.execute("""DELETE FROM kitaplarvar WHERE rowid = (SELECT rowid FROM kitaplarvar WHERE barkod = ?)""", (barkod,))
    con.commit()

def kitap_ver(barkod, no, tarih):

    c.execute("SELECT * FROM kitaplarvar WHERE barkod = ?", (barkod,))
    con.commit()

    tarih2 = tarih.split("-")
    tarih2 = int(tarih2[0] + tarih2[1] + tarih2[2])

    if len(c.fetchall()) != 0:
        
        c.execute("DELETE FROM kitaplarvar WHERE rowid = (SELECT rowid FROM kitaplarvar WHERE barkod = ?)", (barkod,))
        c.execute("INSERT INTO kitaplarverildi VALUES(?, ?, ?, ?)", (barkod, no, tarih, tarih2))
        con.commit()

        return 1
    else:
        return 0
def kitap_al(barkod, no):
    c.execute("DELETE FROM kitaplarverildi WHERE rowid = (SELECT rowid FROM kitaplarvar WHERE barkod = ? AND no = ?)", (barkod, no))
    c.execute("INSERT INTO kitaplarvar VALUES(?)", (barkod,))
    con.commit()

def zaman(tarih):
    b = strftime("%Y %m %d").split(" ")
    b[0] = int(b[0])
    b[1] = int(b[1])
    b[2] = int(b[2])
    bugun = datetime(b[0],b[1],b[2])
    t = tarih.split("-")
    t[0] = int(t[0])
    t[1] = int(t[1])
    t[2] = int(t[2])

    tarih = datetime(t[0], t[1], t[2])
    
    kalan_gun = tarih - bugun

    return kalan_gun.days

def veri_ver(barkod, no, tarih):
    c.execute("SELECT ogrenci FROM ogrenciler WHERE no = ?", (no,))
    con.commit()

    try:
        ogrenci = c.fetchall()[0]

    except:
        ogrenci = "-"

    c.execute("SELECT kitap FROM kitaplar WHERE barkod = ?", (barkod,))
    con.commit()

    try:
        kitap_adi = c.fetchall()[0]

    except:
        kitap_adi = "-"

    try:
        kalan_gun = zaman(tarih)

    except:
        kalan_gun = "-"

    return ogrenci, kitap_adi, kalan_gun
 
 

def spinbox_tarih():
    liste = []
    for i in range(60):
        b = strftime("%Y %m %d").split(" ")
        b[0] = int(b[0])
        b[1] = int(b[1])
        b[2] = int(b[2])
        bugun = datetime(b[0],b[1],b[2])
        bugun = bugun + timedelta(i)
        bugun = str(bugun).split(" ")[0]
        
        liste.append(bugun)
    return liste

def excelden_aktar(ogr_excel_dosya=None, ktp_excel_dosya=None):
    
    try:
        if ogr_excel_dosya != None and ogr_excel_dosya != "":
            c.execute("DELETE FROM ogrenciler")
            con.commit()
            ogrenciler_xl = (ogr_excel_dosya)
            wb = open_workbook(ogrenciler_xl)
            sheet = wb.sheet_by_index(0)
            sheet.cell_value(0, 0)

            for i in range(sheet.nrows):
                isim = sheet.cell_value(i, 0)
                no = sheet.cell_value(i, 1)

                ogr_ekle(isim, no)
        if ktp_excel_dosya != None and ktp_excel_dosya != "":
            c.execute("DELETE FROM kitaplar")
            c.execute("DELETE FROM kitaplarvar")
            c.execute("DELETE FROM kitaplarverildi")
            con.commit()
            kitaplar_xl = (ktp_excel_dosya)
            wb = open_workbook(kitaplar_xl)
            sheet = wb.sheet_by_index(0)
            sheet.cell_value(0, 0)

            for i in range(sheet.nrows):
                isim = sheet.cell_value(i, 0)
                barkod = sheet.cell_value(i, 1)

                kitap_ekle(isim, barkod)
        return True
    except:
        print("hata: dosya aktarılamadı lütfen formatın '.xls' olduğundan emin olunuz.")
        return False
	
