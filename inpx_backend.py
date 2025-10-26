import requests
import xml.etree.ElementTree as ET
from urllib.parse import urljoin

class InpxWebBackend:
    def __init__(self, base_url="http://192.168.31.216:12380"):
        self.base_url = base_url
        self.ns = {"atom": "http://www.w3.org/2005/Atom"}

    def search(self, query):
        url = f"{self.base_url}/opds/search?type=title&term={query}"
        r = requests.get(url)
        r.raise_for_status()
        root = ET.fromstring(r.text)

        results = []
        for entry in root.findall("atom:entry", self.ns):
            subsection = entry.find("atom:link", self.ns).attrib.get("href")
            results.extend(self._fetch_books(subsection))
        return results

    def _fetch_books(self, subsection_href):
        url = urljoin(self.base_url, subsection_href)
        r = requests.get(url)
        r.raise_for_status()
        root = ET.fromstring(r.text)

        books = []
        for entry in root.findall("atom:entry", self.ns):
            title = entry.find("atom:title", self.ns).text
            authors = entry.find("atom:content", self.ns)
            authors = authors.text if authors is not None else "Неизвестен"
            link = entry.find("atom:link", self.ns).attrib.get("href")
            books.extend(self._fetch_downloads(link, title, authors))
        return books

    def _fetch_downloads(self, book_href, title, authors):
        url = urljoin(self.base_url, book_href)
        r = requests.get(url)
        r.raise_for_status()
        root = ET.fromstring(r.text)

        downloads = []
        for entry in root.findall("atom:entry", self.ns):
            for link in entry.findall("atom:link", self.ns):
                if "acquisition" in link.attrib.get("rel", ""):
                    downloads.append({
                        "title": title,
                        "author": authors,
                        "format": link.attrib.get("type"),
                        "download": urljoin(self.base_url, link.attrib['href'])
                    })
        return downloads
