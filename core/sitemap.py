import threading

from bs4 import BeautifulSoup
from django.template.loader import get_template, render_to_string


class SiteMap:
    """
    Class for large sitemaps. Writes sitemap to file, use Django view to serve sitemap.
    Optional sitemap_path defines the path to the sitemap you are working with, defaults to sitemap.xml in web root.
    For wagtail pages, use add_page/remove_page to add/amend/remove relevant entry. Call from appropriate hooks.
    generate_sitemap_from_page will create a sitemap for the site the passed page is in. 
    """
    def __init__(self, sitemap_path="sitemap.xml"):
        self.sitemap_path = sitemap_path
        self.soup = None

    def _get_soup(self):
        """Read and parse sitemap xml"""
        with open(self.sitemap_path, "r") as file:
            self.soup = BeautifulSoup(file, "xml")

    def find_url_entry(self, location):
        """
        Look for <url> element with <loc> child that has value=location
        Return element if found or None
        """
        if not self.soup:
            self._get_soup()

        def match_loc(element):
            return element.name == "loc" and element.string.strip() == location

        match = self.soup.find(match_loc)
        return match.parent if match else None

    def add_url(self, location, lastmod, alternates=None, changefreq=None, priority=None):
        """
        Look for <url> element with <loc> child that has value=location
        Add <url> element with passed parameters if not found, otherwise amend existing element
        """
        url_entry = self.find_url_entry(location)
        if url_entry:
            url_entry.clear()
        else:
            url_entry = self.soup.new_tag("url")
            self.soup.urlset.insert(0, url_entry)

        # Populate the <url> element with the supplied values
        loc_tag = self.soup.new_tag("loc")
        loc_tag.string = location
        url_entry.append(loc_tag)

        lastmod_tag = self.soup.new_tag("lastmod")
        lastmod_tag.string = (
            lastmod if type(lastmod) == "str" else lastmod.date().isoformat()
        )
        url_entry.append(lastmod_tag)

        if alternates:
            for alternate in alternates:
                alternate_tag = self.soup.new_tag(
                    "xhtml:link", hreflang=alternate["hreflang"], href=alternate["href"]
                )
                url_entry.append(alternate_tag)

        if changefreq:
            changefreq_tag = self.soup.new_tag("changefreq")
            changefreq_tag.string = changefreq
            url_entry.append(changefreq_tag)

        if priority:
            priority_tag = self.soup.new_tag("priority")
            priority_tag.string = priority
            url_entry.append(priority_tag)

        self.save()

    def add_page(self, page, thread=True):
        """
        Add or ammend page entry using page get_sitemap_urls
        thread=True passes execution back immediately without waiting for completion
        """
        if thread:
            threading.Thread(
                target=self.add_url,
                kwargs=page.get_sitemap_urls()[0],
            ).start()
        else:
            self.add_url(**page.get_sitemap_urls()[0])

    def remove_url(self, location):
        """
        Remove <url> element that has <loc> value matching location
        """
        url_entry = self.find_url_entry(location)
        if url_entry:
            url_entry.extract()
            self.save()
            return True
        return False

    def remove_page(self, page, thread=True):
        """
        Remove page entry
        thread=True passes execution back immediately without waiting for completion
        """
        if thread:
            threading.Thread(target=self.remove_url, args=(page.full_url,)).start()
        else:
            self.remove_url(page.full_url)

    def save(self):
        """
        Save sitemap soup object to file
        """
        if self.soup:
            with open(self.sitemap_path, "w") as file:
                file.write(str(self.soup))

    def generate_sitemap_from_page(self, page):
        """
        Creates a new sitemap for the site that the passed page is on
        For multi-lingual, repeat for each of page.get_site().root_page.siblings
        """
        urlset = []
        home = page.get_site().root_page
        for child_page in (
            home.get_descendants(inclusive=True).defer_streamfields().live().public().specific()
        ):
            urlset.append(child_page.get_sitemap_urls()[0])
        try:
            urlset.remove([])
        except:
            pass

        template = get_template("sitemap.xml")
        sitemap_xml = render_to_string(template.origin.name, {"urlset": urlset})

        with open(self.sitemap_path, "w") as file:
            file.write(sitemap_xml)
