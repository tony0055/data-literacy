# Week 3 — 피마 인디언 당뇨병(Pima Indians Diabetes) 데이터 프로젝트

Kaggle 데이터셋 [`kumargh/pimaindiansdiabetescsv`](https://www.kaggle.com/datasets/kumargh/pimaindiansdiabetescsv)를 활용하여 0값 은폐 결측치 정제, 결측 보정에 따른 상관관계 왜곡 실증 분석, 인과 요인 시각화 및 당뇨 발병 예측 머신러닝 모델을 구축하는 프로젝트입니다.

---

## 1. 프로젝트 구조

```
school_project/week3/pima_indians/
├── README.md                          # 피마 인디언 프로젝트 분석 가이드 (본 문서)
└── scripts/
    ├── download_pima.py               # KaggleHub 데이터셋 다운로드
    ├── diagnose_data.py               # 0값 결측치·이상치 진단 및 시각화
    ├── data_diagnosis_result.png      # [시각화 1] 데이터 진단 대시보드
    ├── analyze_relationships.py       # 상관관계 왜곡 실증 및 인과 요인 시각화
    ├── relationship_analysis.png      # [시각화 2] 상관관계 및 인과 요인 대시보드
    ├── predict_model.py               # 당뇨 발병 예측 머신러닝 (로지스틱 회귀 & 랜덤포레스트)
    └── model_evaluation.png           # [시각화 3] 모델 성능 평가 및 임상 지표 영향력(오즈비) 대시보드
```

---

## 2. 데이터셋 내려받기

```python
import kagglehub

# Download latest version
path = kagglehub.dataset_download("kumargh/pimaindiansdiabetescsv")
print("Path to dataset files:", path)
```

```bash
python3 school_project/week3/pima_indians/scripts/download_pima.py
```

- 파일: `pima-indians-diabetes.csv` (768행 × 9열)
- 원본 CSV에 **헤더가 없으므로** 표준 9개 컬럼을 직접 지정해야 합니다.

---

## 3. 데이터 진단: 0으로 숨겨진 결측치

```bash
python3 school_project/week3/pima_indians/scripts/diagnose_data.py
```

- **도메인 지식 리터러시**: 포도당, 혈압, 피부두께, 인슐린, BMI가 0인 것은 생물학적으로 불가능하며, 결측치가 0으로 입력된 것입니다.
  - `Insulin` (인슐린): **48.70% (374건)** 결측
  - `SkinThickness` (피부두께): **29.56% (227건)** 결측
  - `BloodPressure` (혈압): **4.56% (35건)** 결측
  - `BMI`: **1.43% (11건)** 결측
  - `Glucose` (포도당): **0.65% (5건)** 결측
- **시각화 결과**: `scripts/data_diagnosis_result.png`

---

## 4. 데이터 시각화: 상관관계 왜곡 실증 및 인과 요인 분석

```bash
python3 school_project/week3/pima_indians/scripts/analyze_relationships.py
```

### 데이터 리터러시 핵심 분석 (상관관계 왜곡 실증 & 인과성)

#### ① 0값 결측 방치 시의 상관계수 왜곡 (수업 핵심 연계)
기계적으로 0을 방치한 채 상관계수를 구했을 때와, 도메인 지식을 반영해 0을 결측(NaN)으로 보정한 후 상관계수를 비교했습니다:

| 컬럼명 | 0 방치 시 상관계수 ($r$) | 결측(NaN) 보정 후 ($r$) | 차이 ($\Delta r$) | 통계적 왜곡 해석 |
| :--- | :---: | :---: | :---: | :--- |
| **`Insulin` (인슐린)** | **+0.1305** | **+0.3035** | **+0.1729** | **2.3배 급증!** 결측치 방치가 인슐린의 중요성을 은폐함 |
| **`SkinThickness` (피부두께)** | **+0.0748** | **+0.2595** | **+0.1847** | **3.5배 급증!** 0 방치 시 무관한 변수로 오판 위험 |
| **`BloodPressure` (혈압)** | **+0.0651** | **+0.1706** | **+0.1055** | **2.6배 급증!** |
| **`Glucose` (포도당)** | +0.4666 | **+0.4947** | +0.0281 | 가장 강력한 1위 양의 상관 |
| **`BMI` (체질량지수)** | +0.2927 | **+0.3137** | +0.0210 | 2위 양의 상관 |

#### ② 인과적 메커니즘 (Causal Drivers)
- **포도당(`Glucose`, $r = 0.495$)과 체질량지수(`BMI`, $r = 0.314$)**:
  - 당뇨(제2형)의 직접적 병리학적 원인(인슐린 저항성 및 췌장 베타세포 기능 저하).
- **연령(`Age`)과 임신 횟수(`Pregnancies`)의 교란 관계($r = 0.544$)**:
  - 나이가 많을수록 임신 횟수가 누적되므로, 임신 자체가 위험 요인인지 노화에 따른 신진대사 저하가 주원인인지 통제 변수 모델링이 필수적입니다.

- **시각화 대시보드 (`scripts/relationship_analysis.png`)**:
  - 패널 1: 0 방치 vs 결측 보정 후 Outcome 상관계수 변화 비교 막대 그래프
  - 패널 2: 결측 보정 후 전체 9개 변수 간 피어슨 상관계수 히트맵
  - 패널 3: 포도당 × BMI 2대 인과 요인 산점도 및 임상 위험 기준선(140 mg/dL, BMI 30)
  - 패널 4: 연령대별 당뇨 발병률 및 평균 임신 횟수 복합 추이

---

## 5. 당뇨 발병 예측 머신러닝 모델

```bash
python3 school_project/week3/pima_indians/scripts/predict_model.py
```

- **데이터 누수 방지(Data Leakage Prevention)**: Train 셋의 중앙값(Median)으로 Test 셋의 결측치를 대치하는 엄격한 머신러닝 파이프라인 적용.

### 모델 비교 (Test Set 평가)

| 모델 | 정확도 (Accuracy) | 정밀도 (Precision) | 재현율 (Recall) | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **로지스틱 회귀 (Logistic Regression)** | 70.78% | 60.00% | 50.00% | 0.5455 | **0.8130** |
| **랜덤 포레스트 (Random Forest)** | **74.03%** | **66.67%** | **51.85%** | **0.5833** | **0.8144** |

### 요인별 영향력 분석 (로지스틱 회귀 승산비 Odds Ratio)
1 표준편차 증가 시 당뇨 발병 승산비:
- **`Glucose` (포도당)**: **3.263배** 위험 증가 (압도적인 1위 발병 인자)
- **`BMI` (체질량지수)**: **1.991배** 위험 증가
- **`Pregnancies` (임신 횟수)**: **1.459배** 위험 증가
- **`DiabetesPedigreeFunction` (유전 가계도 점수)**: **1.263배** 위험 증가
- **`Age` (나이)**: **1.159배** 위험 증가

- **시각화 대시보드 (`scripts/model_evaluation.png`)**:
  - 패널 1: 로지스틱 회귀 vs 랜덤 포레스트 ROC 곡선 비교 (AUC 0.814)
  - 패널 2: 랜덤 포레스트 혼동 행렬 (Confusion Matrix)
  - 패널 3: 로지스틱 회귀 오즈비 (Odds Ratio) 막대 그래프
  - 패널 4: 랜덤 포레스트 특성 중요도 (Feature Importance)
