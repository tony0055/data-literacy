import React from "react";
import { DataComponent, DataTable, EvidenceChart, ReportSection, RichNarrative, useDataApp } from "../../data-app-public.jsx";

const bar = { type: "horizontalBar", x: "label", y: "count", startAtZero: true, valueDecimals: 0, colors: { count: "#42658c" } };
const themes = { type: "horizontalStackedBar", x: "label", y: "긍정", fields: ["긍정", "문제", "혼합"], startAtZero: true, valueDecimals: 0, colors: { "긍정": "#42658c", "문제": "#b07c32", "혼합": "#90979f" } };

function Narrative({ id, queryId, text }) {
  const { snapshot, visible } = useDataApp();
  return visible(id) && <ReportSection id={id} title={text.split("\n")[0].replace(/^#+ /, "")} queryId={queryId} sourceRows={snapshot.queries[queryId].rows} showHeading={false}>
    <RichNarrative id={`${id}:body`} value={text} />
  </ReportSection>;
}

function Figure({ id, queryId, title, description, spec = bar, height = 300 }) {
  const { snapshot, visible } = useDataApp();
  const rows = snapshot.queries[queryId].rows;
  return visible(id) && <EvidenceChart id={id} queryId={queryId} title={title} description={description} spec={spec} rows={rows} sourceRows={rows} height={height} />;
}

function TableBlock({ id, queryId, title, columns, searchable = true }) {
  const { snapshot, visible } = useDataApp();
  const rows = snapshot.queries[queryId].rows;
  return visible(id) && <DataComponent id={id} queryId={queryId} kind="table" title={title} sourceRows={rows}>
    <DataTable rows={rows} columns={columns} rowKey="record_id" searchable={searchable} caption={title} />
  </DataComponent>;
}

export function ReportContent() {
  const { snapshot, canEdit, mode, appTitle, setAppTitle } = useDataApp();
  const s = snapshot.analysisSummary;
  return <article className="report-content" aria-label="스마트글래스 리뷰 탐색적 분석 보고서">
    <header className="report-hero">
      <h1 data-data-app-title contentEditable={canEdit && mode === "edit"} suppressContentEditableWarning onBlur={canEdit && mode === "edit" ? event => setAppTitle(event.currentTarget.textContent.trim() || appTitle) : undefined}>{appTitle}</h1>
      <RichNarrative id="eda-introduction" value="국내 사이트 한국어 리뷰 15건으로, 무엇을 만족스럽게 쓰고 어디에서 제약을 느끼는지 살펴봤다." className="report-deck" />
    </header>
    <Narrative id="eda-summary" queryId="reviews" text={`## 핵심 요약\n\n- 표본은 **4개 사이트·11개 상품명·15건**이다. 구매후기 6건과 개인 사용기 9건은 정보의 깊이와 평점 유무가 달라 분리해서 읽어야 한다.\n- 유효 평점 6건의 평균은 **93.3/100점**, 중앙값은 100점이다. 모두 다나와에 표시된 구매후기이며 전체 시장 만족도나 제품 순위를 뜻하지 않는다.\n- 수집 요약의 수동 코딩에서 **미디어 활용은 7건**, **착용·디자인과 AI·음성은 각각 6건**에 등장한다. AI·음성 6건 중 4건은 낮은 활용 빈도 또는 기능 제약을 포함했다.\n\n핸즈프리 기록·통화·영상 시청의 구체적인 효용이 관찰되지만, 오래 편하게 사용할 수 있는지와 AI가 실제 생활에 쓰이는지는 별도로 확인해야 한다.`} />
    <section className="report-section">
      <Narrative id="eda-sample-reading" queryId="reviews" text={`## 1. 어떤 표본을 모았는가\n\n게시일은 **${s.date_min}부터 ${s.date_max}까지**다. AI 카메라, AR 디스플레이, 오디오 안경이 섞여 있으며 사용 목적이 다르다. 상품명은 CSV 표기 기준 11개로, 세대·형태가 다른 모델을 합치지 않았다.\n\n다나와 6건(40.0%)과 클리앙 5건(33.3%)이 11건을 차지한다. 구매후기는 모두 다나와, 사용기는 나머지 사이트에 있어 **사이트 효과와 리뷰 유형 효과를 분리할 수 없다**. 사이트별 만족도 비교는 하지 않았다.`} />
      <Figure id="eda-sites" queryId="site_counts" title="사이트별 수집 리뷰 수" description="분모 15건 · 리뷰 행 기준 · 시장 점유율 아님" />
      <Figure id="eda-types" queryId="type_counts" title="구매후기 6건과 사용기 9건" description="분모 15건 · 구매후기에는 배송 경험도 포함" height={260} />
      <Figure id="eda-categories" queryId="category_counts" title="상품 유형별 리뷰 수" description="분모 15건 · CSV의 상호 배타적 상품 유형 구분" />
      <Figure id="eda-years" queryId="year_counts" title="게시 연도별 수집 리뷰 수" description="수집 표본의 연도 구성 · 판매·관심도의 추세가 아님" spec={{...bar, type:"bar"}} />
    </section>
    <section className="report-section">
      <Narrative id="eda-rating-reading" queryId="rating_counts" text={`## 2. 높은 평점은 제한된 구매후기에서만 관찰됐다\n\n유효 평점 6건은 100점 4건, 80점 2건이다. 평균 **${s.rating_mean.toFixed(1)}점**, 중앙값 **100점**, 범위 **80–100점**, 표본 표준편차 **${s.rating_sample_std.toFixed(1)}점**이다. 원문 100점 척도를 유지했고 빈 평점 9건은 0점으로 바꾸지 않았다.\n\nKR-001과 KR-003은 판매자·배송·포장 평가가 중심이다. 높은 점수가 착용감·AI·영상 품질 모두에 대한 만족을 뜻하지 않는다. 제품별 구매후기가 1–3건에 불과해 상품 우열이나 통계적 유의성을 검정하지 않았다.`} />
      <Figure id="eda-ratings" queryId="rating_counts" title="평점 분포: 80점 2건 · 100점 4건" description="다나와 구매후기 n=6 · 100점 척도 · 사용기 9건 제외" height={260} />
    </section>
    <section className="report-section">
      <Narrative id="eda-theme-reading" queryId="themes" text={`## 3. 미디어 활용의 만족과 AI·착용의 제약이 함께 나타난다\n\n**미디어 활용 7건**은 긍정 서술 6건, 혼합 1건이다. 혼합 사례 KR-015는 핸즈프리 가족 기록을 좋아하면서 실내 사진 품질을 아쉬워했다. 사진·영상 기록과 영상 시청의 구체적인 사용 상황을 확인할 수 있다.\n\n**착용·디자인 6건**은 긍정 2건, 문제 1건, 혼합 3건이다. 자연스러운 디자인과 장시간 불편·흘러내림·두꺼운 다리의 언급이 공존한다. 장시간 착용 경험을 별도로 수집하면 일상 사용의 한계를 더 분명히 확인할 수 있다.\n\n**AI·음성 6건**은 긍정 2건, 문제 3건, 혼합 1건이다. Rokid의 AI·음성인식 만족(KR-004·005)과 Meta 사용기의 낮은 사용 빈도·한국어 및 지역 지원 제약(KR-007·008·012·014)이 함께 있다. 모델·세대·게시 시점이 달라 브랜드 성능 차이라고 결론 내릴 수 없다.\n\n한 리뷰에 여러 주제를 붙였다. 합계는 15건을 넘으며 **“문제”는 부정 구매자 비율이 아니라 해당 주제의 서술 방향**이다. 원문 전문이 아닌 수집 발췌·요약을 코딩해 빠진 언급은 집계할 수 없다.`} />
      <Figure id="eda-themes" queryId="themes" title="주제별 언급 리뷰 수와 서술 방향" description="분모 전체 15건 · 다중 코딩 · 긍정/문제/혼합은 수동 판정" spec={themes} height={390} />
      <TableBlock id="eda-coding" queryId="coding" title="주제 분류를 행별 근거로 확인하기" columns={[{key:"record_id",label:"리뷰 ID"},{key:"theme",label:"주제"},{key:"direction",label:"서술 방향"},{key:"reason",label:"판정 근거"}]} />
    </section>
    <section className="report-section">
      <Narrative id="eda-quality-reading" queryId="quality" text={`## 4. 결측과 중복을 어떻게 처리했는가\n\n입력은 **15행·19열**, 출처 URL·작성자·게시일 조합의 중복은 **0건**이다. 평점과 척도는 각 9건(60.0%)이 비어 있고 모두 사용기에 해당한다. 평점 결측은 무작위 누락으로 가정하지 않았다. 제목 2건은 비어 있으나 발췌가 있어 제거하지 않았다.\n\n사이트·닉네임 조합은 14개지만 실제 고유 구매자 수를 뜻하지 않는다. 클리앙 오라질의 두 사용기는 같은 작성자의 다른 글이다. 제휴 고지를 확인한 글은 2건이고 나머지의 “미확인”은 제휴가 없다는 뜻이 아니다.`} />
      <TableBlock id="eda-quality" queryId="quality" title="분석 필드 결측 점검" columns={[{key:"field",label:"필드"},{key:"missing",label:"결측 건수"},{key:"total",label:"전체 건수"}]} searchable={false} />
    </section>
    <Narrative id="eda-conclusion" queryId="reviews" text={`## 5. 결론과 다음 수집 설계\n\n이 표본은 **기록·통화·시청의 활용 사례와 일상 착용·AI 활용의 제약을 탐색하는 데** 유용하다. “스마트글래스는 전반적으로 만족도가 높다”거나 “어느 브랜드가 더 좋다”는 주장은 이 자료로 뒷받침할 수 없다.\n\n후속 수집은 상품 유형과 모델·세대를 고정하고, 같은 기간의 긍정·중간·낮은 평가를 함께 확보하는 방식이 적절하다. 배송·판매자 경험과 기능 경험을 나누고, 사용 기간·한국어 AI 사용 여부·장시간 착용 상황을 기록하면 지금 관찰된 제약을 비교할 수 있다. 이는 추가 조사 설계 제안이며 실행한 결과가 아니다.`} />
    <section className="report-section">
      <Narrative id="eda-methods" queryId="reviews" text={`## 방법과 출처\n\n2026-10-02 저장한 CSV를 고정 입력으로 사용했다. 수집일과 게시일은 다르며 새 리뷰를 수집하지 않았다. UTF-8 BOM CSV를 읽고 빈 평점을 null로 보존했다. 평균·중앙값·표본 표준편차는 유효 평점 6건만으로 계산했다. 주제는 수집 요약에 근거한 수동 다중 분류이며 형태소 분석·자동 감성 모델·원문 전체 분석은 시행하지 않았다.\n\n국내 사이트의 한국어 리뷰이며 작성자의 국적·거주지·국내 구매를 확인한 것은 아니다. 오래된 글과 신제품 글을 같은 시점의 기능 평가로 읽어서는 안 된다. 수집 근거는 smart_glasses_review_evidence.json, 계산과 주제 사전은 build_review_eda.py, 집계 결과는 eda_summary.json에 기록했다.\n\n아래에서 원문 발췌와 수집자 요약을 구분하고 출처 링크를 열 수 있다. 표 검색은 해당 표에만 적용되며 위 차트의 전체 표본을 바꾸지 않는다.`} />
      <TableBlock id="eda-reviews" queryId="reviews" title="분석 원자료 15건과 원출처" columns={[
        {key:"record_id",label:"ID"},{key:"site_name",label:"사이트"},{key:"product_name",label:"상품"},
        {key:"review_type",label:"유형"},{key:"review_date",label:"게시일"},
        {key:"rating_raw",label:"평점 /100",renderCell:value=>value===null?"없음":value},
        {key:"review_excerpt",label:"원문 발췌"},{key:"summary_ko",label:"수집자 요약"},
        {key:"source_url",label:"원출처",renderCell:(value,row)=><a href={value} target="_blank" rel="noreferrer">{row.site_name} 원문</a>},
      ]} />
    </section>
  </article>;
}
