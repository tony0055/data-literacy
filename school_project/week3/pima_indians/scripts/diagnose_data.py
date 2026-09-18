"""피마 인디언 당뇨병(Pima Indians Diabetes) 데이터 정제 및 진단 스크립트.

이 스크립트는 원본 데이터를 훼손하지 않고(AI 함정 방지),
결측치(특히 0으로 은폐된 결측치), 중복값, 이상치(IQR)를 객관적으로 검증하고 시각화합니다.
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# ---------------------------------------------------------
# 0. 한글 폰트 및 시각화 스타일 설정 (macOS AppleGothic)
# ---------------------------------------------------------
plt.rc("font", family="AppleGothic")
plt.rcParams["axes.unicode_minus"] = False  # 마이너스 부호 깨짐 방지
sns.set_theme(style="whitegrid", font="AppleGothic")

DATASET_NAME = "kumargh/pimaindiansdiabetescsv"
CSV_FILENAME = "pima-indians-diabetes.csv"

# 피마 인디언 데이터셋의 표준 9개 컬럼명 (원문 CSV에는 헤더가 없음)
COLUMNS = [
    "Pregnancies",  # 임신 횟수
    "Glucose",  # 경구 포도당 내성 검사 2시간 혈장 포도당 농도 (mg/dL)
    "BloodPressure",  # 이완기 혈압 (mm Hg)
    "SkinThickness",  # 삼두근 피부 주름 두께 (mm)
    "Insulin",  # 2시간 혈청 인슐린 (mu U/ml)
    "BMI",  # 체질량 지수 (weight in kg/(height in m)^2)
    "DiabetesPedigreeFunction",  # 당뇨병 혈통 가계도 점수
    "Age",  # 나이 (세)
    "Outcome",  # 당뇨 발병 여부 (0: 정상, 1: 당뇨)
]

# 생물학적으로 0이 될 수 없어 0이 결측치(Missing Value)로 사용된 컬럼 목록
ZERO_AS_MISSING = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]


def load_pima_dataset() -> pd.DataFrame:
    """피마 인디언 데이터셋을 로드하고 표준 컬럼명을 부여합니다."""
    cache_path = os.path.expanduser(
        f"~/.cache/kagglehub/datasets/{DATASET_NAME}/versions/1/{CSV_FILENAME}"
    )
    if not os.path.exists(cache_path):
        import kagglehub

        download_path = kagglehub.dataset_download(DATASET_NAME)
        cache_path = os.path.join(download_path, CSV_FILENAME)

    df = pd.read_csv(cache_path, header=None, names=COLUMNS)
    return df


def diagnose_duplicates(df: pd.DataFrame) -> dict:
    """1. 중복값 검증"""
    print("\n" + "=" * 55)
    print(" [1] 중복값(Duplicate) 검증")
    print("=" * 55)

    total_rows = len(df)
    duplicate_rows = int(df.duplicated().sum())
    duplicate_ratio = (duplicate_rows / total_rows) * 100

    print(f"- 전체 데이터 행 수: {total_rows:,}개")
    print(f"- 완전히 일치하는 중복 행 수: {duplicate_rows:,}개 ({duplicate_ratio:.2f}%)")

    return {
        "total_rows": total_rows,
        "duplicate_rows": duplicate_rows,
        "duplicate_ratio": duplicate_ratio,
    }


def diagnose_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """2. 결측치 검증 (표면적 NaN 및 0으로 숨겨진 결측치 진단)"""
    print("\n" + "=" * 55)
    print(" [2] 결측치(Missing Values) 진단: 0값 은폐 결측치 분석")
    print("=" * 55)

    total_rows = len(df)
    records = []

    for col in df.columns:
        surface_na = int(df[col].isna().sum())
        is_zero_missing_candidate = col in ZERO_AS_MISSING
        zero_count = int((df[col] == 0).sum()) if is_zero_missing_candidate else 0
        effective_na = surface_na + zero_count
        effective_ratio = (effective_na / total_rows) * 100

        records.append(
            {
                "컬럼명": col,
                "자료형": str(df[col].dtype),
                "표면 결측(NaN)": surface_na,
                "0값 결측치": zero_count if is_zero_missing_candidate else "-",
                "실질 결측 합계": effective_na,
                "실질 결측 비율(%)": round(effective_ratio, 2),
            }
        )

    summary_df = pd.DataFrame(records).set_index("컬럼명")
    print(summary_df.to_string())

    print("\n  >> [도메인 지식 리터러시]")
    print("     Glucose(포도당), BloodPressure(혈압), SkinThickness(피부두께),")
    print("     Insulin(인슐린), BMI 수치가 0인 것은 생물학적으로 불가능하며,")
    print("     측정되지 않은 결측치가 0으로 기록된 것입니다.")
    print(
        f"     특히 Insulin은 {summary_df.loc['Insulin', '실질 결측 비율(%)']}%, "
        f"SkinThickness는 {summary_df.loc['SkinThickness', '실질 결측 비율(%)']}%가 결측입니다."
    )

    return summary_df


def diagnose_outliers_iqr(series: pd.Series, col_name: str) -> dict:
    """3. 사분위수(IQR) 기반 이상치 계산"""
    clean_series = series.dropna()
    q1 = clean_series.quantile(0.25)
    q2 = clean_series.quantile(0.50)
    q3 = clean_series.quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = clean_series[
        (clean_series < lower_bound) | (clean_series > upper_bound)
    ]
    outlier_count = len(outliers)
    outlier_ratio = (outlier_count / len(clean_series)) * 100

    return {
        "column": col_name,
        "count": len(clean_series),
        "q1": q1,
        "median": q2,
        "q3": q3,
        "iqr": iqr,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "outlier_count": outlier_count,
        "outlier_ratio": outlier_ratio,
        "min": clean_series.min(),
        "max": clean_series.max(),
    }


def print_outlier_summary(outlier_info: dict):
    col = outlier_info["column"]
    print(f"\n  >> [{col}] 사분위수(IQR) 기반 이상치 진단:")
    print(f"     - 25% 지점(Q1): {outlier_info['q1']:.2f}")
    print(f"     - 중앙값(Q2):   {outlier_info['median']:.2f}")
    print(f"     - 75% 지점(Q3): {outlier_info['q3']:.2f}")
    print(f"     - 사분위 범위(IQR = Q3 - Q1): {outlier_info['iqr']:.2f}")
    print(
        f"     - 정상 범위 기준: [{outlier_info['lower_bound']:.2f} ~ {outlier_info['upper_bound']:.2f}]"
    )
    print(
        f"     - 이상치 개수: {outlier_info['outlier_count']}개 ({outlier_info['outlier_ratio']:.2f}%)"
    )
    print(f"     - 실제 최솟값: {outlier_info['min']}, 최댓값: {outlier_info['max']}")


def visualize_diagnosis(
    df: pd.DataFrame,
    missing_df: pd.DataFrame,
    insulin_iqr: dict,
    bmi_iqr: dict,
    output_path: str,
):
    """4. 종합 진단 시각화 대시보드 생성 (4개 패널)"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(
        "데이터 진단 대시보드: 결측치(0값 은폐)·이상치 시각화 (피마 인디언 당뇨병 데이터)",
        fontsize=16,
        fontweight="bold",
        y=0.98,
    )

    # -------------------------------------------------------------
    # [패널 1] 실질 결측치 비율 막대 그래프
    # -------------------------------------------------------------
    ax1 = axes[0, 0]
    ratios = missing_df["실질 결측 비율(%)"]
    colors = ["#e74c3c" if r > 0 else "#2ecc71" for r in ratios]
    bars = ax1.barh(
        missing_df.index,
        ratios,
        color=colors,
        edgecolor="black",
        alpha=0.85,
    )
    ax1.set_title(
        "[1] 컬럼별 실질 결측치 비율 (%) (0으로 숨겨진 결측 포함)",
        fontsize=13,
        fontweight="bold",
    )
    ax1.set_xlabel("결측치 비율 (%)")
    ax1.set_xlim(0, max(55, ratios.max() * 1.2))

    for bar, r, count in zip(bars, ratios, missing_df["실질 결측 합계"]):
        txt = f"{r:.1f}% ({count}건)" if count > 0 else "0건 (정상)"
        ax1.text(
            bar.get_width() + 1,
            bar.get_y() + bar.get_height() / 2,
            txt,
            va="center",
            fontsize=10,
            fontweight="bold" if count > 0 else "normal",
            color="#c0392b" if count > 0 else "#27ae60",
        )

    # -------------------------------------------------------------
    # [패널 2] 결측치(0 -> NaN) 분포 히트맵
    # -------------------------------------------------------------
    ax2 = axes[0, 1]
    # ZERO_AS_MISSING 컬럼의 0을 NaN으로 치환한 복사본 생성
    df_with_nan = df.copy()
    for col in ZERO_AS_MISSING:
        df_with_nan[col] = df_with_nan[col].replace(0, np.nan)

    sns.heatmap(
        df_with_nan.isna().T,
        cbar=True,
        cmap=["#ecf0f1", "#e74c3c"],
        ax=ax2,
        yticklabels=df_with_nan.columns,
        cbar_kws={"label": "결측 여부 (빨강 = 결측치)", "ticks": [0, 1]},
    )
    ax2.set_title(
        "[2] 실질 결측치 분포 매트릭스 (행 0 ~ 767)",
        fontsize=13,
        fontweight="bold",
    )
    ax2.set_xlabel("행 인덱스 (총 768건)")

    # -------------------------------------------------------------
    # [패널 3] 인슐린(Insulin) 결측 제외 후 이상치 박스플롯
    # -------------------------------------------------------------
    ax3 = axes[1, 0]
    valid_insulin = df[df["Insulin"] > 0]["Insulin"]
    sns.boxplot(
        x=valid_insulin,
        ax=ax3,
        color="#a8d8ea",
        fliersize=5,
        flierprops={"markerfacecolor": "#e74c3c", "markeredgecolor": "black"},
    )
    ax3.axvline(
        insulin_iqr["upper_bound"],
        color="#e74c3c",
        linestyle="--",
        linewidth=1.5,
        label=f"IQR 상한선: {insulin_iqr['upper_bound']:.1f}",
    )
    ax3.axvline(
        insulin_iqr["median"],
        color="#2980b9",
        linestyle="-",
        linewidth=1.5,
        label=f"중앙값(Q2): {insulin_iqr['median']:.1f}",
    )
    ax3.set_title(
        f"[3] 인슐린(Insulin, 0 제외 유효치) 이상치 박스플롯 (이상치 {insulin_iqr['outlier_count']}건)",
        fontsize=13,
        fontweight="bold",
    )
    ax3.set_xlabel("Insulin (mu U/ml)")
    ax3.legend(loc="upper right")

    # -------------------------------------------------------------
    # [패널 4] 당뇨 발병 여부(Outcome)에 따른 포도당(Glucose) 분포
    # -------------------------------------------------------------
    ax4 = axes[1, 1]
    valid_glucose_df = df[df["Glucose"] > 0]
    sns.histplot(
        data=valid_glucose_df,
        x="Glucose",
        hue="Outcome",
        kde=True,
        ax=ax4,
        palette={0: "#3498db", 1: "#e74c3c"},
        bins=25,
        alpha=0.45,
    )
    ax4.set_title(
        "[4] 당뇨 발병 여부별 포도당(Glucose) 분포 (0=정상, 1=당뇨)",
        fontsize=13,
        fontweight="bold",
    )
    ax4.set_xlabel("Glucose (경구 포도당 농도 mg/dL)")
    ax4.set_ylabel("인원 수")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"\n>> 시각화 대시보드가 성공적으로 저장되었습니다: {output_path}")


