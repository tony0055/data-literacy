from collections import Counter
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from statistics import mean, median, stdev


BASE = Path(__file__).resolve().parent
THEMES = {
    "KR-001": {"배송·판매자": ("긍정", "판매자 응대 만족")},
    "KR-002": {"배송·판매자": ("문제", "배송 약 13일"), "디스플레이·구성품": ("문제", "교정 프레임·케이블 부재와 좁은 시야각")},
    "KR-003": {"배송·판매자": ("혼합", "대기는 있었지만 도착·포장 만족")},
    "KR-004": {"착용·디자인": ("긍정", "자연스러운 디자인과 착용감"), "미디어 활용": ("긍정", "카메라 활용 만족"), "AI·음성": ("긍정", "AI·번역 기능 만족")},
    "KR-005": {"AI·음성": ("긍정", "음성인식 만족")},
    "KR-006": {"미디어 활용": ("긍정", "동영상 용도로 활용")},
    "KR-007": {"오디오·통화": ("긍정", "음질 만족"), "착용·디자인": ("혼합", "착용감은 좋으나 흘러내림"), "미디어 활용": ("긍정", "사진 활용"), "AI·음성": ("문제", "AI 사용 빈도 낮음")},
    "KR-008": {"미디어 활용": ("긍정", "사진 품질"), "오디오·통화": ("긍정", "통화 품질"), "배터리·충전": ("긍정", "배터리 개선"), "AI·음성": ("문제", "게시 당시 한국어 AI 제약")},
    "KR-009": {"디스플레이·구성품": ("혼합", "화질 만족, 모니터 대체 한계"), "착용·디자인": ("문제", "장시간 착용 불편")},
    "KR-010": {"착용·디자인": ("혼합", "디자인·만듦새 만족, 큰 프레임·두꺼운 다리 언급")},
    "KR-011": {"착용·디자인": ("혼합", "착용감은 괜찮으나 두꺼운 다리"), "배터리·충전": ("문제", "충전선 쉽게 분리")},
    "KR-012": {"디스플레이·구성품": ("긍정", "디스플레이 미리보기"), "미디어 활용": ("긍정", "사진·영상 활용"), "AI·음성": ("혼합", "Live AI 만족, 지역별 지원 한계")},
    "KR-013": {"미디어 활용": ("긍정", "유튜브 활용과 낮은 발열")},
    "KR-014": {"착용·디자인": ("긍정", "착용감 개선"), "배터리·충전": ("긍정", "배터리 개선"), "AI·음성": ("문제", "AI 활용도 아쉬움")},
    "KR-015": {"미디어 활용": ("혼합", "핸즈프리 기록 만족, 실내 사진 아쉬움"), "오디오·통화": ("긍정", "예상보다 좋은 스피커")},
}


