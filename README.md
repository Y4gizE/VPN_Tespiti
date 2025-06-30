# Honeypot IP Analiz Aracı

Bu proje, honeypot sistemine düşen şüpheli IP adreslerini analiz eden ve bu IP'lerle ilgili detaylı bilgi (lokasyon, ISP, kullanım türü, ters DNS, ping süresi vb.) sağlayan asenkron bir Python uygulamasıdır.

---

## Özellikler

- Asenkron olarak çok sayıda IP adresinin GeoIP bilgilerini toplar.
- IP'nin şehir ve ülke bilgilerini MaxMind GeoIP servisi üzerinden sorgular.
- IP'nin internet servis sağlayıcısını (ISP) ve kullanım türünü (mobil, proxy/VPN, hosting, kuruluş) ip-api.com üzerinden alır.
- IP için ters DNS (reverse DNS) sorgusu yapar.
- IP'ye ICMP ping atarak gecikme süresini ölçer.
- Şüpheli IP listesi dosyasından okunarak toplu analiz yapılabilir.

---

## Gereksinimler

- Python 3.8 ve üzeri
- Aşağıdaki Python kütüphaneleri:
  - `asyncio`
  - `logging`
  - `socket`
  - `requests`
  - `geoip2`
  - `platform`
  - `re`
  - `subprocess`

---

Aşağıdaki site üzerinden Lisans anahtarı ve kullanıcı ID'nizi elde edebilirsiniz.
https://www.maxmind.com/en/home
