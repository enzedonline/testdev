import random
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from .sitemap import SiteMap
from .views import SitemapView
import time

def generate_test_sitemap():
    base_url = "http://localhost:8000/"
    locs = [f"{base_url}page-{i}" for i in range(1, 10001)]

    with open("test_sitemap.xml", "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

        for loc in locs:
            lastmod = datetime.utcnow() - timedelta(days=random.randint(0, 365))
            lastmod_str = lastmod.strftime("%Y-%m-%d")
            f.write(f'  <url>\n')
            f.write(f'    <loc>{loc}</loc>\n')
            f.write(f'    <lastmod>{lastmod_str}</lastmod>\n')
            f.write(f'  </url>\n')

        f.write('</urlset>\n')

def test_add_page_no_thread(pg):
    start_time = time.time()
    SiteMap().add_page(pg, False)
    print(f"Elapsed time: {time.time() - start_time:.6f} seconds")

def test_add_page_with_thread(pg):
    start_time = time.time()
    SiteMap().add_page(pg)
    print(f"Elapsed time: {time.time() - start_time:.6f} seconds")

def test_remove_no_thread(pg):
    start_time = time.time()
    SiteMap().remove_page(pg, False)    
    print(f"Elapsed time: {time.time() - start_time:.6f} seconds")

def test_remove_with_thread(pg):
    start_time = time.time()
    SiteMap().remove_page(pg)    
    print(f"Elapsed time: {time.time() - start_time: 6f} seconds")

def test_sitemap_gen(pg):
    start_time = time.time()
    SiteMap().generate_sitemap_from_page(pg)
    print(f"Elapsed time: {time.time() - start_time:.6f} seconds")

def test_sitemap_view():
    start_time = time.time()
    SitemapView().get(None)
    print(f"Elapsed time: {time.time() - start_time:.6f} seconds")

def test_init_sitemap():
    start_time = time.time()
    sm = SiteMap()
    print(f"Elapsed time: {time.time() - start_time:.6f} seconds")

