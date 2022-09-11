import pandas as pd

from utils import *

tumveriler = get_sheet()
tumveriler = pd.DataFrame(tumveriler, columns=range(0, 62))
ogrenci_numarasi = st.text_input('Öğrenci Numarası', 'b161306350')  # @param {type:"string"}


if st.button("Analiz Et"):
    ogrenci = tumveriler.loc[tumveriler[8] == ogrenci_numarasi]

    try:
        str(ogrenci[8].values[0]) != ogrenci_numarasi
    except IndexError:
        st.error("Öğrenci Numarasını bulunamadı, kontrol edip, programı tekrar çalıştırın ve öğrenci numarasını girin!")


    print("Öğrenci bulundu. Analiz ediliyor.")
    try:
        tanımla_analiz_et(ogrenci[8].values[0])
    except Exception as e:
        st.error("Tanım ve analiz kısmında bir hata oluştu --> " + str(e))


    print("Analiz bitti. Yazdırılıyor...")
    try:
        yazdir(ogrenci[8].values[0])
        yazdir_analiz(ogrenci[8].values[0])
    except Exception as e:
        st.error("Yazdırma sırasında bir hata oluştu --> " + str(e))


    print("Yazdırma bitti, mail olarak gönderiliyor..")
    ogr_ad = str(ogrenci[2].values[0])
    ogr_mail = str(ogrenci[1].values[0])
    try:
        mail_gonder(ogr_ad, ogr_mail)

    except Exception as e:
        st.error("Mail Gönderimi kısmında hata oluştu --> " + str(e))


