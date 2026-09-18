"""Kaggle `heptapod/titanic` 데이터셋을 kagglehub으로 내려받는다.

사전 준비:
    pip install kagglehub
    ~/.kaggle/kaggle.json (Kaggle > Settings > API > Create New Token)

실행:
    python3 school_project/week3/titanic/scripts/download_titanic.py
"""

import os

import kagglehub

DATASET = "heptapod/titanic"


def main() -> None:
    # 캐시에 이미 있으면 재다운로드 없이 캐시 경로를 돌려준다.
    path = kagglehub.dataset_download(DATASET)
    print("Path to dataset files:", path)
    for name in sorted(os.listdir(path)):
        print(" -", name)


if __name__ == "__main__":
    main()
