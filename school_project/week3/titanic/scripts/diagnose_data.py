"""데이터 정제 기초: 결측치, 중복값, 이상치 진단 및 시각화 스크립트.

이 스크립트는 원본 데이터를 절대 수정하거나 지우지 않고(AI 함정 방지),
현재 데이터의 상태를 객관적으로 검증(진단)하고 시각화합니다.
"""

import os
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


def load_titanic_dataset() -> pd.DataFrame:
    """캐시된 타이타닉 데이터셋을 로드하고 더미 열을 정리합니다."""
    cache_path = os.path.expanduser(
        "~/.cache/kagglehub/datasets/heptapod/titanic/versions/1/train_and_test2.csv"
    )
    if not os.path.exists(cache_path):
        import kagglehub
        path = kagglehub.dataset_download("heptapod/titanic")
        cache_path = os.path.join(path, "train_and_test2.csv")

    raw_df = pd.read_csv(cache_path)
    # zero 더미 열(19개) 제거 (단, 원본 파일은 건드리지 않음)
    df = raw_df.loc[:, ~raw_df.columns.str.match(r"zero(\.\d+)?$")].copy()
    return df


def diagnose_duplicates(df: pd.DataFrame) -> dict:
    """1. 중복값 검증"""
    print("\n" + "=" * 50)
    print(" [1] 중복값(Duplicate) 검증")
    print("=" * 50)

    total_rows = len(df)
    duplicate_rows = df.duplicated().sum()
    duplicate_ratio = (duplicate_rows / total_rows) * 100

    print(f"- 전체 데이터 행 수: {total_rows:,}개")
    print(f"- 완전히 일치하는 중복 행 수: {duplicate_rows:,}개 ({duplicate_ratio:.2f}%)")

    # 식별자(Passengerid) 기준 고유성 검증
    if "Passengerid" in df.columns:
        id_duplicates = df.duplicated(subset=["Passengerid"]).sum()
        print(f"- 승객 고유 ID(Passengerid) 중복 수: {id_duplicates:,}개")

    return {
        "total_rows": total_rows,
        "duplicate_rows": duplicate_rows,
        "duplicate_ratio": duplicate_ratio,
    }


def diagnose_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """2. 결측치 검증"""
    print("\n" + "=" * 50)
    print(" [2] 결측치(Missing Values) 검증")
    print("=" * 50)

    total_rows = len(df)
    missing_count = df.isna().sum()
    missing_ratio = (missing_count / total_rows) * 100

    summary_df = pd.DataFrame(
        {
            "자료형(dtype)": df.dtypes,
            "결측 개수": missing_count,
            "결측 비율(%)": missing_ratio.round(2),
            "고유값 개수(nunique)": df.nunique(),
        }
    )

    print(summary_df.to_string())

    # 결측치가 존재하는 열에 대한 세부 진단
    cols_with_na = summary_df[summary_df["결측 개수"] > 0].index.tolist()
    if cols_with_na:
        print("\n  >> 결측치가 존재하는 컬럼 상세:")
        for col in cols_with_na:
            na_indices = df[df[col].isna()].index.tolist()
            print(f"     - [{col}] 결측치 {missing_count[col]}개 (행 번호: {na_indices})")
    else:
        print("\n  >> 결측치가 존재하는 컬럼이 없습니다.")

    return summary_df


