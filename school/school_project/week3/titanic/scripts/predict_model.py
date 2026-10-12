"""타이타닉 생존자 예측 머신러닝 모델 구축 및 평가 스크립트.

모델:
1. Logistic Regression (로지스틱 회귀): 변수별 오즈비(Odds Ratio)를 통한 영향력/인과 추론
2. Random Forest Classifier (랜덤 포레스트): 앙상블 기반 비선형 예측 및 특성 중요도(Feature Importance) 산출
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 한글 폰트 설정
plt.rc("font", family="AppleGothic")
plt.rcParams["axes.unicode_minus"] = False
sns.set_theme(style="whitegrid", font="AppleGothic")


def prepare_data():
    """데이터 로드 및 전처리 파이프라인"""
    cache_path = os.path.expanduser(
        "~/.cache/kagglehub/datasets/heptapod/titanic/versions/1/train_and_test2.csv"
    )
    if not os.path.exists(cache_path):
        import kagglehub

        path = kagglehub.dataset_download("heptapod/titanic")
        cache_path = os.path.join(path, "train_and_test2.csv")

    raw_df = pd.read_csv(cache_path)
    df = raw_df.loc[:, ~raw_df.columns.str.match(r"zero(\.\d+)?$")].copy()

    # 결측치 보정 (Embarked)
    df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

    # 특성 공학 (Feature Engineering)
    df["FamilySize"] = df["sibsp"] + df["Parch"] + 1
    df["IsAlone"] = (df["FamilySize"] == 1).astype(int)

    features = [
        "Pclass",
        "Sex",
        "Age",
        "Fare",
        "sibsp",
        "Parch",
        "Embarked",
        "FamilySize",
        "IsAlone",
    ]
    target = "2urvived"

    X = df[features]
    y = df[target]

    # Stratified Split (80:20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 수치형 표준화 (Standard Scaling)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return (
        X_train,
        X_test,
        X_train_scaled,
        X_test_scaled,
        y_train,
        y_test,
        features,
    )


def train_and_evaluate(
    X_train_s, X_test_s, y_train, y_test, feature_names
):
    """모델 학습, 성능 평가 및 오즈비/특성중요도 반환"""
    print("\n" + "=" * 60)
    print(" [타이타닉 생존 예측 모델] 학습 및 평가 결과")
    print("=" * 60)

    # 1. 로지스틱 회귀
    lr = LogisticRegression(random_state=42, max_iter=1000)
    lr.fit(X_train_s, y_train)
    lr_pred = lr.predict(X_test_s)
    lr_prob = lr.predict_proba(X_test_s)[:, 1]

    # 2. 랜덤 포레스트
    rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    rf.fit(X_train_s, y_train)
    rf_pred = rf.predict(X_test_s)
    rf_prob = rf.predict_proba(X_test_s)[:, 1]

    # 성능 비교표 출력
    models = {
        "로지스틱 회귀 (Logistic Regression)": (lr_pred, lr_prob),
        "랜덤 포레스트 (Random Forest)": (rf_pred, rf_prob),
    }

    print("\n[모델별 테스트셋 성능 비교]")
    for name, (pred, prob) in models.items():
        acc = accuracy_score(y_test, pred)
        prec = precision_score(y_test, pred)
        rec = recall_score(y_test, pred)
        f1 = f1_score(y_test, pred)
        auc = roc_auc_score(y_test, prob)
        print(f"\n▶ {name}")
        print(
            f"  정확도(Accuracy): {acc:.4f} | 정밀도(Precision): {prec:.4f} | 재현율(Recall): {rec:.4f}"
        )
        print(f"  F1-Score: {f1:.4f} | ROC-AUC: {auc:.4f}")

    # 로지스틱 오즈비(Odds Ratio) 계산
    # exp(coef) = 특성이 1표준편차 증가할 때 생존 승산비 변화 배수
    odds_ratios = pd.Series(
        np.exp(lr.coef_[0]), index=feature_names
    ).sort_values(ascending=False)
    print("\n[로지스틱 회귀 오즈비 (Odds Ratio, 영향력 지표)]")
    for feat, odds in odds_ratios.items():
        interpretation = "생존 가능성 증가" if odds > 1.0 else "생존 가능성 감소"
        print(f"  - {feat:12s}: {odds:.3f}배 ({interpretation})")

    # 랜덤 포레스트 특성 중요도
    importances = pd.Series(
        rf.feature_importances_, index=feature_names
    ).sort_values(ascending=False)

    return lr, rf, lr_prob, rf_prob, lr_pred, rf_pred, odds_ratios, importances


def visualize_evaluation(
    y_test,
    lr_prob,
    rf_prob,
    rf_pred,
    odds_ratios,
    importances,
    output_path,
):
    """예측 모델 평가 4분할 시각화 생성"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(
        "타이타닉 생존 예측 모델 성능 평가 및 요인별 영향력 분석",
        fontsize=16,
        fontweight="bold",
        y=0.98,
    )

    # -------------------------------------------------------------
    # [패널 1] ROC 곡선 비교
    # -------------------------------------------------------------
    ax1 = axes[0, 0]
    fpr_lr, tpr_lr, _ = roc_curve(y_test, lr_prob)
    auc_lr = roc_auc_score(y_test, lr_prob)
    fpr_rf, tpr_rf, _ = roc_curve(y_test, rf_prob)
    auc_rf = roc_auc_score(y_test, rf_prob)

    ax1.plot(
        fpr_lr,
        tpr_lr,
        label=f"로지스틱 회귀 (AUC = {auc_lr:.3f})",
        color="#3498db",
        linewidth=2,
    )
    ax1.plot(
        fpr_rf,
        tpr_rf,
        label=f"랜덤 포레스트 (AUC = {auc_rf:.3f})",
        color="#2ecc71",
        linewidth=2,
    )
    ax1.plot(
        [0, 1], [0, 1], "k--", alpha=0.5, label="랜덤 기준선 (AUC = 0.500)"
    )
    ax1.set_title(
        "[1] ROC 곡선 비교 (AUC Score)", fontsize=13, fontweight="bold"
    )
    ax1.set_xlabel("위양성률 (False Positive Rate)")
    ax1.set_ylabel("진양성률 (True Positive Rate)")
    ax1.legend(loc="lower right")

    # -------------------------------------------------------------
    # [패널 2] 랜덤 포레스트 혼동 행렬 (Confusion Matrix)
    # -------------------------------------------------------------
    ax2 = axes[0, 1]
    cm = confusion_matrix(y_test, rf_pred)
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        ax=ax2,
        xticklabels=["사망 예측(0)", "생존 예측(1)"],
        yticklabels=["실제 사망(0)", "실제 생존(1)"],
    )
    ax2.set_title(
        "[2] 랜덤 포레스트 혼동 행렬 (Confusion Matrix)",
        fontsize=13,
        fontweight="bold",
    )

    # -------------------------------------------------------------
    # [패널 3] 로지스틱 회귀 승산비 (Odds Ratio, 인과적 영향 해석)
    # -------------------------------------------------------------
    ax3 = axes[1, 0]
    colors = ["#2ecc71" if val >= 1.0 else "#e74c3c" for val in odds_ratios]
    bars = ax3.barh(odds_ratios.index, odds_ratios.values, color=colors, edgecolor="black", alpha=0.85)
    ax3.axvline(1.0, color="black", linestyle="--", linewidth=1.5, label="기준선 (1.0 = 영향 없음)")
    ax3.set_title("[3] 로지스틱 회귀 오즈비 (Odds Ratio: 1 초과시 생존율 증가)", fontsize=13, fontweight="bold")
    ax3.set_xlabel("승산비 (Odds Ratio)")
    ax3.legend(loc="lower right")
    for bar, val in zip(bars, odds_ratios.values):
        ax3.text(
            bar.get_width() + 0.05,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.2f}x",
            va="center",
            fontsize=9.5,
            fontweight="bold",
        )

    # -------------------------------------------------------------
    # [패널 4] 랜덤 포레스트 특성 중요도 (Feature Importance)
    # -------------------------------------------------------------
    ax4 = axes[1, 1]
    sorted_imp = importances.sort_values(ascending=True)
    ax4.barh(sorted_imp.index, sorted_imp.values, color="#9b59b6", edgecolor="black", alpha=0.85)
    ax4.set_title("[4] 랜덤 포레스트 특성 중요도 (Feature Importance)", fontsize=13, fontweight="bold")
    ax4.set_xlabel("상대적 중요도")
    for y_idx, (feat, val) in enumerate(sorted_imp.items()):
        ax4.text(val + 0.005, y_idx, f"{val*100:.1f}%", va="center", fontsize=9.5)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"\n>> 모델 평가 대시보드가 성공적으로 저장되었습니다: {output_path}")


def main():
    (
        X_train,
        X_test,
        X_train_s,
        X_test_s,
        y_train,
        y_test,
        features,
    ) = prepare_data()

    (
        lr,
        rf,
        lr_prob,
        rf_prob,
        lr_pred,
        rf_pred,
        odds_ratios,
        importances,
    ) = train_and_evaluate(
        X_train_s, X_test_s, y_train, y_test, features
    )

    script_dir = Path(__file__).resolve().parent
    output_path = script_dir / "model_evaluation.png"
    visualize_evaluation(
        y_test,
        lr_prob,
        rf_prob,
        rf_pred,
        odds_ratios,
        importances,
        str(output_path),
    )


if __name__ == "__main__":
    main()
