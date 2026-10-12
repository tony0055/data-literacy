from html import escape
import base64
import json
from pathlib import Path


BASE = Path(__file__).resolve().parent


def horizontal(rows, maximum, title, footer="", stacked=False):
    elements = []
    for index, row in enumerate(rows):
        label, count = row["label"], row["count"]
        width = count / maximum * 100
        if stacked:
            parts = []
            for name, kind in [("긍정", ""), ("문제", "problem"), ("혼합", "mixed")]:
                value = row[name]
                if value:
                    parts.append(f'<span class="segment {kind}" style="width:{value/count*100:.6f}%" aria-label="{name} {value}건">{value}</span>')
            mark = f'<div class="stack" style="width:{width:.6f}%;--delay:{100+index*60}ms">{"".join(parts)}</div>'
        else:
            mark = f'<div class="mark" style="width:{width:.6f}%;--delay:{100+index*60}ms"></div>'
        elements.append(f'<div class="bar-row"><span class="bar-label">{escape(label)}</span><div class="track">{mark}</div><span class="bar-value">{count}</span></div>')
    ticks = "".join(f"<span>{value:g}</span>" for value in [0, maximum/4, maximum/2, maximum*3/4, maximum])
    description = "; ".join(f'{row["label"]} {row["count"]}건' for row in rows)
    return f'<figure class="chart {"theme-chart" if stacked else ""}" style="margin:0" role="img" aria-label="{escape(title+": "+description)}"><div class="chart-heading">{escape(title)}</div>{"".join(elements)}<div class="axis">{ticks}</div><figcaption class="chart-foot">{escape(footer)}</figcaption></figure>'


def vertical(rows, title):
    maximum = max(row["count"] for row in rows)
    parts = []
    for index, row in enumerate(rows):
        parts.append(f'<div class="vgroup"><span class="vvalue">{row["count"]}</span><div class="vbar" style="height:{row["count"]/maximum*82:.6f}%;--delay:{100+index*60}ms"></div><span class="vlabel">{escape(row["label"])}</span></div>')
    return f'<figure class="chart" style="margin:0" role="img" aria-label="{escape(title)}"><div class="chart-heading">{escape(title)}</div><div class="vchart">{"".join(parts)}</div><figcaption class="chart-foot" style="margin-top:2.6cqw">各 연도의 수집 건수 · 2023년은 수집 행 없음</figcaption></figure>'.replace("各", "각")


