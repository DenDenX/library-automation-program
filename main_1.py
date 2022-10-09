from email.mime import image
from mimetypes import common_types
from tkinter import *
from tkinter import messagebox
from tkinter import ttk as t
from time import *
from datetime import *
from sqlite3 import *
from modules_1 import *
from sv_ttk import *
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
       
    ayarpng = ImageTk.PhotoImage(file="ayarlar.png")
    ktpverpng = ImageTk.PhotoImage(file="kitap_ver.png")
    ogrktpes = ImageTk.PhotoImage(file="ogr_ekle_sil.png")
    baslangic = ImageTk.PhotoImage(file="baslangic.png")
    baslangic_sifre = ImageTk.PhotoImage(file="baslangic_sifre.png")
    kk = ImageTk.PhotoImage(file="kk.png")
      
    use_dark_theme()

    ana.iconbitmap("logo.ico")
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
        pencereler.add(g, state=state2, text="Verilecek Kitaplar\n")
        pencereler.add(k,state=state2, text="       Kitap Ver      \n")
        pencereler.add(ok,state=state2, text="""   Öğrenci/ Kitap
        İşlemleri""")
        pencereler.add(ogr_ktp_list,state=state2, text="""    Öğrenciler     
      Kitaplar""")
        pencereler.add(kz,state=state2, text="Kullanım Kılavuzu\n")
        pencereler.add(s, state=state3, text="     Ayarlar      \n")
       
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
            agac.column("kalan_gun", width=150)
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

            def kitap_ver_tk():
                try:
                    barkod = int(barkod_e.get())
                    no = int(no_e.get())
                    tarih = tarih_se.get()
                    message = messagebox.askyesno(title="Onayla?", message="Kitabın ödünç verildiğini onaylıyor musunuz?")
                    if message:
                        if kitap_ver(barkod, no, tarih):
                            agac.grid_forget()
                            agac_olustur()
                        else:
                            messagebox.showerror(title="Hata", message="İşlem Tamamlanamadı! Kitap veya öğrenci bulunamadı. Kitap önceden verilmiş olabilir.")
                except:
                    messagebox.showerror(title="Hata", message="Tekrar deneyin!")
                barkod_e.delete(0, END)
                no_e.delete(0, END)
                tarih_se.delete(0, END)

            resim1 = Label(k, image=ktpverpng)
            resim1.place(x=0, y=0)
            barkod_e = Entry(k,width=20)
            no_e = Entry(k, width=20)
            tarih_se = t.Spinbox(k, values=spinbox_tarih(), width=11)
            onay_b = Button(k, text="   Kitabı Ver   ", command=kitap_ver_tk, relief=RIDGE, background="#8E9AAF",  fg="#000000")
            barkod_e.place(x=194, y=137)
            no_e.place(x=194, y=190)
            tarih_se.place(x=194, y=239)
            onay_b.place(x=436, y=185)

        def ogrenciler_kitaplar_olustur():
            global agac_o
            global agac_k
            ogr_columns = ["ogr", "no"]
            ktp_columns = ["ktp", "barkod"]
            agac_o = t.Treeview(ogr_ktp_list, columns=ogr_columns, show="headings", height=17)
            agac_o.heading("ogr", text="Öğrenci")
            agac_o.heading("no", text="No")
            agac_o.grid(row=0, column=0, columnspan=3)
            agac_o.column("ogr", width=300)
            agac_o.column("no", width=140)
            agac_k = t.Treeview(ogr_ktp_list, columns=ktp_columns, show="headings", height=17)
            agac_k.heading("ktp", text="Kitap")
            agac_k.heading("barkod", text="Barkod")
            agac_k.grid(row=0,column=3, columnspan=3)
            agac_k.column("ktp", width=250)
            agac_k.column("barkod", width=200)

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

            label = Label(ogr_ktp_list, text="Dosya")
            label.grid(row=1, column=0)
            label2 = Label(ogr_ktp_list, text="Dosya")
            label2.grid(row=1, column=3)

            entry_o_xl = Entry(ogr_ktp_list, width=36)
            entry_k_xl = Entry(ogr_ktp_list, width=36)
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

            buton_o_xl = Button(ogr_ktp_list, text="İçeri Aktar", command=komut_o_xl, state=state, relief=RIDGE, background="#8E9AAF",  fg="#000000")
            buton_k_xl = Button(ogr_ktp_list, text="İçeri Aktar", command=komut_k_xl, state=state, relief=RIDGE, background="#8E9AAF",  fg="#000000")
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
            ogr_adi = Label(ok, text="Öğrenci:")
            ogr_adi_e = Entry(ok, width=24)
            ogr_no_e = Entry(ok, width=24)
            ogr_onay = Button(ok, text="        Ekle        ",activebackground="green", command=komut_ogr_1, state=state, relief=RIDGE, background="#8E9AAF",  fg="#000000")
            ogr_adi_e.place(x=155, y=104)
            ogr_no_e.place(x=155, y=162)
            ogr_onay.place(x=155, y=200)
            ogr_no_sil_e = Entry(ok, width=24)
            ogr_no_sil_e.place(x=155, y=269)
            ogr_sil_onay = Button(ok, text="         Sil         ",activebackground="red", command=komut_ogr_2, state=state, relief=RIDGE, background="#8E9AAF",  fg="#000000")
            ogr_sil_onay.place(x=155, y=310)
            ktp_adi_e = Entry(ok, width=24)
            ktp_no_e = Entry(ok, width=24)
            ktp_onay = Button(ok, text="        Ekle        ",activebackground="green", command=komut_ktp_1, state=state, relief=RIDGE, background="#8E9AAF",  fg="#000000")
            ktp_adi_e.place(x=576, y=106)
            ktp_no_e.place(x=576, y=164)
            ktp_onay.place(x=576, y=200)
            ktp_no_sil_e = Entry(ok, width=24)
            ktp_no_sil_e.place(x=576, y=270)
            ktp_sil_onay = Button(ok, text="         Sil         ",activebackground="red",command=komut_ktp_2, state=state, relief=RIDGE, background="#8E9AAF",  fg="#000000")
            ktp_sil_onay.place(x=576, y=310)

        def ayarlar_olustur():
            resim3 = Label(s, image=ayarpng).place(x=0, y=0)
            kullanici_adi_e = Entry(s, width=23)
            sifre_e = Entry(s, width=23)  

            def sifre_degistir_main():
                kadi = kullanici_adi_e.get()
                ksifre = sifre_e.get()

                sifre_degistir(kadi, ksifre)
                messagebox.showinfo(title="Tamamlandı", message="İşlem Tamamlandı")


            onay = Button(s, text="    Değiştir    ",command=sifre_degistir_main, relief=RIDGE, background="#8E9AAF",  fg="#000000")
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
            pencereler.add(bsk,text="""    Baslangıç    \n     """)
            bilgilendirme =Label(bsk,image=baslangic)
            bilgilendirme.place(x=0, y=0)

            def tamam_b():
                global baslangic
                bilgilendirme.config(image=baslangic_sifre)
                tamam.place_forget()

                
                ykadi_olustur_e = Entry(bsk)
                yksifre_olustur_e = Entry(bsk)
                nkadi_olustur_e = Entry(bsk)
                nksifre_olustur_e = Entry(bsk)

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
                        c.execute("SELECT kadi FROM sifre")
                        con.commit()

                        kullanici_adlari = c.fetchall()
            
                        pencereler.add(bsk,text="""    Baslangıç    \n     """)
                        state2 = "disabled"
                        girispng = ImageTk.PhotoImage(file="giris.png")
                        bgfoto = Label(bsk, image=girispng)
                        kadi_e_variable = StringVar()
                        kadi_e_variable.set(kullanici_adlari[1])
                        kadi_e = OptionMenu(bsk, kadi_e_variable, kullanici_adlari[1], kullanici_adlari[0])
                        kadi_e.config(width=15, anchor="w")
                        sifre_e = Entry(bsk)
                       
                        def giris():
                            global state
                            global state2
                            global state3
                            kadi = kadi_e_variable.get().replace("('", "")
                            kadi = kadi.replace("',)", "", 2)

                            giris_anahtar, kullanici_id = sifre_kontrol(kadi, sifre_e.get())
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

                        giris_b = Button(bsk, text="      Giriş      ", command=giris, relief=RIDGE, background="#8E9AAF",  fg="#000000")

                        bgfoto.place(x=0, y=0)
                        giris_b.place(x=230, y=266)
                        sifre_e.place(x=224, y=188)
                        kadi_e.place(x=224, y=153)           
                    else:
                        messagebox.showerror(title="Hata", message="Eksik giriş yapıldı. Tekrar deneyin.")
                baslangic_sifre_olustur_buton = Button(bsk, text="          Başlat          ", command=baslangic, relief=RIDGE, background="#8E9AAF",  fg="#000000")
                 
                ykadi_olustur_e.place(x=290, y=117)
                yksifre_olustur_e.place(x=290, y=149)
                                
                nkadi_olustur_e.place(x=290, y=210)
                nksifre_olustur_e.place(x=290, y=242)
                
                baslangic_sifre_olustur_buton.place(x=255, y=319)
          
            tamam = Button(bsk, text="   Tamam   ", command=tamam_b, relief=RIDGE, background="#8E9AAF",  fg="#000000")
            tamam.place(x=184, y=281)
        else:
            global girispng
            
            pencereler.add(bsk,text="""    Baslangıç    \n     """)
            state2 = "disabled"
            girispng = ImageTk.PhotoImage(file="giris.png")
            bgfoto = Label(bsk, image=girispng)

            c.execute("SELECT kadi FROM sifre")
            con.commit()

            kullanici_adlari = c.fetchall()
            kadi_e_variable = StringVar()
            kadi_e_variable.set(kullanici_adlari[1])
            kadi_e = OptionMenu(bsk, kadi_e_variable, kullanici_adlari[1], kullanici_adlari[0])
            kadi_e.config(width=15, anchor="w")
            sifre_e = Entry(bsk)
            
            def giris():
                global state
                global state2
                global state3
                kadi = kadi_e_variable.get().replace("('", "")
                kadi = kadi.replace("',)", "", 2)

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
            giris_b = Button(bsk, text="      Giriş      ", command=giris, relief=RIDGE, background="#8E9AAF", fg="#000000")

            bgfoto.place(x=0, y=0)
            giris_b.place(x=230, y=266)
            sifre_e.place(x=224, y=188)
            kadi_e.place(x=224, y=153)
   
    bas_sif_kont()
    ana.mainloop()
main()
