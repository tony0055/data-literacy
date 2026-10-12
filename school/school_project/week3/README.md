# Week 3 — 데이터 수집, 정제, 상관·인과 분석 및 예측 모델 프로젝트

데이터리터러시의 이해 3주차 실습 종합 프로젝트 디렉터리입니다.  
Kaggle의 대표적인 2대 정형 데이터셋을 대상으로 **데이터 수집(`kagglehub`)**, **데이터 정제(결측치·이상치·0값 은폐 결측 진단)**, **상관관계 vs 인과관계 시각화**, 그리고 **머신러닝 예측 모델(로지스틱 회귀 & 랜덤 포레스트)**을 구축하였습니다.

---

## 📁 프로젝트 구성 요약

### 1. [🚢 타이타닉 생존자 데이터 프로젝트 (`titanic/`)](titanic/README.md)
- **데이터셋**: [`heptapod/titanic`](https://www.kaggle.com/datasets/heptapod/titanic) (1,309행 × 28열)
- **기본 EDA 종합 산출물**:
  - `basic_eda.py`: 데이터 수집·정제·대푯값 비교·시각화 일괄 실행 파이썬 스크립트
  - `basic_eda.ipynb`: 마크다운 해설 및 인라인 그래프가 포함된 주피터 노트북 대화형 분석 보고서
  - `basic_eda_dashboard.png`: 6분할 종합 EDA 대시보드
- **주요 파이프라인**:
  - `download_titanic.py`: kagglehub을 통한 데이터셋 다운로드
  - `diagnose_data.py`: 더미 열 정리 및 결측치/이상치 진단 대시보드 (`data_diagnosis_result.png`)
  - `analyze_relationships.py`: 성별("여성과 어린이 우선"), 객실등급/운임(교란 요인), 가족 규모의 생존 영향 시각화 (`relationship_analysis.png`)
  - `predict_model.py`: 로지스틱 회귀(오즈비 분석) 및 랜덤포레스트 생존 예측 모델 (`model_evaluation.png`, AUC 0.772)

---

### 2. [🩺 피마 인디언 당뇨병 데이터 프로젝트 (`pima_indians/`)](pima_indians/README.md)
- **데이터셋**: [`kumargh/pimaindiansdiabetescsv`](https://www.kaggle.com/datasets/kumargh/pimaindiansdiabetescsv) (768행 × 9열)
- **종합 보고서 산출물**:
  - `pima_indians_report.ipynb`: 마크다운 해설, 0값 결측 정제, 왜곡 실증, 인과 요인 및 예측 모델링 실행 결과가 모두 내장된 종합 주피터 노트북
  - `comprehensive_report.ipynb`: 동일 내용의 종합 주피터 노트북
- **주요 파이프라인**:
  - `download_pima.py`: kagglehub을 통한 데이터셋 다운로드
  - `diagnose_data.py`: 헤더 부재 대응 및 0으로 숨겨진 결측치(인슐린 48.7%, 피부두께 29.6%) 진단 (`data_diagnosis_result.png`)
  - `analyze_relationships.py`: 0값 결측 방치 시 통계 왜곡 실증($r = 0.13 \to 0.30$) 및 포도당/BMI 인과 요인 시각화 (`relationship_analysis.png`)
  - `predict_model.py`: 데이터 누수 방지 중앙값 대치 및 당뇨 발병 예측 모델 (`model_evaluation.png`, AUC 0.814, 포도당 오즈비 3.26배)

---

## 🗂 전체 디렉터리 및 산출물 트리

```
school_project/week3/
├── README.md                                  # Week 3 종합 안내 (본 문서)
├── titanic/                                   # 🚢 타이타닉 프로젝트
│   ├── README.md                              # 타이타닉 상세 분석 보고서
│   ├── basic_eda.py                           # [기본 EDA] 파이썬 일괄 실행 스크립트
│   ├── basic_eda.ipynb                        # [기본 EDA] 주피터 노트북 대화형 분석 보고서
│   ├── basic_eda_dashboard.png                # [기본 EDA] 6개 패널 종합 대시보드 시각화
│   └── scripts/
│       ├── basic_eda.py                       # [기본 EDA] 실행 스크립트
│       ├── download_titanic.py                # 1. 데이터 다운로드
│       ├── diagnose_data.py                   # 2. 결측치/이상치 진단
│       ├── data_diagnosis_result.png          #    - [시각화] 데이터 진단 대시보드
│       ├── analyze_relationships.py           # 3. 상관관계 & 인과/영향 분석
│       ├── relationship_analysis.png          #    - [시각화] 상관관계/인과 분석 대시보드
│       ├── predict_model.py                   # 4. 머신러닝 생존 예측 모델
│       └── model_evaluation.png               #    - [시각화] 모델 평가 및 오즈비 대시보드
└── pima_indians/                              # 🩺 피마 인디언 당뇨병 프로젝트
    ├── README.md                              # 피마 인디언 상세 분석 보고서
    ├── pima_indians_report.ipynb              # [종합 보고서] 주피터 노트북 대화형 분석 보고서
    ├── comprehensive_report.ipynb             # [종합 보고서] 주피터 노트북 대화형 분석 보고서
    └── scripts/
        ├── download_pima.py                   # 1. 데이터 다운로드
        ├── diagnose_data.py                   # 2. 0값 결측치/이상치 진단
        ├── data_diagnosis_result.png          #    - [시각화] 데이터 진단 대시보드
        ├── analyze_relationships.py           # 3. 상관관계 왜곡 실증 & 인과 분석
        ├── relationship_analysis.png          #    - [시각화] 상관관계 왜곡/인과 대시보드
        ├── predict_model.py                   # 4. 머신러닝 당뇨 예측 모델
        └── model_evaluation.png               #    - [시각화] 모델 평가 및 오즈비 대시보드
```