def main():
    snapshot = json.loads((BASE.parent / "eda_snapshot.json").read_text(encoding="utf-8"))
    summary = snapshot["analysisSummary"]
    q = snapshot["queries"]
    assert summary["rows"] == 15 and summary["rating_n"] == 6
    assert len(q["reviews"]["rows"]) == 15
    slides = []
    notes = []

    def slide(section, title, content, note, source="고정 표본 n=15 · 2026-10-02 수집", dark=False, cover=False):
        number = len(slides) + 1
        classes = "slide" + (" dark" if dark else "")
        header = f'<header class="header a"><div class="kicker">{escape(section)}</div><h2>{title}</h2></header>' if not cover else ""
        footer = f'<footer class="footer"><span>{escape(source)}</span><span>SMART GLASSES / {number:02}</span></footer>'
        slides.append(f'<section class="{classes}" id="slide-{number}" data-notes="{escape(note, quote=True)}" aria-label="{number}번째 슬라이드">{header}{content}{footer}</section>')
        notes.append((title.replace("<br>", " "), note))

    slide("", "스마트글래스, 써보니 어땠을까?", '<div class="content split cover"><div><div class="kicker a">DATA LITERACY · WEEK 05</div><h1 class="a" style="--delay:60ms">스마트글래스,<br>써보니 어땠을까?</h1><p class="deck-subtitle a" style="--delay:120ms">국내 리뷰로 살펴본 활용의 만족과 일상 사용의 제약</p><div class="numbers a" style="--delay:180ms"><div><strong>15</strong><span>리뷰</span></div><div><strong>4</strong><span>국내 사이트</span></div><div><strong>11</strong><span>상품명</span></div></div></div><div class="glasses a" style="--delay:240ms" aria-label="스마트글래스 개념 도식"><div class="lens left"></div><div class="lens right"></div><div class="bridge"></div><div class="camera"></div><span class="diagram-label">CONCEPT DIAGRAM · 실제 제품 사진 아님</span></div></div>', "약 20초. 국내 한국어 리뷰 15건을 분석했습니다. 이번 발표의 질문은 실제로 무엇에 만족하고 어디서 제약을 느꼈는가입니다. 시장 전체나 제품 순위를 판단하는 분석은 아닙니다.", dark=True, cover=True)

    site_chart = horizontal(q["site_counts"]["rows"], 6, "사이트별 리뷰 수 (건)", "분모 15건 · 사이트 점유율이 아닌 수집 비중")
    slide("01 / SAMPLE", "국내 4개 사이트에서 모은 15건", f'<div class="content split"><div class="a"><div class="big">15<small> 건</small></div><p class="metric-caption">다나와와 클리앙이<br><strong>11건 / 15건</strong>을 차지한다.</p><div class="note">Firecrawl API 사용기 9건<br>ego-lite 구매후기 6건</div></div><div class="a" style="--delay:60ms">{site_chart}</div></div>', "약 25초. 다나와 6건, 클리앙 5건, 티스토리 3건, 네이버 블로그 1건입니다. 검색과 기본 노출에서 확보한 편의표본이므로 수집 비중을 시장 비중으로 해석하지 않았습니다.")

    dots = "".join(f'<span class="dot {"empty" if i>=6 else ""}" style="--delay:{i*50}ms">{"–" if i>=6 else "●"}</span>' for i in range(15))
    type_chart = horizontal(q["type_counts"]["rows"], 9, "리뷰 유형별 건수", "사용기는 다른 3개 사이트 · 구매후기는 모두 다나와")
    slide("02 / DATA QUALITY", "평점이 없는 9건은 0점이 아니다", f'<div class="content two"><div class="a"><div class="chart-heading">평점 보유 여부 · 리뷰 한 건당 한 칸</div><div class="matrix">{dots}</div><div class="matrix-caption"><strong>평점 있음 6건</strong> · 평점 없음 9건 (60%)</div><div class="note">평균은 유효 평점 6건으로만 계산.<br>고유키 중복 0건 · 실제 고유 구매자 수는 미확인.</div></div><div class="a" style="--delay:60ms">{type_chart}</div></div>', "약 30초. 파란 칸은 평점이 있는 구매후기 6건이고 회색 칸은 평점이 없는 사용기 9건입니다. 사용기라는 자료 형식 때문에 평점이 없으므로 0점으로 채우거나 무작위 결측으로 간주하지 않았습니다. 같은 작성자의 사용기 두 건도 있습니다.")

    categories = horizontal(q["category_counts"]["rows"], 5, "상품 유형별 리뷰 수 (건)")
    years = vertical(q["year_counts"]["rows"], "게시 연도별 수집 건수")
    slide("03 / COMPARABILITY", "서로 다른 제품과 시점이 섞여 있다", f'<div class="content two"><div class="a">{categories}</div><div class="a" style="--delay:60ms">{years}<div class="note warn" style="margin-top:2cqw">2021–2026년의 글을 함께 수집했다.<br>연도별 건수는 판매·관심도의 성장 추세가 아니다.</div></div></div>', "약 25초. 카메라형과 디스플레이형, 오디오형을 같은 기준으로 비교하기 어렵습니다. 게시 연도도 2021년부터 2026년까지 다릅니다. 이 차트는 표본 구성을 보여줄 뿐 관심도나 판매 추세를 뜻하지 않습니다.")

    ratings = horizontal(q["rating_counts"]["rows"], 4, "평점 분포 (건)", "다나와 구매후기 n=6 · 원문 100점 척도")
    slide("04 / RATINGS", "93.3점은 제한된 구매후기의 평균", f'<div class="content split"><div class="a"><div class="big">{summary["rating_mean"]:.1f}<small> /100</small></div><p class="metric-caption">평균 · 구매후기 n=6</p><div class="numbers"><div><strong>100</strong><span>중앙값</span></div><div><strong>80–100</strong><span>관찰 범위</span></div></div><div class="note warn">배송·포장 만족도도 포함되어 있다.<br><strong>전체 시장 만족도와 제품 순위는 아님.</strong></div></div><div class="a" style="--delay:60ms">{ratings}</div></div>', "약 30초. 평점 6건 중 100점이 4건, 80점이 2건으로 평균은 93.3점입니다. KR-001과 KR-003은 판매자와 배송·포장 평가가 중심입니다. 점수가 높더라도 모든 제품 기능에 대한 만족이나 전체 구매자의 만족도라고 볼 수 없습니다.", source="평점 보유 구매후기 n=6 · 사용기 9건 제외")

    theme_chart = horizontal(q["themes"]["rows"], 7, "주제별 언급 리뷰 수 (건)", "한 리뷰에 여러 주제 가능 · 합계는 15건을 넘음", stacked=True)
    legend = '<div class="legend"><span><i></i>긍정 서술</span><span><i class="problem"></i>문제 서술</span><span><i class="mixed"></i>혼합 서술</span></div>'
    slide("05 / THEMATIC ANALYSIS", "무엇에 만족하고, 무엇이 아쉬웠을까?", f'<div class="content a" style="max-width:78cqw">{legend}{theme_chart}</div>', "약 35초. 원문 전문이 아니라 수집 발췌와 요약을 읽고 수동으로 다중 주제 분류했습니다. 각 막대는 해당 주제를 언급한 리뷰 수이고 색은 주제별 서술 방향입니다. 미디어 7건, 착용·디자인과 AI·음성 각 6건입니다. 자동 감성 분석이나 부정 구매자 비율이 아닙니다.", source="수집 발췌·요약 기반 수동 다중 코딩 · 전체 n=15")

    focus_cards = []
    descriptions = {"미디어 활용": ("기록·시청의 구체적 효용", "핸즈프리 기록은 좋지만<br>실내 사진은 아쉽다는 혼합 사례.", "KR-015 · Ray-Ban Stories"), "착용·디자인": ("일상 사용에는 착용성이 중요", "자연스러운 외형과 함께<br>장시간 불편·흘러내림을 언급.", "KR-007·009·010·011"), "AI·음성": ("기능 존재와 실제 활용은 다름", "6건 중 4건에 낮은 활용 빈도<br>또는 한국어·지역 지원 제약 포함.", "KR-007·008·012·014")}
    for index, label in enumerate(descriptions):
        row = next(row for row in q["themes"]["rows"] if row["label"] == label)
        heading, description, ids = descriptions[label]
        parts = "".join(f'<span class="segment {kind}" style="width:{row[name]/row["count"]*100:.6f}%">{row[name]}</span>' for name, kind in [("긍정", ""), ("문제", "problem"), ("혼합", "mixed")] if row[name])
        focus_cards.append(f'<article class="focus-card a" style="--delay:{index*60}ms"><span class="pill">{label}</span><div class="focus-n">{row["count"]}<small> /15건</small></div><h3>{heading}</h3><div class="stack" role="img" aria-label="{label}: 긍정 {row["긍정"]}, 문제 {row["문제"]}, 혼합 {row["혼합"]}">{parts}</div><p>{description}</p><div class="source-pill">{ids}</div></article>')
    slide("06 / FINDINGS", "쓸모는 구체적이다. 제약도 구체적이다.", f'<div class="content">{legend}<div class="three">{"".join(focus_cards)}</div><div class="note" style="margin-top:1.5cqw">모델·세대·게시 시점이 달라 브랜드 성능 차이로 결론 내릴 수 없다.</div></div>', "약 35초. 핵심은 세 가지입니다. 미디어 활용은 사용 상황이 분명합니다. 착용감은 장기 사용의 제약이 될 수 있습니다. AI는 기능이 있다는 것과 실제 생활에서 자주 쓴다는 것이 다릅니다. 세 카드의 작은 막대는 각각 해당 주제의 언급 건수 내 구성으로 정규화돼 있어 길이를 비교하지 말고 표시된 숫자로 읽어야 합니다.", source="주제별 언급 건수의 서술 방향 구성 · 수동 분류")

    slide("07 / LIMITATIONS", "이 자료로 말할 수 없는 것", '<div class="content three"><article class="card a"><div class="outline-number">01</div><h3>시장 전체의 만족도</h3><p>15건의 편의표본.<br>낮은 평가를 균형 있게 모은 자료가 아니다.</p></article><article class="card a" style="--delay:60ms"><div class="outline-number">02</div><h3>브랜드·사이트 우열</h3><p>상품과 세대가 다르다.<br>사이트와 리뷰 유형도 서로 겹친다.</p></article><article class="card a" style="--delay:120ms"><div class="outline-number">03</div><h3>현재의 AI 지원 상태</h3><p>게시 시점의 경험이다.<br>오래된 글을 현재 기능으로 읽지 않는다.</p></article></div>', "약 25초. 15건이라는 작은 편의표본, 서로 다른 모델과 시점, 사이트와 리뷰 유형의 중첩이 분석 한계입니다. 따라서 시장 전체 만족도, 브랜드 우열, 현재 기능 지원을 말할 수 없습니다. 이 한계가 있어도 구체적인 활용 사례와 불편을 탐색하는 데는 의미가 있습니다.")

    slide("08 / TAKEAWAY", "", '<div class="content" style="display:flex;flex-direction:column;justify-content:center"><div class="kicker a">TAKEAWAY</div><h2 class="conclusion a" style="--delay:60ms">“쓸모가 있다”와<br>“매일 편하게 쓴다”는 다른 질문.</h2><div class="steps"><div class="a" style="--delay:120ms"><strong>활용 상황을 먼저 묻고</strong><p>기록·통화·시청을 구분한다.</p></div><div class="a" style="--delay:180ms"><strong>제품과 기간을 맞추고</strong><p>모델·세대·게시 기간을 고정한다.</p></div><div class="a" style="--delay:240ms"><strong>기능과 배송을 나눈다</strong><p>성능·착용·AI와 판매 경험을 분리한다.</p></div></div><p class="source-pill a" style="margin-top:2cqw;--delay:300ms"><a href="../smart_glasses_eda_report.html">상세 EDA 보고서</a> · <a href="../smart_glasses_reviews.csv">원자료 CSV</a> · <a href="../review_theme_coding.csv">주제 분류 근거</a></p></div>', "약 25초. 결론은 쓸모와 일상 사용을 별개의 질문으로 봐야 한다는 것입니다. 다음 수집에서는 모델과 기간을 맞추고, 사용 상황과 사용 기간을 물으며, 배송 평가를 기능 평가에서 분리해야 합니다. 이는 후속 조사 제안이고 현재 검증한 결과가 아닙니다.")

    assert len(slides) == 9
    template = (BASE / "deck-template.html").read_text(encoding="utf-8")
    data = {"summary": summary, "charts": {name: q[name]["rows"] for name in ["site_counts", "type_counts", "category_counts", "year_counts", "rating_counts", "themes"]}, "source": "smart_glasses_reviews.csv", "coding": "review_theme_coding.csv"}
    hero = base64.b64encode((BASE / "assets/smart-glasses-hero-v1.png").read_bytes()).decode("ascii")
    old = '<div class="glasses a" style="--delay:240ms" aria-label="스마트글래스 개념 도식"><div class="lens left"></div><div class="lens right"></div><div class="bridge"></div><div class="camera"></div><span class="diagram-label">CONCEPT DIAGRAM · 실제 제품 사진 아님</span></div>'
    slides[0] = slides[0].replace(old, f'<figure class="hero a" style="--delay:240ms"><img src="data:image/png;base64,{hero}" alt="검은 스마트글래스의 AI 생성 콘셉트 이미지"><figcaption>AI 생성 콘셉트 이미지 · 실제 제품 아님</figcaption></figure>')
    library = (BASE / "assets/anime-4.5.0.umd.min.js").read_text(encoding="utf-8")
    document = template.replace("{{SLIDES}}", "\n".join(slides)).replace("{{ANIME}}", library).replace("{{DATA}}", json.dumps(data, ensure_ascii=False).replace("<", "\\u003c"))
    (BASE / "index.html").write_text(document, encoding="utf-8")
    script = ["# 스마트글래스 리뷰 발표 대본", "", "총 9장 · 약 4분 10초. 슬라이드별 권장 시간을 포함한다.", ""]
    for index, (title, note) in enumerate(notes, 1):
        script.extend([f"## {index}. {title or '결론'}", "", note, ""])
    (BASE / "script.md").write_text("\n".join(script), encoding="utf-8")
    print(json.dumps({"html": str(BASE / "index.html"), "slides": len(slides), "charts": 10, "input_sha256": summary["source_sha256"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
