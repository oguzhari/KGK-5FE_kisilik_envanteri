import streamlit as st
from utils import *
head()
tumveriler = get_sheet()
ogrenci_numarasi = st.text_input('Öğrenci Numarası', 'b161306350')  # @param {type:"string"}

kopya = st.checkbox('Bir kopyasını öğrenciye gönder.')
if st.button("Analiz Et"):
    my_bar = st.progress(0)
    ogrenci = tumveriler.loc[tumveriler[8] == ogrenci_numarasi]
    try:
        str(ogrenci[8].values[0]) != ogrenci_numarasi
        my_bar.progress(25)
        try:
            tanımla_analiz_et(ogrenci)
            my_bar.progress(50)
            try:
                yazdir(ogrenci)
                yazdir_analiz(ogrenci)
                my_bar.progress(75)
                ogr_ad = str(ogrenci[2].values[0])
                ogr_mail = str(ogrenci[1].values[0])
                try:
                    mail_gonder_yetkili(ogr_ad)
                    try:
                        st.success("Tamamlandı!")
                        if kopya:
                            mail_gonder(ogr_ad, ogr_mail)
                        # st.info("Öğrenciye mail gönderildi!")
                    except Exception as e:
                        st.error("Öğrenciye Mail Gönderilemedi. Hata: {}".format(e))
                except Exception as e:
                    st.error("Mail Gönderimi kısmında hata oluştu. Hata: {}".format(e))
                my_bar.progress(100)
            except Exception as e:
                st.error("Yazdırma sırasında bir hata oluştu. Hata: {}".format(e))
        except Exception as e:
            st.error("Tanım ve analiz kısmında bir hata oluştu. Hata: {}".format(e))
    except IndexError:
        st.error("Öğrenci Numarasını bulunamadı, kontrol edip öğrenci numarasını tekrar girin!")

versiyon()