def main():
    parser = argparse.ArgumentParser(description="리뷰 CSV EDA와 수동 주제 코딩 집계")
    parser.add_argument("--sync-report", action="store_true", help="기존 보고서의 데이터 갱신; ID·제목 보존")
    args = parser.parse_args()
    path = BASE / "smart_glasses_reviews.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8-sig", newline="")))
    assert len(rows) == len(THEMES) and {row["record_id"] for row in rows} == set(THEMES)
    ratings = [float(row["rating_raw"]) for row in rows if row["rating_raw"]]
    dates = [row["review_date"] for row in rows]
    keys = [(row["source_url"], row["author"], row["review_date"]) for row in rows]
    for row in rows:
        row["rating_raw"] = float(row["rating_raw"]) if row["rating_raw"] else None
        row["rating_scale"] = float(row["rating_scale"]) if row["rating_scale"] else None
    source = {
        "label": "국내 스마트글래스 리뷰 CSV · 2026-10-02 수집 스냅샷",
        "files": ["smart_glasses_reviews.csv"],
        "executedAt": datetime.now(timezone.utc).isoformat(),
        "evidenceFlow": [
            {"title": "입력", "detail": "국내 4개 사이트 15건 CSV; 사용기 9건 Firecrawl API, 구매후기 6건 ego-lite. 원문 전문 대신 발췌·수집 요약 포함."},
            {"title": "변환", "detail": "UTF-8 BOM CSV 읽기. 빈 평점은 null. 날짜·고유키·결측 검사. 그룹별 행 수와 유효 평점만 집계."},
            {"title": "주제 코딩", "detail": "summary_ko와 발췌에 근거한 수동 다중 코딩. THEMES 사전의 행별 판정 근거 사용. 긍정·문제·혼합은 주제별 서술 방향이지 자동 감성 점수가 아님."},
        ],
        "caveats": ["편의표본; 시장 대표성·성장률·제품 우열·인과관계를 추정하지 않음", "제품과 게시 연도가 다르고 사이트와 리뷰 유형이 겹침", "닉네임은 식별자이며 실제 고유 구매자 수를 보장하지 않음"],
    }
    queries = {}

    def query(name, data, definition, component):
        queries[name] = {"rows": data, "source": {**source, "metricDefinitions": [{"label": name, "definition": definition, "componentIds": [component]}]}, "methods": [{"language": "text", "code": definition + " 재현: python3 build_review_eda.py"}]}

    def counts(field):
        return [{"label": k, "count": v} for k, v in Counter(row[field] for row in rows).most_common()]

    query("site_counts", counts("site_name"), "사이트별 리뷰 행 수; 분모 15건.", "eda-sites")
    query("category_counts", counts("product_category"), "CSV 상품 유형별 리뷰 행 수; 분모 15건.", "eda-categories")
    query("type_counts", counts("review_type"), "구매후기와 사용기 행 수; 분모 15건.", "eda-types")
    query("year_counts", [{"label": str(year), "count": sum(d.startswith(str(year)) for d in dates)} for year in range(2021, 2027)], "게시 연도별 수집 행 수; 0은 해당 연도 수집 행 없음이며 시장 활동 부재가 아님.", "eda-years")
    query("rating_counts", [{"label": "80점", "count": ratings.count(80)}, {"label": "100점", "count": ratings.count(100)}], "평점이 있는 구매후기 6건의 100점 척도 분포. 사용기 9건은 제외.", "eda-ratings")
    quality = []
    for field in ["rating_raw", "rating_scale", "review_title", "review_date", "source_url", "summary_ko"]:
        quality.append({"field": field, "missing": sum(row[field] in (None, "") for row in rows), "total": len(rows)})
    query("quality", quality, "필드별 빈 문자열 또는 null 행 수. 미확인 문자열은 결측과 별도로 기록.", "eda-quality")
    theme_rows = []
    code_rows = []
    for record_id, assignments in THEMES.items():
        for theme, (direction, reason) in assignments.items():
            code_rows.append({"record_id": record_id, "theme": theme, "direction": direction, "reason": reason})
    for theme, count in Counter(row["theme"] for row in code_rows).most_common():
        theme_rows.append({"label": theme, "count": count, **{direction: sum(row["theme"] == theme and row["direction"] == direction for row in code_rows) for direction in ["긍정", "문제", "혼합"]}})
    query("themes", theme_rows, "주제가 언급된 리뷰 수. 한 리뷰에 여러 주제가 가능하여 합계는 15를 넘음. 수집 요약 기반 수동 코딩.", "eda-themes")
    query("coding", code_rows, "행별 주제·서술 방향·수동 판정 근거. 원문 전체의 감성 분석이 아님.", "eda-coding")
    query("reviews", rows, "수집 리뷰 1건당 1행. 평균 평점 산출에서 null은 제외. 원문 발췌와 수집자의 요약을 구분.", "eda-reviews")
    summary = {
        "rows": len(rows), "columns": len(rows[0]), "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "sites": len(set(row["site_name"] for row in rows)), "products": len(set(row["product_name"] for row in rows)),
        "author_handles": len(set((row["site_name"], row["author"]) for row in rows)),
        "duplicate_records": len(keys) - len(set(keys)), "date_min": min(dates), "date_max": max(dates),
        "rating_n": len(ratings), "rating_missing": len(rows) - len(ratings),
        "rating_mean": mean(ratings), "rating_median": median(ratings), "rating_min": min(ratings), "rating_max": max(ratings), "rating_sample_std": stdev(ratings),
        "affiliate_disclosed_n": sum(row["affiliate_disclosed"].startswith("있음") for row in rows),
        "unknown_origin_n": sum(row["origin_site"] == "미확인" for row in rows),
    }
    snapshot = {"surface": "report", "title": "스마트글래스 리뷰: 활용의 만족과 일상 사용의 제약", "generatedAt": datetime.now(timezone.utc).isoformat(), "status": "reviewed", "buildStatus": "creating", "filters": [], "report": {"asOf": "2026-10-02"}, "queries": queries, "analysisSummary": summary}
    (BASE / "eda_snapshot.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (BASE / "eda_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.sync_report:
        report_path = BASE / "eda-report" / "src" / "data.json"
        previous = json.loads(report_path.read_text(encoding="utf-8"))
        snapshot.update({key: previous[key] for key in ["id", "title", "buildStatus"]})
        report_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (BASE / "review_theme_coding.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["record_id", "theme", "direction", "reason"])
        writer.writeheader()
        writer.writerows(code_rows)
    print(json.dumps({"summary": summary, "themes": theme_rows}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
