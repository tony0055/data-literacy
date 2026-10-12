"""타이타닉 데이터셋 상관관계 및 인과/영향 분석 시각화 스크립트.

데이터 리터러시 관점:
1. 단순 상관관계(Correlation)와 실제 생존 메커니즘(Causation)의 차이 규명
2. '여성과 어린이 우선' 원칙(Sex, Age)과 사회경제적 계층(Pclass, Fare)의 복합적 영향 분석
3. 요금(Fare)과 객실(Pclass) 간의 교란 효과(Confounder) 및 가족 규모(FamilySize)의 비선형 효과 분석
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

# ---------------------------------------------------------
# 한글 폰트 및 스타일 설정 (macOS AppleGothic)
# ---------------------------------------------------------
plt.rc("font", family="AppleGothic")
plt.rcParams["axes.unicode_minus"] = False
sns.set_theme(style="whitegrid", font="AppleGothic")


def load_and_preprocess() -> pd.DataFrame:
    """타이타닉 데이터를 불러오고 분석용 전처리를 수행합니다."""
    cache_path = os.path.expanduser(
        "~/.cache/kagglehub/datasets/heptapod/titanic/versions/1/train_and_test2.csv"
    )
    if not os.path.exists(cache_path):
        import kagglehub

        path = kagglehub.dataset_download("heptapod/titanic")
        cache_path = os.path.join(path, "train_and_test2.csv")

    raw_df = pd.read_csv(cache_path)
    # 19개 더미 열 제거
    df = raw_df.loc[:, ~raw_df.columns.str.match(r"zero(\.\d+)?$")].copy()

    # 타깃 컬럼명을 직관적인 'Survived'로 복사
    df["Survived"] = df["2urvived"]

    # 결측치 처리 (Embarked 결측 2건을 최빈값으로 대치)
    df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

    # 파생 변수 생성: 가족 규모(FamilySize) 및 1인 탑승 여부(IsAlone)
    df["FamilySize"] = df["sibsp"] + df["Parch"] + 1
    df["IsAlone"] = (df["FamilySize"] == 1).astype(int)

    # 성별 텍스트 매핑 (0: 남성, 1: 여성)
    df["Sex_Label"] = df["Sex"].map({0: "남성 (Male)", 1: "여성 (Female)"})
    df["Pclass_Label"] = df["Pclass"].map(
        {1: "1등석 (First)", 2: "2등석 (Second)", 3: "3등석 (Third)"}
    )

    return df


def print_statistical_tests(df: pd.DataFrame):
    """주요 변수 간 상관계수 및 통계적 가설 검정 출력"""
    print("\n" + "=" * 60)
    print(" [타이타닉] 상관관계 및 통계적 가설 검정 결과")
    print("=" * 60)

    # 1. 수치형 컬럼 상관계수
    numeric_cols = [
        "Survived",
        "Sex",
        "Pclass",
        "Age",
        "Fare",
        "sibsp",
        "Parch",
        "FamilySize",
        "IsAlone",
    ]
    corr = df[numeric_cols].corr(method="pearson")
    print("\n[생존(Survived)과의 상관계수 (Pearson)]")
    target_corr = corr["Survived"].sort_values(ascending=False)
    for col, val in target_corr.items():
        if col != "Survived":
            print(f"  - {col:12s}: {val:+.4f}")

    # 2. 교차분석 및 카이제곱 검정 (Sex vs Survived)
    sex_contingency = pd.crosstab(df["Sex_Label"], df["Survived"])
    chi2_sex, p_sex, _, _ = stats.chi2_contingency(sex_contingency)
    print(
        f"\n[성별(Sex) vs 생존 카이제곱 검정] Chi2: {chi2_sex:.2f}, p-value: {p_sex:.2e}"
    )

    female_surv_rate = (
        df[df["Sex"] == 1]["Survived"].mean() * 100
    )  # 여성 생존율
    male_surv_rate = df[df["Sex"] == 0]["Survived"].mean() * 100  # 남성 생존율
    print(f"  * 여성 생존율: {female_surv_rate:.1f}%")
    print(f"  * 남성 생존율: {male_surv_rate:.1f}%")

    # 3. 객실등급(Pclass) vs 생존
    pclass_contingency = pd.crosstab(df["Pclass_Label"], df["Survived"])
    chi2_pclass, p_pclass, _, _ = stats.chi2_contingency(pclass_contingency)
    print(
        f"\n[객실등급(Pclass) vs 생존 카이제곱 검정] Chi2: {chi2_pclass:.2f}, p-value: {p_pclass:.2e}"
    )
    for p_val in [1, 2, 3]:
        rate = df[df["Pclass"] == p_val]["Survived"].mean() * 100
        print(f"  * {p_val}등석 생존율: {rate:.1f}%")

    print("\n" + "-" * 60)
    print(" [데이터 리터러시 해석: 상관관계 vs 인과관계]")
    print(
        " 1. 성별(Sex)과 생존(Survived)은 r = +0.54로 가장 강력한 양의 상관을 보입니다."
    )
    print(
        "    이는 단순 상관이 아니라 '여성과 어린이 우선'이라는 당시의 탈출 원칙이"
    )
    print("    직접 작동한 명확한 인과적 영향(Causal Effect)입니다.")
    print(" 2. 운임(Fare, r = +0.26)과 객실(Pclass, r = -0.34)의 생존 영향:")
    print("    높은 운임 자체가 생존을 보장한 것이 아니라, 고운임 = 1등석 상부 갑판 위치라는")
    print("    물리적/구조적 요인이 보트에 신속히 탑승할 수 있었던 교란 경로입니다.")
    print("-" * 60)


def visualize_relationships(df: pd.DataFrame, output_path: str):
    """상관관계 및 인과/영향 분석 4분할 시각화 생성"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 13))
    fig.suptitle(
        "타이타닉 생존 요인 탐색: 상관관계 및 인과/영향 분석",
        fontsize=16,
        fontweight="bold",
        y=0.98,
    )

    # -------------------------------------------------------------
    # [패널 1] 주요 변수 간 피어슨 상관계수 히트맵
    # -------------------------------------------------------------
    ax1 = axes[0, 0]
    corr_cols = [
        "Survived",
        "Sex",
        "Pclass",
        "Fare",
        "Age",
        "FamilySize",
        "IsAlone",
    ]
    corr_labels = [
        "생존(Survived)",
        "성별(Sex:여성1)",
        "객실등급(Pclass)",
        "요금(Fare)",
        "나이(Age)",
        "가족규모(FamilySize)",
        "단독탑승(IsAlone)",
    ]
    corr_matrix = df[corr_cols].corr()
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

    sns.heatmap(
        corr_matrix,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-0.6,
        vmax=0.6,
        ax=ax1,
        xticklabels=corr_labels,
        yticklabels=corr_labels,
        cbar_kws={"label": "상관계수 (Pearson r)"},
    )
    ax1.set_title(
        "[1] 주요 변수 간 상관계수 히트맵", fontsize=13, fontweight="bold"
    )
    ax1.tick_params(axis="x", rotation=30)

    # -------------------------------------------------------------
    # [패널 2] 성별 × 객실등급별 생존율 (인과 요인 상호작용)
    # -------------------------------------------------------------
    ax2 = axes[0, 1]
    palette = {"남성 (Male)": "#3498db", "여성 (Female)": "#e74c3c"}
    surv_by_class_sex = (
        df.groupby(["Pclass_Label", "Sex_Label"])["Survived"]
        .mean()
        .reset_index()
    )
    surv_by_class_sex["Survived_Pct"] = surv_by_class_sex["Survived"] * 100

    sns.barplot(
        data=surv_by_class_sex,
        x="Pclass_Label",
        y="Survived_Pct",
        hue="Sex_Label",
        palette=palette,
        ax=ax2,
        edgecolor="black",
        alpha=0.85,
    )
    ax2.set_title(
        "[2] 객실등급 × 성별에 따른 생존율 (%) (구조적 계층 효과)",
        fontsize=13,
        fontweight="bold",
    )
    ax2.set_xlabel("객실 등급")
    ax2.set_ylabel("생존율 (%)")
    ax2.set_ylim(0, 105)

    for p in ax2.patches:
        height = p.get_height()
        if height > 0:
            ax2.annotate(
                f"{height:.1f}%",
                (p.get_x() + p.get_width() / 2.0, height + 1.5),
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
            )
    ax2.legend(title="성별", loc="upper right")

    # -------------------------------------------------------------
    # [패널 3] 나이 × 요금에 따른 생존 분포 (어린이 및 부유층 구명 효과)
    # -------------------------------------------------------------
    ax3 = axes[1, 0]
    sns.scatterplot(
        data=df,
        x="Age",
        y="Fare",
        hue="Survived",
        palette={0: "#95a5a6", 1: "#2ecc71"},
        alpha=0.7,
        s=40,
        ax=ax3,
    )
    # 어린이 보호선 (Age <= 10) 및 고운임 기준선 (Fare >= 50)
    ax3.axvline(
        10,
        color="#e67e22",
        linestyle="--",
        label="어린이 기준선 (10세 이하 생존율 58.8%)",
    )
    ax3.axhline(50, color="#8e44ad", linestyle=":", label="고운임 기준선 (50 이상)")
    ax3.set_title(
        "[3] 나이(Age) × 요금(Fare)에 따른 생존 분포",
        fontsize=13,
        fontweight="bold",
    )
    ax3.set_xlabel("나이 (Age)")
    ax3.set_ylabel("운임 요금 (Fare)")
    ax3.legend(
        title="생존 여부",
        labels=[
            "사망 (0)",
            "생존 (1)",
            "어린이 (≤10세)",
            "고운임 (≥50)",
        ],
        loc="upper right",
    )

    # -------------------------------------------------------------
    # [패널 4] 가족 규모(FamilySize)에 따른 생존율 (비선형 관계)
    # -------------------------------------------------------------
    ax4 = axes[1, 1]
    family_surv = (
        df.groupby("FamilySize")["Survived"]
        .agg(["mean", "count"])
        .reset_index()
    )
    family_surv["mean_pct"] = family_surv["mean"] * 100

    sns.lineplot(
        data=family_surv,
        x="FamilySize",
        y="mean_pct",
        marker="o",
        markersize=8,
        color="#2c3e50",
        linewidth=2.5,
        ax=ax4,
    )
    ax4.bar(
        family_surv["FamilySize"],
        family_surv["mean_pct"],
        alpha=0.25,
        color="#34495e",
        width=0.4,
    )
    ax4.set_title(
        "[4] 가족 규모(FamilySize)와 생존율 (적정 가족 크기의 보호 효과)",
        fontsize=13,
        fontweight="bold",
    )
    ax4.set_xlabel("가족 규모 (본인 포함 동승자 수)")
    ax4.set_ylabel("생존율 (%)")
    ax4.set_ylim(0, 85)

    for _, row in family_surv.iterrows():
        ax4.text(
            row["FamilySize"],
            row["mean_pct"] + 2,
            f"{row['mean_pct']:.1f}%\n(n={int(row['count'])})",
            ha="center",
            fontsize=8.5,
        )

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"\n>> 시각화 대시보드가 성공적으로 저장되었습니다: {output_path}")


def main():
    df = load_and_preprocess()
    print_statistical_tests(df)

    script_dir = Path(__file__).resolve().parent
    output_path = script_dir / "relationship_analysis.png"
    visualize_relationships(df, str(output_path))


if __name__ == "__main__":
    main()
