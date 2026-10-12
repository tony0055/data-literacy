import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import date
import json
from pathlib import Path
import re
import subprocess


BASE = Path(__file__).resolve().parent
FIELDS = [
    "record_id", "product_name", "product_category", "site_name", "origin_site",
    "review_type", "rating_raw", "rating_scale", "review_date", "author",
    "review_title", "purchase_claim", "affiliate_disclosed", "review_excerpt",
    "summary_ko", "source_url", "collection_method", "collected_at", "note",
]


def normalize(value):
    return re.sub(r"\s+", "", value.replace("**", "").replace("\\", ""))


def check_source(row, key):
    config = "\n".join([
        "silent", "show-error", 'url = "https://api.firecrawl.dev/v2/scrape"',
        'request = "POST"', f'header = "Authorization: Bearer {key}"',
        'header = "Content-Type: application/json"',
    ])
    payload = json.dumps({"url": row["source_url"], "formats": ["markdown"], "maxAge": 86400000})
    result = subprocess.run(
        ["curl", "--config", "-", "--data-binary", payload],
        input=config, text=True, capture_output=True, timeout=90, check=True,
    )
    response = json.loads(result.stdout)
    data = response.get("data", {})
    found = normalize(row["review_excerpt"]) in normalize(data.get("markdown", ""))
    return {
        "source_url": row["source_url"], "method": row["collection_method"],
        "status_code": data.get("metadata", {}).get("statusCode"),
        "scrape_id": data.get("metadata", {}).get("scrapeId", ""),
        "excerpt_matched": found, "api_success": response.get("success", False),
    }


def main():
    parser = argparse.ArgumentParser(description="국내 한국어 리뷰 스냅샷을 UTF-8 BOM CSV로 변환")
    parser.add_argument("--verify-sources", action="store_true", help="Firecrawl API로 사용기 발췌 재확인 (크레딧 사용)")
    args = parser.parse_args()
    snapshot = json.loads((BASE / "smart_glasses_reviews_ko.json").read_text(encoding="utf-8"))
    rows = snapshot["reviews"]
    seen = set()
    for row in rows:
        identity = (row["source_url"], row["author"], row["review_date"])
        if identity in seen:
            raise ValueError(f"중복 리뷰: {identity}")
        seen.add(identity)
        if not re.search(r"[가-힣]", row["review_excerpt"]):
            raise ValueError("한국어 발췌가 없는 리뷰")
        date.fromisoformat(row["review_date"])
        if row["rating_raw"] != "" and not 0 <= row["rating_raw"] <= row["rating_scale"]:
            raise ValueError("원문 평점 범위 오류")
    evidence = {
        "collected_at": snapshot["collected_at"], "scope": snapshot["scope"],
        "review_count": len(rows), "sites": dict(Counter(row["site_name"] for row in rows)),
        "types": dict(Counter(row["review_type"] for row in rows)),
        "sources": [
            {"source_url": row["source_url"], "method": row["collection_method"],
             "initial_scrape_id": row.get("scrape_id", ""),
             "observed_date": snapshot["collected_at"]}
            for row in rows
        ],
        "limitations": [
            "편의표본이며 대표성 없음; 구매후기와 개인 사용기를 분리할 것",
            "다나와는 동적 쇼핑몰 리뷰 영역을 ego-lite로 직접 확인; 원 쇼핑몰 상세 페이지는 미확인",
            "사용기는 별점 없음; 구매 진술은 작성자 주장이고 구매 인증이 아님",
            "오라질 작성자 사용기 2건은 독립 구매자 2명으로 해석하지 말 것",
            "요약은 수집자 작성, 발췌는 원문 일부; 기능 지원은 게시 당시 경험",
        ],
        "excluded": [{"source_url": "https://prod.danawa.com/info/?pcode=13151421", "reason": "실제 쇼핑몰 리뷰 탭에 등록된 상품리뷰 없음"}],
    }
    evidence_path = BASE / "smart_glasses_review_evidence.json"
    if evidence_path.exists():
        previous = json.loads(evidence_path.read_text(encoding="utf-8"))
        if "api_excerpt_checks" in previous:
            evidence["api_excerpt_checks"] = previous["api_excerpt_checks"]
    if args.verify_sources:
        env_path = next(parent / ".env" for parent in BASE.parents if (parent / ".env").exists())
        key_line = next(line for line in env_path.read_text().splitlines() if line.startswith("FIRECRAWL_API_KEY="))
        key = key_line.split("=", 1)[1].strip().strip("\"'")
        api_rows = [row for row in rows if row["collection_method"] == "Firecrawl v2 API"]
        with ThreadPoolExecutor(max_workers=3) as pool:
            checks = list(pool.map(lambda row: check_source(row, key), api_rows))
        evidence["api_excerpt_checks"] = {"checked_at": date.today().isoformat(), "results": checks}
        evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if any(not check["excerpt_matched"] for check in checks):
            failed = [check["source_url"] for check in checks if not check["excerpt_matched"]]
            raise ValueError(f"발췌 재확인 실패: {failed}")
    output = BASE / "smart_glasses_reviews.csv"
    with output.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        for index, row in enumerate(rows, 1):
            writer.writerow({**row, "record_id": f"KR-{index:03d}", "collected_at": snapshot["collected_at"]})
    evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "rows": len(rows), "sites": evidence["sites"], "types": evidence["types"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
