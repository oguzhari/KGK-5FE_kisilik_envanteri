import streamlit as st

# test
from utils import *

head()
tumveriler = get_sheet()
# https://myaccount.google.com/lesssecureapps
st.caption("Envanteri dolduran son beş öğrenci")
son_ogrenciler = pd.DataFrame(
    {
        "Envanter Doldurulma Tarihi": tumveriler[0],
        "Öğrenci Adı": tumveriler[2],
        "Öğrenci Numarası": tumveriler[8],
    }
)
st.dataframe(son_ogrenciler.tail(5), hide_index=True, width=700)
ogrenci_numarasi = st.text_input(
    "Danışanın Öğrenci Numarası", "b161306350", key="ogrenci_numarasi"
)
mail_adresleri = st.text_input(
    "Mail Adresleri", "kariyer@sakarya.edu.tr", key="mail_adresleri"
)
info = """
Mail adreslerini virgülle ayırarak birden fazla adres girebilirsiniz.
Örneğin: 

adres1@example.com, adres2@example.com

Tek mail adresi girilmesi halinde sadece bir danışana mail gönderilecektir.
"""

st.info(info)
mail_listesi = [mail.strip() for mail in mail_adresleri.split(",")]
kopya = st.checkbox("Bir kopyasını danışana gönder.")
fuar_modu = st.checkbox("Fuar Modu")
st.warning(
    "Bir kopyasını danışana gönder seçeneği seçildiğinde, danışanlara özel hazırlanmış özet bir versiyonu gönderir."
    "\nFuar modu seçildiğinde, öğrenciye tam analiz gönderilir ancak danışmana mail gönderilmez."
)
if st.button("Analiz Et"):
    my_bar = st.progress(0)
    ogrenci = tumveriler.loc[tumveriler[8] == ogrenci_numarasi]
    try:
        my_bar.progress(25)
        try:
            tanımla_analiz_et(ogrenci)
            my_bar.progress(50)
            try:
                danisman_analiz_olustur(ogrenci)
                ogrenci_analiz_olustur(ogrenci)
                my_bar.progress(75)
                ogr_ad = str(ogrenci[2].values[0]).title()
                ogr_mail = str(ogrenci[1].values[0])
                try:
                    if kopya:
                        for mail in mail_listesi:
                            mail_gonder_yetkili(ogr_ad, mail)
                        mail_gonder(ogr_ad, ogr_mail)
                        st.success("Tamamlandı!")
                    elif fuar_modu:
                        mail_gonder_fuar(ogr_ad, ogr_mail)
                        st.success("Tamamlandı!")
                    else:
                        for mail in mail_listesi:
                            mail_gonder_yetkili(ogr_ad, mail)
                        st.success("Tamamlandı!")
                except Exception as e:
                    if "Username and Password not" in str(e):
                        st.error(
                            """
                        Mail gönderilmesi için bu linkten ayarlar "AÇIK" hale getirilmeli.
                        https://myaccount.google.com/lesssecureapps
                        """
                        )
                    else:
                        st.error(
                            "Mail Gönderimi kısmında hata oluştu. Hata: {}".format(e)
                        )
                my_bar.progress(100)
            except Exception as e:
                st.error("Yazdırma sırasında bir hata oluştu. Hata: {}".format(e))
        except Exception as e:
            st.error("Tanım ve analiz kısmında bir hata oluştu. Hata: {}".format(e))
    except IndexError:
        st.error(
            "Öğrenci Numarasını bulunamadı, kontrol edip öğrenci numarasını tekrar girin!"
        )

versiyon()
