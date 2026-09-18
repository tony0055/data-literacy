"""피마 인디언 당뇨병(Pima Indians Diabetes) 예측 머신러닝 모델 구축 및 평가 스크립트.

데이터 리터러시 핵심:
1. 0으로 은폐된 결측치를 Train 세트의 중앙값(Median)으로 대치하여 데이터 누수(Data Leakage) 방지
2. Logistic Regression의 오즈비(Odds Ratio)를 통해 각 생체 지표의 당뇨 발병 위험도(영향력) 해석
3. Random Forest를 통한 비선형 상호작용 포착 및 특성 중요도(Feature Importance) 분석
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
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
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

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


def prepare_data():
    """데이터 로드, 0 결측 치환, Train/Test 분할 및 중앙값 대치/스케일링"""
    cache_path = os.path.expanduser(
        f"~/.cache/kagglehub/datasets/{DATASET_NAME}/versions/1/{CSV_FILENAME}"
    )
    if not os.path.exists(cache_path):
        import kagglehub

        download_path = kagglehub.dataset_download(DATASET_NAME)
        cache_path = os.path.join(download_path, CSV_FILENAME)

    df = pd.read_csv(cache_path, header=None, names=COLUMNS)

    # 0으로 기록된 결측치를 NaN으로 변환
    for col in ZERO_AS_MISSING:
        df[col] = df[col].replace(0, np.nan)

    features = [c for c in COLUMNS if c != "Outcome"]
    X = df[features]
    y = df["Outcome"]

    # Stratified Train-Test Split (80:20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 데이터 누수(Data Leakage)를 방지하기 위해 Train 셋 기준으로 중앙값(Median) 산출 및 대치
    imputer = SimpleImputer(strategy="median")
    X_train_imp = imputer.fit_transform(X_train)
    X_test_imp = imputer.transform(X_test)

    # 표준화 스케일링
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train_imp)
    X_test_s = scaler.transform(X_test_imp)

    return X_train_s, X_test_s, y_train, y_test, features


def train_and_evaluate(X_train_s, X_test_s, y_train, y_test, feature_names):
    """로지스틱 회귀 및 랜덤포레스트 학습 및 오즈비/중요도 산출"""
    print("\n" + "=" * 65)
    print(" [피마 인디언 당뇨병 예측 모델] 머신러닝 학습 및 평가 결과")
    print("=" * 65)

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

    models = {
        "로지스틱 회귀 (Logistic Regression)": (lr_pred, lr_prob),
        "랜덤 포레스트 (Random Forest)": (rf_pred, rf_prob),
    }

    print("\n[테스트셋 분류 성능 지표]")
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

    # 오즈비(Odds Ratio) = exp(coef)
    odds_ratios = pd.Series(
        np.exp(lr.coef_[0]), index=feature_names
    ).sort_values(ascending=False)
    print("\n[로지스틱 회귀 오즈비 (Odds Ratio, 당뇨 발병 위험 승산비)]")
    for feat, odds in odds_ratios.items():
        print(f"  - {feat:24s}: {odds:.3f}배 (1표준편차 증가 시 당뇨 위험)")

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
    """예측 모델 종합 평가 4분할 시각화"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(
        "피마 인디언 당뇨병 예측 모델 성능 평가 및 임상 지표 영향력",
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
        [0, 1], [0, 1], "k--", alpha=0.5, label="무작위 기준선 (AUC = 0.500)"
    )
    ax1.set_title(
        "[1] ROC 곡선 비교 (분류 성능 평가)", fontsize=13, fontweight="bold"
    )
    ax1.set_xlabel("위양성률 (1 - 특이도)")
    ax1.set_ylabel("진양성률 (민감도/재현율)")
    ax1.legend(loc="lower right")

    # -------------------------------------------------------------
    # [패널 2] 혼동 행렬 (Confusion Matrix)
    # -------------------------------------------------------------
    ax2 = axes[0, 1]
    cm = confusion_matrix(y_test, rf_pred)
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Reds",
        ax=ax2,
        xticklabels=["정상 예측(0)", "당뇨 예측(1)"],
        yticklabels=["실제 정상(0)", "실제 당뇨(1)"],
    )
    ax2.set_title(
        "[2] 랜덤 포레스트 혼동 행렬 (Confusion Matrix)",
        fontsize=13,
        fontweight="bold",
    )

    # -------------------------------------------------------------
    # [패널 3] 로지스틱 회귀 오즈비 (Odds Ratio)
    # -------------------------------------------------------------
    ax3 = axes[1, 0]
    colors = ["#e74c3c" if val >= 1.0 else "#3498db" for val in odds_ratios]
    bars = ax3.barh(
        odds_ratios.index,
        odds_ratios.values,
        color=colors,
        edgecolor="black",
        alpha=0.85,
    )
    ax3.axvline(
        1.0,
        color="black",
        linestyle="--",
        linewidth=1.5,
        label="기준선 (1.0 = 위험 변화 없음)",
    )
    ax3.set_title(
        "[3] 로지스틱 회귀 오즈비 (1표준편차 증가 시 당뇨 위험 배수)",
        fontsize=13,
        fontweight="bold",
    )
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
    ax4.barh(
        sorted_imp.index,
        sorted_imp.values,
        color="#e67e22",
        edgecolor="black",
        alpha=0.85,
    )
    ax4.set_title(
        "[4] 랜덤 포레스트 특성 중요도 (Feature Importance)",
        fontsize=13,
        fontweight="bold",
    )
    ax4.set_xlabel("상대적 중요도")
    for y_idx, (feat, val) in enumerate(sorted_imp.items()):
        ax4.text(
            val + 0.005, y_idx, f"{val*100:.1f}%", va="center", fontsize=9.5
        )

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(
        f"\n>> 피마 인디언 모델 평가 대시보드가 성공적으로 저장되었습니다: {output_path}"
    )


def main():
    X_train_s, X_test_s, y_train, y_test, features = prepare_data()
    (
        lr,
        rf,
        lr_prob,
        rf_prob,
        lr_pred,
        rf_pred,
        odds_ratios,
        importances,
    ) = train_and_evaluate(X_train_s, X_test_s, y_train, y_test, features)

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
