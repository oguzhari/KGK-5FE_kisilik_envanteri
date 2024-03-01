import streamlit as st
from utils import *
head()
tumveriler = get_sheet()
ogrenci_numarasi = st.text_input('Danışanın Öğrenci Numarası', 'b161306350', key='ogrenci_numarasi')  # @param {type:"string"}
# https://myaccount.google.com/lesssecureapps
st.caption("Envanteri dolduran son beş öğrenci")
son_ogrenciler = pd.DataFrame(tumveriler[[2, 8]].tail(5), columns=['Öğrenci Adı', 'Öğrenci Numarası'])
st.dataframe(son_ogrenciler, hide_index=True)
kopya = st.checkbox('Bir kopyasını danışana gönder.')
fuar_modu = st.checkbox('Fuar Modu')
st.warning("Bir kopyasını danışana gönder seçeneği seçildiğinde, danışanlara özel hazırlanmış özet bir versiyonu gönderir."
           "\nFuar modu seçildiğinde, öğrenciye tam analiz gönderilir ancak danışmana mail gönderilmez.")
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
                        mail_gonder_yetkili(ogr_ad)
                        mail_gonder(ogr_ad, ogr_mail)
                        st.success("Tamamlandı!")
                    elif fuar_modu:
                        mail_gonder_fuar(ogr_ad, ogr_mail)
                        st.success("Tamamlandı!")
                    else:
                        mail_gonder(ogr_ad, ogr_mail)
                        st.success("Tamamlandı!")
                except Exception as e:
                    if "Username and Password not" in str(e):
                        st.error('''
                        Mail gönderilmesi için bu linkten ayarlar "AÇIK" hale getirilmeli.
                        https://myaccount.google.com/lesssecureapps
                        ''')
                    else:
                        st.error("Mail Gönderimi kısmında hata oluştu. Hata: {}".format(e))
                my_bar.progress(100)
            except Exception as e:
                st.error("Yazdırma sırasında bir hata oluştu. Hata: {}".format(e))
        except Exception as e:
            st.error("Tanım ve analiz kısmında bir hata oluştu. Hata: {}".format(e))
    except IndexError:
        st.error("Öğrenci Numarasını bulunamadı, kontrol edip öğrenci numarasını tekrar girin!")

versiyon()
