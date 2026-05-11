import certifi
import urllib.request

CERT_URL = "https://gu-st.ru/content/lending/russian_trusted_root_ca_pem.crt"

cert_data = urllib.request.urlopen(CERT_URL).read()

with open(certifi.where(), "ab") as cert_file:
    cert_file.write(cert_data)

print("Russian trusted root certificate installed")