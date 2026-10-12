#!/usr/bin/env python3
import csv
from datetime import datetime
import json
import re
from pathlib import Path
import subprocess
import sys


PROJECT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[4]
ENV_PATH = ROOT / ".env"
OUTPUT_PATH = PROJECT_DIR / "smart_glasses_reviews.csv"
TARGET_REVIEWS_PATH = PROJECT_DIR / "target_reviews_ego_lite.json"
COLLECTED_AT = "2026-10-02"
MAX_EXCERPT_CHARS = 220

SOURCES = {
    "Best Buy": {
        "url": "https://www.bestbuy.com/product/ray-ban-meta-wayfarer-gen-1-smart-ai-glasses-for-men-women-camera-audio-video-recording-green-lenses-shiny-black/BCKVZQ48PC#tabbed-customerreviews",
        "limit": 4,
    },
    "Walmart": {
        "url": "https://www.walmart.com/reviews/product/5272102656",
        "limit": 6,
    },
}

FIELDS = [
    "record_id",
    "product_name",
    "product_variant",
    "site_name",
    "rating",
    "rating_scale",
    "review_date",
    "review_date_raw",
    "review_title",
    "reviewer_name",
    "verified_purchase",
    "incentivized",
    "review_scope",
    "review_excerpt",
    "source_url",
    "collection_method",
    "collected_at",
]


def load_env_value(path: Path, name: str) -> str:
    if not path.is_file():
        return ""
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == name:
            return value.strip().strip("'\"")
    return ""


def scrape_markdown(api_key: str, url: str) -> str:
    payload = json.dumps(
        {
            "url": url,
            "formats": ["markdown"],
            "onlyMainContent": True,
            "maxAge": 86_400_000,
            "waitFor": 3000,
        }
    )
    curl_config = "\n".join(
        [
            "silent",
            "show-error",
            'url = "https://api.firecrawl.dev/v2/scrape"',
            'request = "POST"',
            f'header = "Authorization: Bearer {api_key}"',
            'header = "Content-Type: application/json"',
        ]
    )
    completed = subprocess.run(
        ["curl", "--config", "-", "--data-binary", payload],
        input=curl_config,
        capture_output=True,
        text=True,
        timeout=90,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"curl failed with exit {completed.returncode}")
    result = json.loads(completed.stdout)
    data = result.get("data") or {}
    metadata = data.get("metadata") or {}
    if not result.get("success") or metadata.get("statusCode") != 200:
        raise RuntimeError(
            f"Firecrawl scrape failed: status={metadata.get('statusCode')}"
        )
    return data.get("markdown") or ""


def clean_excerpt(value: str) -> str:
    value = re.sub(r"!\[[^]]*\]\([^)]*\)", "", value)
    value = re.sub(r"\s+", " ", value).strip()
    if len(value) <= MAX_EXCERPT_CHARS:
        return value
    shortened = value[: MAX_EXCERPT_CHARS + 1].rsplit(" ", 1)[0]
    return f"{shortened}…"


def parse_best_buy(markdown: str, url: str, limit: int) -> list[dict]:
    starts = [
        match.start()
        for match in re.finditer(r"- Rated [1-5] out of 5 stars", markdown)
    ]
    rows = []
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(markdown)
        block = markdown[start:end]
        rating_match = re.search(r"Rated ([1-5]) out of 5 stars", block)
        title_match = re.search(r"#### (.+)", block)
        posted_match = re.search(r"Posted (.+?) by ([^\n]+)", block)
        variant_match = re.search(r"This review is from \[([^]]+)\]", block)
        body_start = block.find("\n\n", (title_match.end() if title_match else 0))
        body_end = block.find("This review is from")
        body = block[body_start:body_end if body_end >= 0 else len(block)]
        body = re.sub(r"^\s*- (?:Incentivized|Verified Purchaser|My Best Buy® Member|Owned for [^\n]+)\s*$", "", body, flags=re.MULTILINE)
        excerpt = clean_excerpt(body)
        if not re.search(r"\b(glasses|meta|ray-ban|rayban)\b", excerpt, re.I):
            continue
        rows.append(
            {
                "product_name": "Ray-Ban Meta Wayfarer (Gen 1)",
                "product_variant": variant_match.group(1) if variant_match else None,
                "site_name": "Best Buy",
                "rating": int(rating_match.group(1)) if rating_match else None,
                "rating_scale": 5,
                "review_date": None,
                "review_date_raw": posted_match.group(1) if posted_match else None,
                "review_title": title_match.group(1).strip() if title_match else None,
                "reviewer_name": posted_match.group(2).strip() if posted_match else None,
                "verified_purchase": "Verified Purchaser" in block,
                "incentivized": "Incentivized" in block,
                "review_scope": "product",
                "review_excerpt": excerpt,
                "source_url": url,
                "collection_method": "Firecrawl v2 API",
                "collected_at": COLLECTED_AT,
            }
        )
        if len(rows) == limit:
            break
    return rows


