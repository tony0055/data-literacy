"""타이타닉(Titanic) 데이터셋 기본 EDA (Exploratory Data Analysis) 스크립트.

데이터리터러시 3~4주차 핵심 개념 반영:
1. 데이터 정제와 무결성 진단 (결측치, 중복값, 이상치 IQR 진단)
2. 기술통계와 대푯값 비교 (평균의 함정과 중앙값/IQR의 필요성)
3. 단변량·이변량·다변량 탐색적 데이터 분석
4. 상관관계 분석 및 데이터 리터러시 관점의 인과/교란 요인 해석

실행 방법:
    python3 school_project/week3/titanic/basic_eda.py
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

# -----------------------------------------------------------------------------
# 0. 시각화 한글 폰트 및 스타일 환경 설정
# -----------------------------------------------------------------------------
def setup_korean_font():
    """운영체제(macOS, Linux, Windows)별 한글 폰트 자동 설정"""
    import platform
    os_name = platform.system()
    if os_name == "Darwin":
        font_family = "AppleGothic"
    elif os_name == "Windows":
        font_family = "Malgun Gothic"
    else:
        font_family = "NanumGothic"

    plt.rc("font", family=font_family)
    plt.rcParams["axes.unicode_minus"] = False  # 마이너스 기호 깨짐 방지
    sns.set_theme(style="whitegrid", font=font_family)


# -----------------------------------------------------------------------------
# 1. 데이터 로드 및 초기 정제
# -----------------------------------------------------------------------------
def load_titanic_data() -> pd.DataFrame:
    """KaggleHub 캐시 또는 다운로드를 통해 타이타닉 데이터를 로드하고 기본 컬럼을 정제합니다."""
    cache_path = os.path.expanduser(
        "~/.cache/kagglehub/datasets/heptapod/titanic/versions/1/train_and_test2.csv"
    )
    if not os.path.exists(cache_path):
        import kagglehub
        path = kagglehub.dataset_download("heptapod/titanic")
        cache_path = os.path.join(path, "train_and_test2.csv")

    raw_df = pd.read_csv(cache_path)

    # 19개 더미 열(zero, zero.1, ... zero.18) 제거
    df = raw_df.loc[:, ~raw_df.columns.str.match(r"zero(\.\d+)?$")].copy()

    # 타깃 변수명 직관화: '2urvived' -> 'Survived'
    df["Survived"] = df["2urvived"]

    # 파생 변수 생성
    # 1) 가족 규모 (본인 포함): FamilySize = sibsp + Parch + 1
    df["FamilySize"] = df["sibsp"] + df["Parch"] + 1
    # 2) 1인 탑승 여부: IsAlone (가족이 없으면 1, 있으면 0)
    df["IsAlone"] = (df["FamilySize"] == 1).astype(int)

    # 가독성을 위한 범주 라벨 컬럼 추가
    df["Sex_Label"] = df["Sex"].map({0: "남성 (Male)", 1: "여성 (Female)"})
    df["Pclass_Label"] = df["Pclass"].map({1: "1등석 (First)", 2: "2등석 (Second)", 3: "3등석 (Third)"})
    df["Survived_Label"] = df["Survived"].map({0: "사망 (Perished)", 1: "생존 (Survived)"})
    df["Embarked_Label"] = df["Embarked"].map({0.0: "Cherbourg(C)", 1.0: "Queenstown(Q)", 2.0: "Southampton(S)"})

    return df


# -----------------------------------------------------------------------------
# 2. 데이터 구조 및 요약 정보 출력
# -----------------------------------------------------------------------------
def print_data_overview(df: pd.DataFrame):
    """데이터 크기, 컬럼 타입, 결측치 여부 등 구조적 개요 출력"""
    print("=" * 70)
    print(" [Step 1] 데이터 기본 구조 및 형태 파악 (Overview)")
    print("=" * 70)
    print(f"▶ 데이터 크기 (Shape): {df.shape[0]:,}행 × {df.shape[1]:,}열")
    print(f"▶ 컬럼 목록: {df.columns.tolist()}\n")

    print("▶ 데이터 상위 3개 행 (head):")
    display_cols = ["Passengerid", "Survived", "Pclass", "Sex", "Age", "Fare", "sibsp", "Parch", "Embarked"]
    print(df[display_cols].head(3).to_string(index=False))

    print("\n▶ 컬럼별 자료형(Dtype) 및 Non-Null 수:")
    info_table = pd.DataFrame({
        "Dtype": df[display_cols].dtypes,
        "Non-Null Count": df[display_cols].notnull().sum(),
        "Null Count": df[display_cols].isnull().sum(),
        "Unique Values": df[display_cols].nunique(),
    })
    print(info_table.to_string())


# -----------------------------------------------------------------------------
# 3. 기술통계 및 대푯값 비교 (평균 vs 중앙값)
# -----------------------------------------------------------------------------
def print_descriptive_stats(df: pd.DataFrame):
    """수치형 변수 기술통계 및 평균 vs 중앙값 비교 (데이터 리터러시 관점)"""
    print("\n" + "=" * 70)
    print(" [Step 2] 기술통계 및 대푯값 비교 (평균 vs 중앙값의 함정)")
    print("=" * 70)

    numeric_cols = ["Age", "Fare", "sibsp", "Parch", "FamilySize"]
    desc = df[numeric_cols].describe().T[["count", "mean", "std", "min", "25%", "50%", "75%", "max"]]
    desc["IQR"] = desc["75%"] - desc["25%"]
    desc["Skewness"] = df[numeric_cols].skew()
    print(desc.round(2).to_string())

    print("\n[데이터 리터러시 핵심 해석: 왜도와 대푯값 선택]")
    print(f" - 운임(Fare): 평균 ${df['Fare'].mean():.2f} vs 중앙값(50%) ${df['Fare'].median():.2f}")
    print(f"   왜도(Skewness) = {df['Fare'].skew():.2f} (심한 양의 왜도/우측 꼬리 분포)")
    print("   → 극소수 부유층의 초고가 티켓(최대 $512.33)으로 인해 평균이 크게 상향 왜곡됨.")
    print("   → 일반 승객의 운임을 대표하는 지표로는 '평균'보다 '중앙값' 및 '사분위수(IQR)'가 객관적임.")

    print(f"\n - 나이(Age): 평균 {df['Age'].mean():.1f}세 vs 중앙값(50%) {df['Age'].median():.1f}세")
    print(f"   왜도(Skewness) = {df['Age'].skew():.2f} (대체로 정규분포에 근접)")


# -----------------------------------------------------------------------------
# 4. 데이터 품질 진단 (중복값, 결측치, IQR 이상치)
# -----------------------------------------------------------------------------
def diagnose_data_quality(df: pd.DataFrame) -> dict:
    """결측치, 중복값, 이상치 진단 수행"""
    print("\n" + "=" * 70)
    print(" [Step 3] 데이터 품질 진단 (Data Quality Diagnosis)")
    print("=" * 70)

    # 1) 중복값
    full_dups = df.duplicated().sum()
    id_dups = df.duplicated(subset=["Passengerid"]).sum()
    print(f"▶ 1. 중복값 진단:")
    print(f"   - 전체 완전 일치 중복 행: {full_dups}건")
    print(f"   - 승객 ID(Passengerid) 중복: {id_dups}건 (모든 행이 고유 식별자 유지)")

    # 2) 결측치
    missing_cnt = df.isnull().sum()
    missing_rate = (missing_cnt / len(df)) * 100
    missing_summary = pd.DataFrame({"결측수": missing_cnt, "결측비율(%)": missing_rate})
    cols_with_na = missing_summary[missing_summary["결측수"] > 0]
    print(f"\n▶ 2. 결측치 진단:")
    if not cols_with_na.empty:
        print(cols_with_na.to_string())
        for col in cols_with_na.index:
            print(f"   → [{col}] 컬럼 결측 {int(missing_cnt[col])}건 ({missing_rate[col]:.2f}%)")
            print(f"     대응 방안: 최빈값({df[col].mode()[0]})으로 대치 권장")
    else:
        print("   - 결측치가 존재하는 컬럼이 없습니다.")

    # 3) 이상치 진단 (IQR 방식)
    print(f"\n▶ 3. 이상치(IQR 기준) 진단:")
    iqr_results = {}
    for col in ["Fare", "Age"]:
        series = df[col].dropna()
        q1 = series.quantile(0.25)
        median = series.quantile(0.50)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers = series[(series < lower) | (series > upper)]
        outlier_count = len(outliers)
        outlier_ratio = (outlier_count / len(series)) * 100
        iqr_results[col] = {
            "q1": q1, "median": median, "q3": q3, "iqr": iqr,
            "lower": lower, "upper": upper, "count": outlier_count, "ratio": outlier_ratio
        }
        print(f"   - [{col:4s}] 정상범위: [{lower:.2f} ~ {upper:.2f}] | 이상치 수: {outlier_count:,}건 ({outlier_ratio:.2f}%)")

    return {"missing": missing_summary, "iqr": iqr_results}


# -----------------------------------------------------------------------------
# 5. 상관관계 및 주요 변수 교차 분석
# -----------------------------------------------------------------------------
def analyze_relationships(df: pd.DataFrame):
    """상관분석 및 교차분석 (성별, 객실등급, 가족규모 등)"""
    print("\n" + "=" * 70)
    print(" [Step 4] 상관관계 및 생존 요인 교차분석")
    print("=" * 70)

    # 1) 성별 생존율
    print("▶ 1. 성별(Sex)별 생존율:")
    sex_stat = df.groupby("Sex_Label")["Survived"].agg(["count", "sum", "mean"]).reset_index()
    sex_stat.columns = ["성별", "탑승자수", "생존자수", "생존율"]
    sex_stat["생존율(%)"] = (sex_stat["생존율"] * 100).round(1)
    print(sex_stat[["성별", "탑승자수", "생존자수", "생존율(%)"]].to_string(index=False))

    # 2) 객실등급별 생존율
    print("\n▶ 2. 객실등급(Pclass)별 생존율:")
    pclass_stat = df.groupby("Pclass_Label")["Survived"].agg(["count", "sum", "mean"]).reset_index()
    pclass_stat.columns = ["객실등급", "탑승자수", "생존자수", "생존율"]
    pclass_stat["생존율(%)"] = (pclass_stat["생존율"] * 100).round(1)
    print(pclass_stat[["객실등급", "탑승자수", "생존자수", "생존율(%)"]].to_string(index=False))

    # 3) 객실등급 × 성별 교차 생존율
    print("\n▶ 3. 객실등급 × 성별 교차 생존율(%):")
    cross = pd.crosstab(df["Pclass_Label"], df["Sex_Label"], values=df["Survived"], aggfunc="mean") * 100
    print(cross.round(1).to_string())

    # 4) 가족 규모별 생존율
    print("\n▶ 4. 가족 규모(FamilySize)별 생존율(%):")
    fam_stat = df.groupby("FamilySize")["Survived"].agg(["count", "mean"]).reset_index()
    fam_stat["생존율(%)"] = (fam_stat["mean"] * 100).round(1)
    fam_stat.rename(columns={"count": "승객수"}, inplace=True)
    print(fam_stat[["FamilySize", "승객수", "생존율(%)"]].to_string(index=False))

    # 5) 상관계수 요약
    num_cols = ["Survived", "Sex", "Pclass", "Fare", "Age", "FamilySize", "IsAlone"]
    corr = df[num_cols].corr()["Survived"].sort_values(ascending=False)
    print("\n▶ 5. 생존(Survived)과의 상관계수 (Pearson r):")
    for col, val in corr.items():
        if col != "Survived":
            direction = "양의 상관" if val > 0 else "음의 상관"
            print(f"   - {col:12s}: {val:+.4f} ({direction})")


# -----------------------------------------------------------------------------
# 6. 종합 시각화 대시보드 생성 (6개 패널)
# -----------------------------------------------------------------------------
def generate_eda_dashboard(df: pd.DataFrame, output_path: str):
    """EDA 핵심 결과를 6분할 종합 대시보드로 시각화하여 저장"""
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle(
        "타이타닉(Titanic) 탐색적 데이터 분석(EDA) 종합 대시보드",
        fontsize=18,
        fontweight="bold",
        y=0.98,
    )

    # -------------------------------------------------------------------------
    # [패널 1] 생존자 비율 (Univariate Target)
    # -------------------------------------------------------------------------
    ax1 = axes[0, 0]
    surv_counts = df["Survived_Label"].value_counts()
    colors1 = ["#e74c3c", "#2ecc71"]
    wedges, texts, autotexts = ax1.pie(
        surv_counts,
        labels=surv_counts.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=colors1,
        explode=(0.05, 0),
        textprops={"fontsize": 11, "fontweight": "bold"},
    )
    ax1.set_title("[1] 타깃 변수: 생존율 분포", fontsize=13, fontweight="bold")

    # -------------------------------------------------------------------------
    # [패널 2] 성별 × 생존율 (Women and Children First)
    # -------------------------------------------------------------------------
    ax2 = axes[0, 1]
    palette_sex = {"사망 (Perished)": "#95a5a6", "생존 (Survived)": "#e74c3c"}
    sns.countplot(data=df, x="Sex_Label", hue="Survived_Label", palette=palette_sex, ax=ax2, edgecolor="black", alpha=0.85)
    ax2.set_title("[2] 성별(Sex)에 따른 생존자 및 사망자 수", fontsize=13, fontweight="bold")
    ax2.set_xlabel("성별")
    ax2.set_ylabel("승객 수 (명)")
    ax2.legend(title="생존 여부")

    # -------------------------------------------------------------------------
    # [패널 3] 객실등급 × 성별 교차 생존율 (%)
    # -------------------------------------------------------------------------
    ax3 = axes[0, 2]
    cross_df = df.groupby(["Pclass_Label", "Sex_Label"])["Survived"].mean().reset_index()
    cross_df["Survived_Pct"] = cross_df["Survived"] * 100
    sns.barplot(
        data=cross_df,
        x="Pclass_Label",
        y="Survived_Pct",
        hue="Sex_Label",
        palette={"남성 (Male)": "#3498db", "여성 (Female)": "#e74c3c"},
        ax=ax3,
        edgecolor="black",
        alpha=0.85,
    )
    ax3.set_title("[3] 객실등급 × 성별 교차 생존율 (%)", fontsize=13, fontweight="bold")
    ax3.set_xlabel("객실 등급")
    ax3.set_ylabel("생존율 (%)")
    ax3.set_ylim(0, 110)
    for p in ax3.patches:
        h = p.get_height()
        if h > 0:
            ax3.annotate(f"{h:.1f}%", (p.get_x() + p.get_width() / 2.0, h + 2), ha="center", fontsize=9, fontweight="bold")

    # -------------------------------------------------------------------------
    # [패널 4] 나이(Age) 분포: 생존자 vs 사망자 (KDE)
    # -------------------------------------------------------------------------
    ax4 = axes[1, 0]
    sns.kdeplot(data=df[df["Survived"] == 1]["Age"], label="생존 (1)", color="#2ecc71", fill=True, alpha=0.3, ax=ax4)
    sns.kdeplot(data=df[df["Survived"] == 0]["Age"], label="사망 (0)", color="#e74c3c", fill=True, alpha=0.3, ax=ax4)
    ax4.axvline(10, color="#d35400", linestyle="--", linewidth=1.5, label="어린이 기준선(≤10세)")
    ax4.set_title("[4] 나이(Age) 분포: 생존 vs 사망 밀도 곡선", fontsize=13, fontweight="bold")
    ax4.set_xlabel("나이 (세)")
    ax4.set_ylabel("확률 밀도 (Density)")
    ax4.legend(loc="upper right")

    # -------------------------------------------------------------------------
    # [패널 5] 가족 규모(FamilySize)와 생존율 (비선형 관계)
    # -------------------------------------------------------------------------
    ax5 = axes[1, 1]
    fam_summary = df.groupby("FamilySize")["Survived"].agg(["mean", "count"]).reset_index()
    fam_summary["mean_pct"] = fam_summary["mean"] * 100
    sns.lineplot(data=fam_summary, x="FamilySize", y="mean_pct", marker="o", markersize=8, color="#2c3e50", linewidth=2.5, ax=ax5)
    ax5.bar(fam_summary["FamilySize"], fam_summary["mean_pct"], alpha=0.2, color="#34495e", width=0.4)
    ax5.set_title("[5] 가족 규모(FamilySize)별 생존율 (비선형 곡선)", fontsize=13, fontweight="bold")
    ax5.set_xlabel("가족 규모 (본인 포함)")
    ax5.set_ylabel("생존율 (%)")
    ax5.set_ylim(0, 85)
    for _, row in fam_summary.iterrows():
        ax5.text(row["FamilySize"], row["mean_pct"] + 2.5, f"{row['mean_pct']:.1f}%", ha="center", fontsize=8.5)

    # -------------------------------------------------------------------------
    # [패널 6] 주요 변수 간 상관계수 히트맵
    # -------------------------------------------------------------------------
    ax6 = axes[1, 2]
    corr_cols = ["Survived", "Sex", "Pclass", "Fare", "Age", "FamilySize", "IsAlone"]
    corr_labels = ["생존", "성별(여1)", "객실등급", "요금", "나이", "가족규모", "단독탑승"]
    corr_mat = df[corr_cols].corr()
    mask = np.triu(np.ones_like(corr_mat, dtype=bool))
    sns.heatmap(
        corr_mat,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-0.6,
        vmax=0.6,
        ax=ax6,
        xticklabels=corr_labels,
        yticklabels=corr_labels,
        cbar_kws={"label": "상관계수 (Pearson r)"}
    )
    ax6.set_title("[6] 주요 변수 간 피어슨 상관계수 히트맵", fontsize=13, fontweight="bold")
    ax6.tick_params(axis="x", rotation=30)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"\n>> EDA 대시보드 이미지가 저장되었습니다: {output_path}")


# -----------------------------------------------------------------------------
# 7. 메인 실행 함수
# -----------------------------------------------------------------------------
def main():
    setup_korean_font()

    print("*" * 70)
    print("      타이타닉(Titanic) 데이터셋 기본 EDA (탐색적 데이터 분석)")
    print("*" * 70)

    # 1. 데이터 로드
    df = load_titanic_data()

    # 2. 데이터 개요
    print_data_overview(df)

    # 3. 기술통계 및 대푯값
    print_descriptive_stats(df)

    # 4. 데이터 품질 진단
    diagnose_data_quality(df)

    # 5. 상관관계 및 교차 분석
    analyze_relationships(df)

    # 6. 시각화 대시보드 저장
    script_dir = Path(__file__).resolve().parent
    output_png = script_dir / "basic_eda_dashboard.png"
    generate_eda_dashboard(df, str(output_png))

    print("\n" + "=" * 70)
    print(" [Step 5] 데이터 리터러시 관점의 종합 결론 (Insights)")
    print("=" * 70)
    print("1. [인과 메커니즘]: 성별(Sex)은 생존에 가장 결정적인 요인 (여성 50% vs 남성 12.9%).")
    print("   단순한 통계적 연관이 아니라 '여성과 어린이 우선'이라는 당시의 탈출 원칙이 직접 작용함.")
    print("2. [교란 요인]: 요금(Fare)과 객실등급(Pclass)의 관계.")
    print("   고운임 승객이 생존한 것은 돈 자체가 아니라 1등석의 상부 갑판 위치라는 물리적 접근성이 본질임.")
    print("3. [비선형 효과]: 가족 규모(FamilySize)는 2~4명 적정 가족에서 생존율이 가장 높고, 1인 탑승자나 5인 이상 대가족은 급감함.")
    print("4. [기술통계 시사점]: Fare의 극단치 왜곡(왜도 4.37)으로 인해 평균 대신 중앙값/IQR 기반 분석이 필수적임.")
    print("*" * 70)


if __name__ == "__main__":
    main()
