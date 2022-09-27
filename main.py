import streamlit as st
from utils import *

tumveriler = get_sheet()
ogrenci_numarasi = st.text_input('Öğrenci Numarası', 'b161306350')  # @param {type:"string"}


if st.button("Analiz Et"):
    my_bar = st.progress(0)
    ogrenci = tumveriler.loc[tumveriler[8] == ogrenci_numarasi]

    try:
        str(ogrenci[8].values[0]) != ogrenci_numarasi
        st.info("Öğrenci bulundu. Analiz ediliyor.")
        my_bar.progress(25)
        try:
            tanımla_analiz_et(ogrenci)
            st.info("Analiz bitti. Yazdırılıyor...")
            my_bar.progress(50)
            try:
                yazdir(ogrenci)
                yazdir_analiz(ogrenci)
                st.info("Yazdırma bitti, mail olarak gönderiliyor..")
                my_bar.progress(75)
                ogr_ad = str(ogrenci[2].values[0])
                ogr_mail = str(ogrenci[1].values[0])
                try:
                    # mail_gonder(ogr_ad, ogr_mail)
                    mail_gonder_yetkili(ogr_ad)
                except Exception as e:
                    st.error("Mail Gönderimi kısmında hata oluştu --> " + str(e))
                st.info("Tamamlandı!")
                my_bar.progress(100)
            except Exception as e:
                st.error("Yazdırma sırasında bir hata oluştu --> " + str(e))
        except Exception as e:
            st.error("Tanım ve analiz kısmında bir hata oluştu --> " + str(e))
    except IndexError:
        st.error("Öğrenci Numarasını bulunamadı, kontrol edip öğrenci numarasını tekrar girin!")
