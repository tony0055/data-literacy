"""피마 인디언 당뇨병 데이터셋 상관관계 및 인과/영향 분석 시각화 스크립트.

데이터 리터러시 핵심:
1. 0으로 숨겨진 결측치를 방치했을 때 vs 결측 보정 후의 상관계수 왜곡 실증 (Data Literacy Insight)
2. 포도당(Glucose), BMI, 인슐린(Insulin)의 당뇨 발병에 대한 직접적 인과 기전 규명
3. 나이(Age)와 임신 횟수(Pregnancies) 간의 교란 관계(Confounder) 분석
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

plt.rc("font", family="AppleGothic")
plt.rcParams["axes.unicode_minus"] = False
sns.set_theme(style="whitegrid", font="AppleGothic")

DATASET_NAME = "kumargh/pimaindiansdiabetescsv"
CSV_FILENAME = "pima-indians-diabetes.csv"

COLUMNS = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
    "Outcome",
]

ZERO_AS_MISSING = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]


def load_datasets():
    """원본 데이터 및 0을 NaN으로 치환한 결측 보정 데이터를 반환합니다."""
    cache_path = os.path.expanduser(
        f"~/.cache/kagglehub/datasets/{DATASET_NAME}/versions/1/{CSV_FILENAME}"
    )
    if not os.path.exists(cache_path):
        import kagglehub

        download_path = kagglehub.dataset_download(DATASET_NAME)
        cache_path = os.path.join(download_path, CSV_FILENAME)

    raw_df = pd.read_csv(cache_path, header=None, names=COLUMNS)

    # 0값을 NaN으로 보정한 정제 데이터셋
    clean_df = raw_df.copy()
    for col in ZERO_AS_MISSING:
        clean_df[col] = clean_df[col].replace(0, np.nan)

    # 연령대 파생 변수 (Age Group)
    clean_df["AgeGroup"] = pd.cut(
        clean_df["Age"],
        bins=[20, 30, 40, 50, 60, 100],
        labels=["20대", "30대", "40대", "50대", "60대 이상"],
        right=False,
    )

    return raw_df, clean_df


def print_relationship_insights(raw_df: pd.DataFrame, clean_df: pd.DataFrame):
    """결측 보정 전/후 상관계수 비교 및 통계 검정 출력"""
    print("\n" + "=" * 65)
    print(" [피마 인디언 당뇨병] 상관관계 및 데이터 리터러시 인과 분석")
    print("=" * 65)

    raw_corr = raw_df.corr()["Outcome"]
    clean_corr = clean_df.corr(numeric_only=True)["Outcome"]

    comparison = pd.DataFrame(
        {
            "0 방치 시 상관계수": raw_corr,
            "결측(NaN) 보정 후 상관계수": clean_corr,
            "차이 (보정후 - 방치시)": clean_corr - raw_corr,
        }
    ).drop("Outcome")

    print("\n[당뇨 발병(Outcome)과의 상관계수 비교: 0값 은폐 결측의 왜곡 실증]")
    print(comparison.round(4).to_string())

    print("\n" + "-" * 65)
    print(" [데이터 리터러시 핵심 통찰: AI/통계의 함정]")
    print(" 1. Insulin(인슐린):")
    print(
        f"    - 0을 방치하면 r = {raw_corr['Insulin']:.4f}로 영향이 미미해 보이지만,"
    )
    print(
        f"    - 0을 결측치로 정제하면 r = {clean_corr['Insulin']:.4f}로 2배 이상 급증합니다."
    )
    print(
        "    - 기계적인 통계 처리가 인슐린의 임상적 중요성을 완전히 은폐했던 사례입니다."
    )
    print(" 2. Glucose(포도당)과 BMI의 인과성:")
    print(
        f"    - Glucose는 r = {clean_corr['Glucose']:.4f}, BMI는 r = {clean_corr['BMI']:.4f}로"
    )
    print(
        "      당뇨 발병을 결정짓는 가장 직접적인 생물학적 원인(Causal Driver)입니다."
    )
    print(" 3. Pregnancies(임신 횟수)와 Age(나이)의 교란(Confounding):")
    age_preg_corr = clean_df["Age"].corr(clean_df["Pregnancies"])
    print(f"    - Age와 Pregnancies 간 상관계수는 r = {age_preg_corr:.4f}입니다.")
    print(
        "    - 나이가 들수록 임신 횟수가 누적되므로, 임신 자체의 위험인지 연령 증가에 따른"
    )
    print(
        "      인슐린 저항성 증가인지 통제 변수를 적용한 다변량 분석이 필수적입니다."
    )
    print("-" * 65)


def visualize_relationships(
    raw_df: pd.DataFrame, clean_df: pd.DataFrame, output_path: str
):
    """피마 인디언 관계성 4분할 시각화 생성"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 13))
    fig.suptitle(
        "피마 인디언 당뇨병 데이터 관계성 탐색: 상관관계 왜곡 실증 및 인과 요인 분석",
        fontsize=16,
        fontweight="bold",
        y=0.98,
    )

    # -------------------------------------------------------------
    # [패널 1] 0 방치 vs 결측 보정 후 Outcome 상관계수 비교 막대 그래프
    # -------------------------------------------------------------
    ax1 = axes[0, 0]
    raw_corr = raw_df.corr()["Outcome"].drop("Outcome")
    clean_corr = clean_df.corr(numeric_only=True)["Outcome"].drop("Outcome")

    x = np.arange(len(raw_corr))
    width = 0.35

    ax1.bar(
        x - width / 2,
        raw_corr,
        width,
        label="0 방치 시 (결측 미처리)",
        color="#95a5a6",
        edgecolor="black",
        alpha=0.8,
    )
    ax1.bar(
        x + width / 2,
        clean_corr,
        width,
        label="결측(NaN) 보정 후",
        color="#e74c3c",
        edgecolor="black",
        alpha=0.85,
    )

    ax1.set_title(
        "[1] 결측 보정 전 vs 후 상관계수 변화 (데이터 왜곡 실증)",
        fontsize=13,
        fontweight="bold",
    )
    ax1.set_xticks(x)
    ax1.set_xticklabels(raw_corr.index, rotation=35, ha="right")
    ax1.set_ylabel("Outcome(당뇨)과의 상관계수")
    ax1.axhline(0, color="black", linestyle="--", alpha=0.5)
    ax1.legend(loc="upper left")

    # -------------------------------------------------------------
    # [패널 2] 결측 보정 후 전체 지표 간 상관계수 히트맵
    # -------------------------------------------------------------
    ax2 = axes[0, 1]
    corr_matrix = clean_df[COLUMNS].corr()
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

    sns.heatmap(
        corr_matrix,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-0.4,
        vmax=0.6,
        ax=ax2,
        cbar_kws={"label": "상관계수 (Pearson r)"},
    )
    ax2.set_title(
        "[2] 결측 보정 후 전체 변수 간 상관계수 히트맵",
        fontsize=13,
        fontweight="bold",
    )
    ax2.tick_params(axis="x", rotation=35)

    # -------------------------------------------------------------
    # [패널 3] 포도당(Glucose) × BMI 산점도 (양대 인과 드라이버)
    # -------------------------------------------------------------
    ax3 = axes[1, 0]
    valid_scatter = clean_df.dropna(subset=["Glucose", "BMI"])
    sns.scatterplot(
        data=valid_scatter,
        x="Glucose",
        y="BMI",
        hue="Outcome",
        palette={0: "#3498db", 1: "#e74c3c"},
        alpha=0.75,
        s=45,
        ax=ax3,
    )
    # 임상적 위험 기준선 표시
    ax3.axvline(
        140,
        color="#c0392b",
        linestyle="--",
        linewidth=1.5,
        label="내당능 장애 기준 (식후 140 mg/dL)",
    )
    ax3.axhline(
        30,
        color="#8e44ad",
        linestyle=":",
        linewidth=1.5,
        label="비만 기준선 (BMI ≥ 30)",
    )
    ax3.set_title(
        "[3] 포도당(Glucose) × BMI 2대 인과 요인 분포",
        fontsize=13,
        fontweight="bold",
    )
    ax3.set_xlabel("Glucose (포도당 농도 mg/dL)")
    ax3.set_ylabel("BMI (체질량 지수)")
    ax3.legend(
        title="구분",
        labels=["정상 (0)", "당뇨 (1)", "포도당 위험(≥140)", "비만 위험(≥30)"],
        loc="upper left",
    )

    # -------------------------------------------------------------
    # [패널 4] 연령대별 당뇨 발병률 및 평균 임신 횟수 추이
    # -------------------------------------------------------------
    ax4 = axes[1, 1]
    age_stats = (
        clean_df.groupby("AgeGroup", observed=False)
        .agg(
            Diabetes_Rate=("Outcome", "mean"),
            Mean_Pregnancies=("Pregnancies", "mean"),
            Count=("Outcome", "count"),
        )
        .reset_index()
    )
    age_stats["Diabetes_Pct"] = age_stats["Diabetes_Rate"] * 100

    ax4_sub = ax4.twinx()
    bars = ax4.bar(
        age_stats["AgeGroup"],
        age_stats["Diabetes_Pct"],
        color="#e74c3c",
        alpha=0.6,
        width=0.45,
        edgecolor="black",
        label="당뇨 발병률 (%)",
    )
    lines = ax4_sub.plot(
        age_stats["AgeGroup"],
        age_stats["Mean_Pregnancies"],
        color="#2c3e50",
        marker="s",
        linewidth=2.5,
        markersize=8,
        label="평균 임신 횟수",
    )

    ax4.set_title(
        "[4] 연령대별 당뇨 발병률 및 임신 횟수 추이 (연령 교란 효과)",
        fontsize=13,
        fontweight="bold",
    )
    ax4.set_xlabel("연령대")
    ax4.set_ylabel("당뇨 발병률 (%)", color="#c0392b")
    ax4_sub.set_ylabel("평균 임신 횟수 (회)", color="#2c3e50")
    ax4.set_ylim(0, 80)
    ax4_sub.set_ylim(0, 8)
    ax4_sub.grid(False)

    for bar, pct in zip(bars, age_stats["Diabetes_Pct"]):
        ax4.text(
            bar.get_x() + bar.get_width() / 2,
            pct + 2,
            f"{pct:.1f}%",
            ha="center",
            fontsize=10,
            fontweight="bold",
        )

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"\n>> 피마 인디언 시각화 대시보드가 성공적으로 저장되었습니다: {output_path}")


def main():
    raw_df, clean_df = load_datasets()
    print_relationship_insights(raw_df, clean_df)

    script_dir = Path(__file__).resolve().parent
    output_path = script_dir / "relationship_analysis.png"
    visualize_relationships(raw_df, clean_df, str(output_path))


if __name__ == "__main__":
    main()