def parse_walmart(markdown: str, url: str, limit: int) -> list[dict]:
    marker = re.search(r"Showing \d+-\d+ of [\d,]+ reviews", markdown)
    segment = markdown[marker.end() :] if marker else markdown
    blocks = re.split(r"\n\* \* \*\n", segment)
    rows = []
    for block in blocks:
        rating_match = re.search(r"([1-5]) out of 5 stars review", block)
        date_match = re.search(r"\b([A-Z][a-z]{2} \d{1,2}, \d{4})\b", block)
        reviewer_match = re.search(r"Reviewer name: ([^\n]+)", block)
        title_match = re.search(r"### (.+)", block)
        color_match = re.search(r"Color: ([^\n]+)", block)
        if not rating_match or not date_match:
            continue
        body_start = title_match.end() if title_match else rating_match.end()
        body_end_candidates = [
            point
            for point in (block.find("Read more", body_start), block.find("Helpful?", body_start))
            if point >= 0
        ]
        body_end = min(body_end_candidates) if body_end_candidates else len(block)
        excerpt = clean_excerpt(block[body_start:body_end])
        rows.append(
            {
                "product_name": "Ray-Ban Meta Wayfarer (Gen 1)",
                "product_variant": color_match.group(1).strip() if color_match else None,
                "site_name": "Walmart",
                "rating": int(rating_match.group(1)),
                "rating_scale": 5,
                "review_date": datetime.strptime(
                    date_match.group(1), "%b %d, %Y"
                ).date().isoformat(),
                "review_date_raw": date_match.group(1),
                "review_title": title_match.group(1).strip() if title_match else None,
                "reviewer_name": reviewer_match.group(1).strip() if reviewer_match else None,
                "verified_purchase": "Verified Purchase" in block,
                "incentivized": None,
                "review_scope": "product",
                "review_excerpt": excerpt,
                "source_url": url,
                "collection_method": "Firecrawl v2 API",
                "collected_at": COLLECTED_AT,
            }
        )
        if len(rows) == limit:
            break
    return rows


def load_target_rows() -> list[dict]:
    evidence = json.loads(TARGET_REVIEWS_PATH.read_text(encoding="utf-8"))
    rows = []
    for review in evidence["reviews"]:
        rows.append(
            {
                "product_name": evidence["product_name"],
                "product_variant": evidence["product_variant"],
                "site_name": evidence["source"],
                "rating": review["rating"],
                "rating_scale": evidence["aggregate_rating_scale"],
                "review_date": review["review_date"],
                "review_date_raw": review["review_date_raw"],
                "review_title": review["review_title"],
                "reviewer_name": review["reviewer_name"],
                "verified_purchase": review["verified_purchase"],
                "incentivized": None,
                "review_scope": review["review_scope"],
                "review_excerpt": review["review_excerpt"],
                "source_url": evidence["source_url"],
                "collection_method": evidence["collection_method"],
                "collected_at": evidence["collected_at"],
            }
        )
    return rows


def main() -> int:
    api_key = load_env_value(ENV_PATH, "FIRECRAWL_API_KEY")
    if not api_key:
        print("FIRECRAWL_API_KEY is missing from the repository root .env")
        return 2

    best_buy_markdown = scrape_markdown(api_key, SOURCES["Best Buy"]["url"])
    walmart_markdown = scrape_markdown(api_key, SOURCES["Walmart"]["url"])
    rows = parse_best_buy(
        best_buy_markdown, SOURCES["Best Buy"]["url"], SOURCES["Best Buy"]["limit"]
    )
    rows.extend(
        parse_walmart(
            walmart_markdown, SOURCES["Walmart"]["url"], SOURCES["Walmart"]["limit"]
        )
    )
    rows.extend(load_target_rows())

    for index, row in enumerate(rows, start=1):
        row["record_id"] = f"SGR-{index:03d}"

    with OUTPUT_PATH.open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    counts = {name: sum(row["site_name"] == name for row in rows) for name in SOURCES}
    counts["Target"] = sum(row["site_name"] == "Target" for row in rows)
    print(f"OUTPUT={OUTPUT_PATH}")
    print(f"ROWS={len(rows)}")
    print("SITE_COUNTS=" + json.dumps(counts, ensure_ascii=False, sort_keys=True))
    return 0 if len(rows) == 15 and all(counts.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
