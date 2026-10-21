import unittest
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


if __name__ == "__main__":
    unittest.main()

