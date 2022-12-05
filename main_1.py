
from tkinter import *
from tkinter import messagebox
from tkinter import ttk as t
from time import *
from datetime import *
from sqlite3 import *
from modules_1 import *
#from sv_ttk import *
from PIL import Image, ImageTk


anahtar1 = True
anahtar2 = False
state = "active" #active , disabled
state2 = "" #normal , disabled
state3 = "" #normal , disabled


def main():
    global state
    global state2
    ana = Tk()
    # Create a style
    style = t.Style(ana)

# Import the tcl file
    ana.call("source", "forest-dark.tcl")

# Set the theme with the theme_use method
    style.theme_use("forest-dark")




    ayarpng = ImageTk.PhotoImage(file="ayarlar.png")
    ktpverpng = ImageTk.PhotoImage(file="kitap_ver.png")
    ogrktpes = ImageTk.PhotoImage(file="ogr_ekle_sil.png")
    baslangic = ImageTk.PhotoImage(file="hosgeldiniz.png")
    baslangic_sifre = ImageTk.PhotoImage(file="sifre_olustur.png")
    kk = ImageTk.PhotoImage(file="kk.png")

    #sv_ttk.use_dark_theme()

    #ana.iconbitmap("logo.ico")
    ana.title("FETGEM Kütüphane Otomasyon")
    ana.geometry("912x500")
    ana.resizable(FALSE, FALSE)
    ana.focus_force()
    pencereler = t.Notebook(ana)

    g = Frame(pencereler)
    ok = Frame(pencereler)
    k = Frame(pencereler)
    ogr_ktp_list = Frame(pencereler)
    kz = Frame(pencereler)
    s = Frame(pencereler)
    bsk = Frame(pencereler)
    pencereler.place(x=0, y=0, width=912, height=500)
    gsayac = 0

    def program():
        pencereler.add(g, state=state2, text="Verilecek Kitaplar")
        pencereler.add(k,state=state2, text="       Kitap Ver      ")
        pencereler.add(ok,state=state2, text="""   Öğrenci/ Kitap İşlemleri""")
        pencereler.add(ogr_ktp_list,state=state2, text="""Öğrenciler Kitaplar""")
        pencereler.add(kz,state=state2, text="Kullanım Kılavuzu")
        pencereler.add(s, state=state3, text="     Ayarlar      ")

        resim_kk = Label(kz, image=kk).place(x=0, y=0)

        def agac_olustur():
            global agac

            columns = ["ogrenci", "kitap", "kalan_gun"]
            agac = t.Treeview(g, columns=columns, show="headings", height=20)

            agac.heading("ogrenci", text="Öğrenci")
            agac.heading("kitap", text="Kitap")
            agac.heading("kalan_gun", text="Kalan Gün")

            agac.column("ogrenci", width=400)
            agac.column("kitap", width=350)
            agac.column("kalan_gun", width=107)
            agac.grid()

            c.execute("""SELECT * FROM kitaplarverildi ORDER BY tarih2""")
            veriler = c.fetchall()

            for veri in veriler:
                iid = str(veri[0]) + " " + str(veri[1])
                veri = veri_ver(veri[0], veri[1], veri[2])
                if int(veri[2]) < 0:
                    agac.insert("", END, iid=iid, values=(veri[0][0], veri[1][0], veri[2]), tags=("az"))
                elif int(veri[2]) < 1:
                    agac.insert("", END, iid=iid, values=(veri[0][0], veri[1][0], veri[2]), tags=("orta"))

                elif int(veri[2]) < 8:
                    agac.insert("", END, iid=iid, values=(veri[0][0], veri[1][0], veri[2]), tags=("normal"))

                else:
                    agac.insert("", END, iid=iid, values=(veri[0][0], veri[1][0], veri[2]))

            def soru():
                global anahtar1
                if anahtar1:
                    return messagebox.askyesno(title="Kitabı al?", message="Kitabın teslim edildiğini onaylıyor musunuz?")
                else:
                    anahtar1 = True
            def kitap_al_ttk(bos):
                global anahtar1
                if soru():
                    iid = agac.selection()[0]
                    agac.delete(iid)
                    iid_bol = iid.split(" ")
                    kitap_al(iid_bol[0], iid_bol[1])
                    agac.focus()
                    anahtar1 = False
            agac.tag_configure("az", background="red")
            agac.tag_configure("orta", background="orange")
            agac.tag_configure("normal", background="blue")

            agac.bind("<<TreeviewSelect>>", kitap_al_ttk)

        def kitap_ver_olustur():

            def get_values():
                global  barkod_kitap_ver, no_kitap_ver, tarih_kitap_ver
                
                        
                barkod_kitap_ver = (barkod_e.get())
                no_kitap_ver = (no_e.get())
                tarih_kitap_ver = tarih_se.get()
                

            barkod_veri = ''
            no_veri = ''
            tarih_veri = ''

            ktp_veri_var = StringVar()
            ktp_veri_var.set('')
            no_veri_var = StringVar()
            no_veri_var.set('')
            tarih_veri_var = StringVar()
            tarih_veri_var.set('')

            def kitap_ver_tk():
                try:
                    get_values()
                    message = messagebox.askyesno(title="Onayla?", message="Kitabın ödünç verildiğini onaylıyor musunuz?")
                    if message:

                        if kitap_ver(barkod_kitap_ver, no_kitap_ver, tarih_kitap_ver):

                            agac.grid_forget()
                            agac_olustur()
                            ktp_veri_var.set('')
                            no_veri_var.set('')
                            tarih_veri_var.set('')
                        else:
                            messagebox.showerror(title="Hata", message="İşlem Tamamlanamadı! Kitap veya öğrenci bulunamadı. Kitap önceden verilmiş olabilir.")
                except:
                    messagebox.showerror(title="Hata", message="Tekrar deneyin!")
                barkod_e.delete(0, END)
                no_e.delete(0, END)
                tarih_se.delete(0, END)


            def ktp_ver_sorgu():
                

                get_values()


                if kitap_ver_sorgu(no_kitap_ver, barkod_kitap_ver):
                    c.execute("""SElECT ogrenci FROM ogrenciler WHERE no = (?)""", (no_kitap_ver,))
                    con.commit()

                    ogr_veri = c.fetchall()[0][0]

                    c.execute("""SElECT kitap FROM kitaplar WHERE barkod = (?)""", (barkod_kitap_ver,))
                    con.commit()

                    ktp_veri = c.fetchall()[0][0]

                    tarih = tarih_kitap_ver.split('-')
                    tarih= liste_string(tarih)

                    no_veri_var.set(ogr_veri)

                    if len(ktp_veri) > 25:
                        str = ''
                        for i in range(23):
                            str = str + ktp_veri[i]
                        str = str + '...'

                    else:
                        str = ktp_veri

                    ktp_veri_var.set(str)
                    tarih_veri_var.set(tarih)




                else:
                    messagebox.showerror('Hata', 'Kayıt Bulunamadı.')
                    ktp_veri_var.set('')
                    no_veri_var.set('')
                    tarih_veri_var.set('')






            values1 = spinbox_tarih()
            resim1 = Label(k, image=ktpverpng)
            resim1.place(x=0, y=0)
            barkod_e = Entry(k, background="#DFDFDF", foreground="#343434", width=21, font="roboto 15", borderwidth=0, border=0, highlightthickness=0)
            no_e = Entry(k, background="#DFDFDF", foreground="#343434", width=21, font="roboto 15", borderwidth=0,border=0, highlightthickness=0)
            tarih_se = Spinbox(k, values=values1, background="#dfdfdf", foreground="#343434")
            tarih_se.configure(background="#dfdfdf", font="roboto 14", borderwidth=0, highlightthickness=0, width=19)
            tarih_se.delete(0, END)
            tarih_se.insert(0,values1[7])
            sorgu_b = t.Button(k, text='      Sorgu       ', command=ktp_ver_sorgu)
            onay_b = t.Button(k, text="   Kitabı Ver   ", command=kitap_ver_tk)
            barkod_e.place(x=155, y=155)
            no_e.place(x=155, y=201)
            tarih_se.place(x=155, y=251)
            sorgu_b.place(x=190, y=300)
            onay_b.place(x=622, y=330)

            ogr_bilg_label = Label(k, font='roboto 13', bg='#a4a4a4', textvariable=no_veri_var)
            ktp_bilg_label = Label(k,font='roboto 13', bg='#a4a4a4', textvariable=ktp_veri_var)
            trh_bilg_label = Label(k, font='roboto 13', bg='#a4a4a4', textvariable=tarih_veri_var)
            ogr_bilg_label.place(x=585,y=100)
            ktp_bilg_label.place(x=585,y=175)
            trh_bilg_label.place(x=585,y=250)


        def ogrenciler_kitaplar_olustur():
            global agac_o
            global agac_k
            ogr_columns = ["ogr", "no"]
            ktp_columns = ["ktp", "barkod"]
            agac_o = t.Treeview(ogr_ktp_list, columns=ogr_columns, show="headings", height=18)
            agac_o.heading("ogr", text="Öğrenci")
            agac_o.heading("no", text="No")
            agac_o.grid(row=0, column=0, columnspan=3)
            agac_o.column("ogr", width=250)
            agac_o.column("no", width=150)
            agac_k = t.Treeview(ogr_ktp_list, columns=ktp_columns, show="headings", height=18)
            agac_k.heading("ktp", text="Kitap")
            agac_k.heading("barkod", text="Barkod")
            agac_k.grid(row=0,column=3, columnspan=3)
            agac_k.column("ktp", width=257)
            agac_k.column("barkod", width=160)

            def ogrenci_yerlestir():
                c.execute("SELECT * FROM ogrenciler ORDER BY ogrenci")
                con.commit()
                ogr_liste = c.fetchall()
                for ogr in ogr_liste:
                    agac_o.insert("", END, values=ogr)

            def kitap_yerlestir():
                c.execute("SELECT * FROM kitaplar ORDER BY kitap")
                con.commit()
                ktp_liste = c.fetchall()
                for ktp in ktp_liste:
                    agac_k.insert("", END, values=ktp)

            label = Label(ogr_ktp_list, text="Dosya", font="roboto 13")
            label.grid(row=1, column=0)
            label2 = Label(ogr_ktp_list, text="Dosya", font="roboto 13")
            label2.grid(row=1, column=3)

            entry_o_xl = Entry(ogr_ktp_list, background="#343434", foreground="#DFDFDF", width=22, font="roboto 13", borderwidth=0, border=0, highlightthickness=0)
            entry_k_xl = Entry(ogr_ktp_list, background="#343434", foreground="#DFDFDF", width=22, font="roboto 13", borderwidth=0, border=0, highlightthickness=0)
            entry_o_xl.grid(row=1, column=1)
            entry_k_xl.grid(row=1, column=4)

            def komut_k_xl():
                dosya_k_xl = entry_k_xl.get()
                excelden_aktar(ktp_excel_dosya=dosya_k_xl)
                agac_k.grid_forget()
                ogrenciler_kitaplar_olustur()

            def komut_o_xl():
                dosya_o_xl = entry_o_xl.get()
                excelden_aktar(ogr_excel_dosya=dosya_o_xl)
                agac_o.grid_forget()
                ogrenciler_kitaplar_olustur()

            buton_o_xl = t.Button(ogr_ktp_list, text="İçeri Aktar", command=komut_o_xl, state=state)
            buton_k_xl = t.Button(ogr_ktp_list, text="İçeri Aktar", command=komut_k_xl, state=state)
            buton_o_xl.grid(row = 1, column=2)
            buton_k_xl.grid(row=1, column=5)

            kitap_yerlestir()
            ogrenci_yerlestir()

        def o_k_ekleme_silme_olustur():
            global agac_o
            global agac_k
            global state
            def komut_ogr_1():
                try:
                    ogr = ogr_adi_e.get(), int(ogr_no_e.get())
                    ogr_ekle(ogr[0], ogr[1])
                    ogr_adi_e.delete(0, END)
                    ogr_no_e.delete(0, END)
                    agac_o.grid_forget()
                    agac_k.grid_forget()
                    ogrenciler_kitaplar_olustur()

                except:
                    messagebox.showerror(title="Hata", message="Tekrar deneyin!")
                    ogr_adi_e.delete(0, END)
                    ogr_no_e.delete(0, END)

            def komut_ogr_2():
                try:
                    no = int(ogr_no_sil_e.get())
                    ogr_sil(no)
                    ogr_no_sil_e.delete(0, END)
                    agac_o.grid_forget()
                    agac_k.grid_forget()
                    ogrenciler_kitaplar_olustur()

                except:
                    messagebox.showerror(title="Hata", message="Tekrar deneyin!")
                    ogr_no_sil_e.delete(0, END)

            def komut_ktp_1():

                try:

                    ktp = ktp_adi_e.get(), int(ktp_no_e.get())
                    kitap_ekle(ktp[0], ktp[1])
                    ktp_adi_e.delete(0, END)
                    ktp_no_e.delete(0, END)
                    agac_o.grid_forget()
                    agac_k.grid_forget()
                    ogrenciler_kitaplar_olustur()

                except:
                    messagebox.showerror(title="Hata", message="Tekrar deneyin!")
                    ktp_adi_e.delete(0, END)
                    ktp_no_e.delete(0, END)
            def komut_ktp_2():
                try:
                    no = int(ktp_no_sil_e.get())
                    kitap_sil(no)
                    ktp_no_sil_e.delete(0, END)
                    agac_o.grid_forget()
                    agac_k.grid_forget()
                    ogrenciler_kitaplar_olustur()

                except:
                    messagebox.showerror(title="Hata", message="Tekrar deneyin!")
                    ktp_no_sil_e.delete(0, END)

            resim2 = Label(ok, image=ogrktpes).place(x=0, y=0)

            ogr_adi_e = Entry(ok, background="#DFDFDF", foreground="#343434", width=21, font="roboto 15", borderwidth=0, border=0, highlightthickness=0)
            ogr_no_e = Entry(ok, background="#DFDFDF", foreground="#343434", width=21, font="roboto 15", borderwidth=0, border=0, highlightthickness=0)
            ogr_onay = t.Button(ok, text="        Ekle        ", command=komut_ogr_1, state=state)
            ogr_adi_e.place(x=141, y=128)
            ogr_no_e.place(x=141, y=176)
            ogr_onay.place(x=185, y=220)

            ogr_no_sil_e = Entry(ok, background="#DFDFDF", foreground="#343434", width=21, font="roboto 15", borderwidth=0, border=0, highlightthickness=0)
            ogr_no_sil_e.place(x=141, y=288)
            ogr_sil_onay = t.Button(ok, text="         Sil         ", command=komut_ogr_2, state=state)
            ogr_sil_onay.place(x=185, y=328)

            ktp_adi_e = Entry(ok, background="#DFDFDF", foreground="#343434", width=21, font="roboto 15", borderwidth=0, border=0, highlightthickness=0)
            ktp_no_e = Entry(ok, background="#DFDFDF", foreground="#343434", width=21, font="roboto 15", borderwidth=0, border=0, highlightthickness=0)
            ktp_onay = t.Button(ok, text="        Ekle        ", command=komut_ktp_1, state=state)
            ktp_adi_e.place(x=558, y=128)
            ktp_no_e.place(x=558, y=176)
            ktp_onay.place(x=596, y=220)

            ktp_no_sil_e = Entry(ok, background="#DFDFDF", foreground="#343434", width=21, font="roboto 15", borderwidth=0, border=0, highlightthickness=0)
            ktp_no_sil_e.place(x=558, y=288)
            ktp_sil_onay = t.Button(ok, text="         Sil         ",command=komut_ktp_2, state=state)
            ktp_sil_onay.place(x=596, y=328)

        def ayarlar_olustur():
            resim3 = Label(s, image=ayarpng).place(x=0, y=0)
            kullanici_adi_e = Entry(s, background="#DFDFDF", foreground="#343434", width=21, font="roboto 15", borderwidth=0, border=0, highlightthickness=0)
            sifre_e = Entry(s, background="#DFDFDF", foreground="#343434", width=21, font="roboto 15", borderwidth=0, border=0, highlightthickness=0)

            def sifre_degistir_main():
                kadi = kullanici_adi_e.get()
                ksifre = sifre_e.get()

                sifre_degistir(kadi, ksifre)
                messagebox.showinfo(title="Tamamlandı", message="İşlem Tamamlandı")


            onay = t.Button(s, text="    Değiştir    ",command=sifre_degistir_main)
            onay.place(x=187, y=248)

            kullanici_adi_e.place(x=214, y=107)
            sifre_e.place(x=214, y=164)

        agac_olustur()
        o_k_ekleme_silme_olustur()
        kitap_ver_olustur()
        ogrenciler_kitaplar_olustur()
        ayarlar_olustur()

    def bas_sif_kont():
        global state
        global state2
        c.execute("SELECT * FROM sifre")
        con.commit()
        sifreler = c.fetchall()

        if len(sifreler) < 2:
            state2 = "disabled"
            pencereler.add(bsk,text="""    Baslangıç    """)
            bilgilendirme =Label(bsk,image=baslangic)
            bilgilendirme.place(x=0, y=0)

            def tamam_b():
                global baslangic
                bilgilendirme.config(image=baslangic_sifre)
                tamam.place_forget()


                ykadi_olustur_e = Entry(bsk, background="#DFDFDF", foreground="#343434", width=21, font="roboto 15", borderwidth=0, border=0, highlightthickness=0)
                yksifre_olustur_e = Entry(bsk, background="#DFDFDF", foreground="#343434", width=21, font="roboto 15", borderwidth=0, border=0, highlightthickness=0)
                nkadi_olustur_e = Entry(bsk, background="#DFDFDF", foreground="#343434", width=21, font="roboto 15", borderwidth=0, border=0, highlightthickness=0)
                nksifre_olustur_e = Entry(bsk, background="#DFDFDF", foreground="#343434", width=21, font="roboto 15", borderwidth=0, border=0, highlightthickness=0)

                def baslangic():
                    global state
                    global state2
                    admin = ykadi_olustur_e.get()
                    admins = yksifre_olustur_e.get()
                    nobetci = nkadi_olustur_e.get()
                    nobetcis = nksifre_olustur_e.get()

                    if admin != "" and admins != "" and nobetci != "" and nobetcis != "":
                        baslangic_sifre_olustur(admin, admins, nobetci, nobetcis)
                        messagebox.showinfo(title="Tamamlandı", message="İşlem Tamamlandı")
                        state2 = "normal"

                        ykadi_olustur_e.grid_forget()
                        yksifre_olustur_e.grid_forget()
                        nkadi_olustur_e.grid_forget()
                        nksifre_olustur_e.grid_forget()
                        baslangic_sifre_olustur_buton.grid_forget()
                        pencereler.forget(bsk)
                        global girispng

                        c.execute("SELECT * FROM sifre")
                        con.commit()
                        veri = c.fetchall()
                        print(veri)
                        kullanici_adlari = veri[0][0], veri[1][0]
                        print(kullanici_adlari)


                        pencereler.add(bsk,text="""    Baslangıç     """)
                        state2 = "disabled"
                        girispng = ImageTk.PhotoImage(file="giris.png")
                        bgfoto = Label(bsk, image=girispng)

                        kadi_e = Entry(bsk, background="#DFDFDF", foreground="#343434", width=21, font="roboto 15", borderwidth=0, border=0, highlightthickness=0)
                        sifre_e = Entry(bsk, background="#DFDFDF", foreground="#343434", width=21, font="roboto 15", borderwidth=0, border=0, highlightthickness=0)

                        def giris():
                            global state
                            global state2
                            global state3


                            giris_anahtar, kullanici_id = sifre_kontrol(kadi_e.get(), sifre_e.get())
                            if giris_anahtar:
                                if kullanici_id == 1:
                                    state="active"
                                    state2="normal"
                                    state3="normal"
                                else:
                                    state = "disabled"
                                    state2 = "normal"
                                    state3 = "disabled"
                                pencereler.forget(bsk)
                                program()
                            else:
                                messagebox.showerror(title="Hatalı Giriş", message="Kullanıcı Adınızı veya Şifrenizi Doğru Girdiğinizden Emin Olunuz.")

                        giris_b = t.Button(bsk, text="       Giriş       ", command=giris)

                        bgfoto.place(x=0, y=0)
                        giris_b.place(x=388, y=358)
                        sifre_e.place(x=345, y=300)
                        kadi_e.place(x=345, y=238)
                    else:
                        messagebox.showerror(title="Hata", message="Eksik giriş yapıldı. Tekrar deneyin.")
                baslangic_sifre_olustur_buton = t.Button(bsk, text="          Başlat          ", command=baslangic)

                ykadi_olustur_e.place(x=143, y=224)
                yksifre_olustur_e.place(x=143, y=270)

                nkadi_olustur_e.place(x=534, y=224)
                nksifre_olustur_e.place(x=534, y=270)

                baslangic_sifre_olustur_buton.place(x=362, y=319)

            tamam = t.Button(bsk, text="   Tamam   ", command=tamam_b)
            tamam.place(x=643, y=219)
        else:
            global girispng

            pencereler.add(bsk,text="""       Giriş       """)
            state2 = "disabled"
            girispng = ImageTk.PhotoImage(file="giris.png")
            bgfoto = Label(bsk, image=girispng)

            c.execute("SELECT * FROM sifre")
            con.commit()

            veri = c.fetchall()
            print(veri)
            kullanici_adlari = veri[0][0], veri[1][0]
            

            kadi_e = Entry(bsk, background="#DFDFDF", foreground="#343434", width=21, font="roboto 15", borderwidth=0, border=0, highlightthickness=0)
            sifre_e = Entry(bsk, background="#DFDFDF", foreground="#343434", width=21, font="roboto 15", borderwidth=0, border=0, highlightthickness=0)

            def giris():
                global state
                global state2
                global state3

                kadi = kadi_e.get().replace("('", "")
                kadi = kadi.replace("',)", "", 2)
                kadi = kadi.replace("{", "")
                kadi = kadi.replace("'}", "", 2)

                giris_anahtar, kullanici_id = sifre_kontrol(kadi, sifre_e.get())
                if giris_anahtar:
                    if kullanici_id == 1:
                        state="normal"
                        state2="normal"
                        state3="normal"
                    else:
                        state = "disabled"
                        state2 = "normal"
                        state3 = "disabled"
                    pencereler.forget(bsk)
                    program()
                else:
                    messagebox.showerror(title="Hatalı Giriş", message="Kullanıcı Adınızı veya Şifrenizi Doğru Girdiğinizden Emin Olunuz.")
            #giris_b = Button(bsk, text="      Giriş      ", command=giris, relief=RIDGE, background="#8E9AAF", fg="#000000")
            giris_b = t.Button(bsk, text="      Giriş      ", command=giris)
            bgfoto.place(x=0, y=0)
            giris_b.place(x=388, y=358)
            sifre_e.place(x=345, y=300)
            kadi_e.place(x=345, y=238)

    bas_sif_kont()
    ana.mainloop()
main()