def diagnose_outliers_iqr(df: pd.DataFrame, column: str) -> dict:
    """3. 이상치 검증 (IQR 방식)"""
    series = df[column].dropna()

    q1 = series.quantile(0.25)
    q2 = series.quantile(0.50)  # 중앙값
    q3 = series.quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = series[(series < lower_bound) | (series > upper_bound)]
    outlier_count = len(outliers)
    outlier_ratio = (outlier_count / len(series)) * 100

    return {
        "column": column,
        "count": len(series),
        "q1": q1,
        "median": q2,
        "q3": q3,
        "iqr": iqr,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "outlier_count": outlier_count,
        "outlier_ratio": outlier_ratio,
        "min": series.min(),
        "max": series.max(),
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
    fare_iqr: dict,
    age_iqr: dict,
    output_path: str,
):
    """4. 종합 시각화 대시보드 생성 (4개 패널)"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle(
        "데이터 진단 대시보드: 결측치·이상치 시각화 (타이타닉 데이터셋)",
        fontsize=16,
        fontweight="bold",
        y=0.98,
    )

    # -------------------------------------------------------------
    # [패널 1] 결측치 비율 막대 그래프
    # -------------------------------------------------------------
    ax1 = axes[0, 0]
    colors = [
        "#e74c3c" if r > 0 else "#3498db" for r in missing_df["결측 비율(%)"]
    ]
    bars = ax1.barh(
        missing_df.index,
        missing_df["결측 비율(%)"],
        color=colors,
        edgecolor="black",
        alpha=0.8,
    )
    ax1.set_title(
        "[1] 컬럼별 결측치(Missing Value) 비율 (%)",
        fontsize=13,
        fontweight="bold",
    )
    ax1.set_xlabel("결측치 비율 (%)")
    ax1.set_xlim(0, max(5, missing_df["결측 비율(%)"].max() * 1.5))

    # 값 레이블 추가
    for bar, val, count in zip(
        bars, missing_df["결측 비율(%)"], missing_df["결측 개수"]
    ):
        label = f"{val:.2f}% ({count}건)" if count > 0 else "0건 (정상)"
        ax1.text(
            bar.get_width() + 0.1,
            bar.get_y() + bar.get_height() / 2,
            label,
            va="center",
            fontsize=10,
            fontweight="bold" if count > 0 else "normal",
            color="#c0392b" if count > 0 else "#555555",
        )

    # -------------------------------------------------------------
    # [패널 2] 결측치 위치 히트맵 (어디에 결측이 있는지 시각화)
    # -------------------------------------------------------------
    ax2 = axes[0, 1]
    # 결측치 여부를 불리언 매트릭스로 변환 (True=1, False=0)
    # 데이터가 많으므로 상위 200개 행을 보거나 전체의 결측 패턴 표시
    sns.heatmap(
        df.isna().T,
        cbar=True,
        cmap=["#f8f9fa", "#e74c3c"],
        ax=ax2,
        yticklabels=df.columns,
        cbar_kws={"label": "결측 여부 (빨간색 = 결측치)", "ticks": [0, 1]},
    )
    ax2.set_title(
        "[2] 결측치 분포 매트릭스 (전체 행 관측)",
        fontsize=13,
        fontweight="bold",
    )
    ax2.set_xlabel("행 인덱스 (0 ~ 1308)")

    # -------------------------------------------------------------
    # [패널 3] 요금(Fare) 박스플롯 & 이상치 탐지
    # -------------------------------------------------------------
    ax3 = axes[1, 0]
    sns.boxplot(
        x=df["Fare"],
        ax=ax3,
        color="#a8d8ea",
        fliersize=5,
        flierprops={"markerfacecolor": "#e74c3c", "markeredgecolor": "black"},
    )
    ax3.axvline(
        fare_iqr["upper_bound"],
        color="#e74c3c",
        linestyle="--",
        linewidth=1.5,
        label=f"IQR 상한선: {fare_iqr['upper_bound']:.2f}",
    )
    ax3.axvline(
        fare_iqr["median"],
        color="#2980b9",
        linestyle="-",
        linewidth=1.5,
        label=f"중앙값(Q2): {fare_iqr['median']:.2f}",
    )
    ax3.set_title(
        f"[3] 요금(Fare) 이상치 박스플롯 (이상치 {fare_iqr['outlier_count']}건 탐지)",
        fontsize=13,
        fontweight="bold",
    )
    ax3.set_xlabel("Fare (운임 요금)")
    ax3.legend(loc="upper right")

    # -------------------------------------------------------------
    # [패널 4] 나이(Age) 분포 히스토그램 및 박스플롯 (복합)
    # -------------------------------------------------------------
    ax4 = axes[1, 1]
    sns.histplot(
        df["Age"],
        kde=True,
        ax=ax4,
        color="#3498db",
        bins=30,
        stat="density",
        alpha=0.5,
    )
    ax4.axvline(
        age_iqr["lower_bound"],
        color="#e67e22",
        linestyle="--",
        label=f"하한선: {age_iqr['lower_bound']:.1f}",
    )
    ax4.axvline(
        age_iqr["upper_bound"],
        color="#e67e22",
        linestyle="--",
        label=f"상한선: {age_iqr['upper_bound']:.1f}",
    )
    ax4.axvline(
        age_iqr["median"],
        color="#2c3e50",
        linestyle="-",
        label=f"중앙값: {age_iqr['median']:.1f}",
    )
    ax4.set_title(
        f"[4] 나이(Age) 분포 및 밀도 곡선 (이상치 {age_iqr['outlier_count']}건)",
        fontsize=13,
        fontweight="bold",
    )
    ax4.set_xlabel("Age (나이)")
    ax4.set_ylabel("밀도 (Density)")
    ax4.legend(loc="upper right")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"\n>> 시각화 대시보드가 성공적으로 저장되었습니다: {output_path}")


def main():
    print("=" * 60)
    print(" [데이터 진단] 결측치 · 중복값 · 이상치 검증 시작 ")
    print("=" * 60)

    # 1. 데이터 로드
    df = load_titanic_dataset()
    print(f"데이터셋 로드 완료: {df.shape[0]}개 행, {df.shape[1]}개 열")

    # 2. 중복값 검증
    dup_info = diagnose_duplicates(df)

    # 3. 결측치 검증
    missing_df = diagnose_missing_values(df)

    # 4. 이상치 검증 (IQR 방식)
    print("\n" + "=" * 50)
    print(" [3] 이상치(Outliers) 검증")
    print("=" * 50)
    fare_iqr = diagnose_outliers_iqr(df, "Fare")
    print_outlier_summary(fare_iqr)

    age_iqr = diagnose_outliers_iqr(df, "Age")
    print_outlier_summary(age_iqr)

    # 5. 시각화 생성 및 저장
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_img = os.path.join(script_dir, "data_diagnosis_result.png")
    visualize_diagnosis(df, missing_df, fare_iqr, age_iqr, output_img)


if __name__ == "__main__":
    main()
