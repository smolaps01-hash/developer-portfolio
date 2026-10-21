import unittest
import json
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AssetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.assets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "link" and values.get("href"):
            self.assets.append(values["href"])
        if tag == "script" and values.get("src"):
            self.assets.append(values["src"])


class LandingTests(unittest.TestCase):
    def test_local_assets_exist(self) -> None:
        for directory in ("landing", "docs"):
            html = ROOT.joinpath(directory, "index.html").read_text(encoding="utf-8")
            parser = AssetParser()
            parser.feed(html)
            for asset in parser.assets:
                if not asset.startswith(("http://", "https://", "//")):
                    self.assertTrue(ROOT.joinpath(directory, asset).is_file(), asset)

    def test_form_has_accessible_status(self) -> None:
        html = ROOT.joinpath("landing", "index.html").read_text(encoding="utf-8")
        self.assertIn('role="status"', html)
        self.assertIn('aria-live="polite"', html)

    def test_pages_has_mobile_viewport(self) -> None:
        html = ROOT.joinpath("docs", "index.html").read_text(encoding="utf-8")
        self.assertIn('name="viewport"', html)

    def test_pages_has_canonical_and_social_metadata(self) -> None:
        html = ROOT.joinpath("docs", "index.html").read_text(encoding="utf-8")
        self.assertIn('rel="canonical"', html)
        self.assertIn('property="og:title"', html)
        self.assertIn('name="twitter:card"', html)

    def test_pages_has_valid_person_structured_data(self) -> None:
        html = ROOT.joinpath("docs", "index.html").read_text(encoding="utf-8")
        marker = '<script type="application/ld+json">'
        payload = html.split(marker, 1)[1].split("</script>", 1)[0]
        data = json.loads(payload)
        self.assertEqual(data["@type"], "Person")
        self.assertIn("https://github.com/smolaps01-hash", data["sameAs"])

    def test_pages_brief_builder_is_accessible(self) -> None:
        html = ROOT.joinpath("docs", "index.html").read_text(encoding="utf-8")
        self.assertIn('for="current-state"', html)
        self.assertIn('for="desired-result"', html)
        self.assertIn('role="status"', html)
        self.assertIn('aria-live="polite"', html)

    def test_pages_has_visible_keyboard_focus(self) -> None:
        css = ROOT.joinpath("docs", "styles.css").read_text(encoding="utf-8")
        self.assertIn(":focus-visible", css)
        self.assertIn("outline:", css)

    def test_pages_has_search_discovery_files(self) -> None:
        self.assertTrue(ROOT.joinpath("docs", "robots.txt").is_file())
        sitemap = ROOT.joinpath("docs", "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("https://smolaps01-hash.github.io/developer-portfolio/", sitemap)


if __name__ == "__main__":
    unittest.main()

