# Week 3 — 타이타닉(Titanic) 데이터 프로젝트

Kaggle 데이터셋 [`heptapod/titanic`](https://www.kaggle.com/datasets/heptapod/titanic)을 활용하여 데이터 정제(결측치·중복값·이상치 진단), 상관관계 및 인과/영향 분석 시각화, 생존 예측 머신러닝 모델을 구축하는 프로젝트입니다.

---

## 1. 프로젝트 구조

```
school_project/week3/titanic/
├── README.md                          # 타이타닉 프로젝트 분석 가이드 (본 문서)
├── basic_eda.py                       # [기본 EDA] 파이썬 일괄 실행 스크립트
├── basic_eda.ipynb                    # [기본 EDA] 주피터 노트북 대화형 분석 보고서
├── basic_eda_dashboard.png            # [기본 EDA] 6개 패널 종합 대시보드 시각화
└── scripts/
    ├── basic_eda.py                   # [기본 EDA] 스크립트 디렉터리 내 실행 파일
    ├── download_titanic.py            # KaggleHub 데이터셋 다운로드
    ├── diagnose_data.py               # 결측치·이상치 진단 및 시각화
    ├── data_diagnosis_result.png      # [시각화 1] 데이터 진단 대시보드
    ├── analyze_relationships.py       # 상관관계 및 인과/영향 분석 시각화
    ├── relationship_analysis.png      # [시각화 2] 상관관계 및 인과 요인 대시보드
    ├── predict_model.py               # 머신러닝 예측 모델링 (로지스틱 회귀 & 랜덤포레스트)
    └── model_evaluation.png           # [시각화 3] 모델 성능 평가 및 영향력(오즈비) 대시보드
```

---

## 2. 기본 EDA (탐색적 데이터 분석) 실행

데이터 수집부터 정제, 기술통계 대푯값 비교(평균 vs 중앙값의 함정), 단변량/이변량/다변량 시각화, 상관관계 분석까지 하나의 완결된 파이프라인으로 수행합니다.

### 2.1. 파이썬 스크립트 실행
```bash
python3 school_project/week3/titanic/basic_eda.py
# 또는
python3 school_project/week3/titanic/scripts/basic_eda.py
```
- 콘솔에 요약 보고서 출력 및 `basic_eda_dashboard.png`(6분할 대시보드) 자동 생성

### 2.2. 주피터 노트북 실행
```bash
jupyter notebook school_project/week3/titanic/basic_eda.ipynb
# 또는 VS Code / Cursor / JupyterLab에서 열기
```
- 마크다운 설명과 함께 단계별 코드 셀을 인터랙티브하게 실행하고 결과를 바로 인라인으로 확인 가능

---

## 3. 데이터셋 내려받기

```python
import kagglehub

# Download latest version
path = kagglehub.dataset_download("heptapod/titanic")
print("Path to dataset files:", path)
```

```bash
python3 school_project/week3/titanic/scripts/download_titanic.py
```

- 파일: `train_and_test2.csv` (1,309행 × 28열)
- 28개 열 중 **19개가 `zero` 더미 열**이므로 정제 시 제외합니다.

---

## 4. 데이터 진단 및 정제

```bash
python3 school_project/week3/titanic/scripts/diagnose_data.py
```

- **중복값**: 완전 중복 0건
- **결측치**: 탑승 항구(`Embarked`) 결측 2건 (최빈값으로 대치)
- **이상치(IQR)**: 운임(`Fare`) 171건(13.06%), 나이(`Age`) 101건(7.72%) 탐지
- **시각화 결과**: `scripts/data_diagnosis_result.png`

---

## 5. 데이터 시각화: 상관관계 및 인과/영향 분석

```bash
python3 school_project/week3/titanic/scripts/analyze_relationships.py
```

### 데이터 리터러시 관점의 핵심 분석 (상관관계 vs 인과관계)
1. **성별(`Sex`)의 강력한 인과적 영향 ($r = +0.404$, 카이제곱 $p = 5.69 \times 10^{-48}$)**:
   - 여성 생존율은 **50.0%**, 남성 생존율은 **12.9%**로 압도적 차이.
   - 이는 단순한 통계적 연관이 아니라 당시 구명보트 탑승 규범인 **"여성과 어린이 우선(Women and children first)"**이 작동한 직접적 **인과적 메커니즘(Causal Mechanism)**입니다.
2. **객실등급(`Pclass`)과 요금(`Fare`)의 교란 효과(Confounder)**:
   - 1등석 생존율(42.1%) > 2등석(31.4%) > 3등석(16.8%).
   - 운임(`Fare`)이 높아서 살아남은 것이 아니라, 고운임 승객이 이용하는 1등석 객실이 상부 갑판에 위치하여 구명보트에 빠르게 접근할 수 있었던 **물리적 환경 요인이 교란 요인**으로 작용했습니다.
3. **가족 규모(`FamilySize`)의 비선형 보호 효과**:
   - 나홀로 탑승자(생존율 약 19%)보다 적정 가족(2~4명, 생존율 35~45%)의 생존율이 더 높았으나, 5인 이상 대가족은 탈출 시 서로를 챙기느라 생존율이 급감하는 U자형 비선형 관계가 관측됩니다.

- **시각화 대시보드 (`scripts/relationship_analysis.png`)**:
  - 패널 1: 주요 변수 간 피어슨 상관계수 히트맵
  - 패널 2: 객실등급 × 성별 교차 생존율 막대 그래프
  - 패널 3: 나이 × 요금에 따른 생존자 분포 및 어린이 기준선 산점도
  - 패널 4: 가족 규모별 생존율 곡선

---

## 6. 생존 예측 머신러닝 모델

```bash
python3 school_project/week3/titanic/scripts/predict_model.py
```

### 모델 비교 (Test Set 평가)

| 모델 | 정확도 (Accuracy) | 정밀도 (Precision) | 재현율 (Recall) | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **로지스틱 회귀 (Logistic Regression)** | 75.19% | 53.06% | 38.24% | 0.4444 | **0.7662** |
| **랜덤 포레스트 (Random Forest)** | **77.10%** | **58.00%** | **42.65%** | **0.4915** | **0.7720** |

### 요인별 영향력 분석 (로지스틱 회귀 승산비 Odds Ratio)
- **`Sex` (여성)**: **2.455배** 생존 확률 증가 (가장 강력한 생존 드라이버)
- **`Pclass` (객실등급)**: **0.501배** (등급 숫자가 커질수록[3등석] 생존 승산 50% 급감)
- **`Age` (나이)**: **0.662배** (연령 증가 시 생존 승산 감소, 어린이 보호 효과)
- **`IsAlone` (단독 탑승)**: **0.755배** (혼자 탄 승객의 생존 승산 25% 감소)

- **시각화 대시보드 (`scripts/model_evaluation.png`)**:
  - 패널 1: 로지스틱 회귀 vs 랜덤 포레스트 ROC 곡선 비교
  - 패널 2: 랜덤 포레스트 혼동 행렬 (Confusion Matrix)
  - 패널 3: 로지스틱 회귀 오즈비(Odds Ratio) 막대 그래프
  - 패널 4: 랜덤 포레스트 특성 중요도(Feature Importance)
