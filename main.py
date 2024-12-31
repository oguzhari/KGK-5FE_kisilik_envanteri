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
ogrenci_numarasi = ogrenci_numarasi.lower()
mail_adresleri = st.text_input(
    "Analizi Talep Edenin Mail Adresi", "kariyer@sakarya.edu.tr", key="mail_adresleri"
)
info = """
Mail adreslerini virgülle ayırarak birden fazla adres girebilirsiniz.

Örneğin: 

adres1@sakarya.edu.tr, adres2@sakarya.edu.tr

Tek mail adresi girilmesi halinde sadece bir danışmana mail gönderilecektir.

adres1@sakarya.edu.tr
"""

st.info(info)
mail_listesi = [mail.strip() for mail in mail_adresleri.split(",")]
kopya = st.checkbox("Bir kopyasını danışana gönder.")
fuar_modu = st.checkbox("Fuar Modu")
st.warning(
    "Bir kopyasını danışana gönder seçeneği seçildiğinde, danışanlara özel hazırlanmış özet bir versiyonu gönderir."
    "\nFuar modu seçildiğinde, öğrenciye tam analiz gönderilir ancak danışmana mail gönderilmez."
)

st.error(
    "Yapay Zeka alt yapısı kullandığımız için analiz süresi uzun sürebilir. "
    "Lütfen hata almanız halinde ne yaptığınızı, hangi ayarlar ile yaptığınızı ve hata mesajını doğrudan "
    "oari@sakarya.edu.tr adresine iletin."
)
if st.button("Analiz Et"):
    my_bar = st.progress(0)
    ogrenci = tumveriler.loc[tumveriler[8] == ogrenci_numarasi]
    try:
        my_bar.progress(25)
        tanımla_analiz_et(ogrenci)
        my_bar.progress(50)
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
            elif fuar_modu:
                mail_gonder_fuar(ogr_ad, ogr_mail)
            else:
                for mail in mail_listesi:
                    mail_gonder_yetkili(ogr_ad, mail)
            st.success("Tamamlandı!")
        except Exception as e:
            if "Username and Password not" in str(e):
                st.error(
                    "Mail gönderilmesi için bu linkten ayarlar 'AÇIK' hale getirilmeli.\nhttps://myaccount.google.com/lesssecureapps"
                )
            else:
                st.error(f"Mail Gönderimi kısmında hata oluştu. Hata: {e}")
        my_bar.progress(100)
    except IndexError:
        st.error(
            "Öğrenci Numarasını bulunamadı, kontrol edip öğrenci numarasını tekrar girin!"
        )
    except Exception as e:
        st.error(f"Tanım ve analiz kısmında bir hata oluştu. Hata: {e}")


versiyon()
