import asyncio
import logging
import socket
import requests
import subprocess
from geoip2.webservice import AsyncClient
import platform
import re


# GeoIP istemcisi için kimlik bilgileri
ACCOUNT_ID =  "your_account_id_here"  # GeoIP hesap ID'nizi buraya girin
LICENSE_KEY = "your_license_key_here"  # GeoIP lisans anahtarınızı buraya girin
HOST = "geolite.info"

async def get_ip_info(ip_address):
    """Verilen IP adresi hakkında GeoIP bilgisini alır."""
    async_client = AsyncClient(ACCOUNT_ID, LICENSE_KEY, host=HOST)
    try:
        response = await async_client.city(ip_address)
        country = response.country.name if response.country.name else "Bilinmiyor"
        city = response.city.name if response.city.name else "Bilinmiyor"
        isp = get_isp_info(ip_address)
        usage_type = get_usage_type(ip_address)
        reverse_dns = get_reverse_dns(ip_address)
        latency = get_icmp_ping(ip_address)

        info = (f"////IP: {ip_address} - Şehir: {city}, Ülke: {country}, ISP: {isp}, Kullanım Türü: {usage_type}, "
                f"Ters DNS: {reverse_dns}, TCP Ping: {latency} ms")
        logging.info(info)
        print(info)
    except Exception as e:
        logging.error(f"{ip_address} için GeoIP sorgusu başarısız: {e}")
    finally:
        await async_client.close()

def get_isp_info(ip_address):
    """Verilen IP için ISP bilgisini döndürür."""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5)
        data = response.json()
        return data.get("isp", "Bilinmiyor")
    except Exception as e:
        return f"Hata: {e}"

def get_reverse_dns(ip_address):
    """Ters DNS kaydını getirir."""
    try:
        return socket.gethostbyaddr(ip_address)[0]
    except (socket.herror, socket.gaierror):
        return "Yok"

def get_usage_type(ip_address):
    """Verilen IP adresinin kullanım türünü döndürür."""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=mobile,proxy,hosting,org", timeout=5)
        data = response.json()
        usage_types = []
        if data.get("mobile"):
            usage_types.append("Mobil")
        if data.get("proxy"):
            usage_types.append("Proxy/VPN")
        if data.get("hosting"):
            usage_types.append("Hosting")
        if data.get("org"):
            usage_types.append(f"Kuruluş: {data['org']}")
        return ", ".join(usage_types) if usage_types else "Bilinmiyor"
    except Exception as e:
        return f"Hata: {e}"

def get_icmp_ping(ip_address):
    """ICMP Ping ile gecikmeyi ölçer ve milisaniye cinsinden döndürür."""
    param = "-n" if platform.system().lower() == "windows" else "-c"  # Windows/Linux uyumlu
    try:
        result = subprocess.run(["ping", param, "1", ip_address], capture_output=True, text=True, timeout=3)
        if result.returncode == 0:
            if platform.system().lower() == "windows":
                match = re.search(r"M?inimum = (\d+)ms", result.stdout)
            else:
                match = re.search(r"time=(\d+\.?\d*) ms", result.stdout)
            
            if match:
                return float(match.group(1))  # Milisaniye cinsinden süre
            else:
                return "Gecikme bilgisi alınamadı"
        else:
            return "Ping başarısız"
    except Exception:
        return "Ping hatası"








async def honeypot_ip_checker(ip_list):
    """Honeypot sistemine düşen IP'leri kontrol eder."""
    tasks = [get_ip_info(ip) for ip in ip_list]
    await asyncio.gather(*tasks)

def load_suspicious_ips(file_path):
    """Şüpheli IP'leri belirtilen dosyadan yükler."""
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        logging.error(f"Dosya bulunamadı: {file_path}")
        return []

# Test amaçlı şüpheli IP'leri dosyadan al
if __name__ == "__main__":
    suspicious_ips = load_suspicious_ips("suspicious_ips.txt")
    if suspicious_ips:
        asyncio.run(honeypot_ip_checker(suspicious_ips))