def main():
    print("=" * 60)
    print(" [피마 인디언 당뇨병] 결측치 · 중복값 · 이상치 데이터 진단 ")
    print("=" * 60)

    # 1. 데이터 로드
    df = load_pima_dataset()
    print(f"데이터셋 로드 완료: {df.shape[0]}개 행, {df.shape[1]}개 열")

    # 2. 중복값 검증
    diagnose_duplicates(df)

    # 3. 결측치 검증
    missing_df = diagnose_missing_values(df)

    # 4. 이상치 검증 (결측치인 0을 제외한 실제 유효 측정값 기준 IQR)
    print("\n" + "=" * 55)
    print(" [3] 이상치(Outliers) 검증 (0 결측 제외 유효값 기준)")
    print("=" * 55)
    insulin_valid = df[df["Insulin"] > 0]["Insulin"]
    insulin_iqr = diagnose_outliers_iqr(insulin_valid, "Insulin")
    print_outlier_summary(insulin_iqr)

    bmi_valid = df[df["BMI"] > 0]["BMI"]
    bmi_iqr = diagnose_outliers_iqr(bmi_valid, "BMI")
    print_outlier_summary(bmi_iqr)

    # 5. 시각화 생성 및 저장
    script_dir = Path(__file__).resolve().parent
    output_img = script_dir / "data_diagnosis_result.png"
    visualize_diagnosis(df, missing_df, insulin_iqr, bmi_iqr, str(output_img))


if __name__ == "__main__":
    main()
