import requests
import xml.etree.ElementTree as ET
from urllib.parse import urljoin

class InpxWebBackend:
    def __init__(self, base_url="http://192.168.31.216:12380"):
        self.base_url = base_url
        self.ns = {"atom": "http://www.w3.org/2005/Atom"}

    def search(self, query):
        # 1. Поиск по названию
        url = f"{self.base_url}/opds/search?type=title&term={query}"
        r = requests.get(url)
        r.raise_for_status()
        root = ET.fromstring(r.text)

        results = []
        for entry in root.findall("atom:entry", self.ns):
            results.extend(self._parse_entry(entry))
        return results

    def _parse_entry(self, entry):
        """Разбираем один <entry> и сразу достаём acquisition-ссылки"""
        title = entry.find("atom:title", self.ns).text
        authors = entry.find("atom:content", self.ns)
        authors = authors.text if authors is not None else "Неизвестен"

        downloads = []
        for link in entry.findall("atom:link", self.ns):
            if "acquisition" in link.attrib.get("rel", ""):
                downloads.append({
                    "title": title,
                    "author": authors,
                    "format": link.attrib.get("type"),
                    "download": urljoin(self.base_url, link.attrib['href'])
                })
        return downloads
