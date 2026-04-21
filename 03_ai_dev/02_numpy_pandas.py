# =============================================================================
# NumPy & Pandas  |  데이터 처리의 기본
# =============================================================================
# 설치: pip install numpy pandas
# AI/ML 파이프라인에서 데이터 전처리에 필수

import numpy as np
import pandas as pd

print("=" * 60)
print("NumPy - 수치 계산 (행렬/배열)")
print("=" * 60)

# ── NumPy 배열 ─────────────────────────────────────────────────────────────
a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

print(a.dtype)     # int64
print(a.shape)     # (5,)
print(a.ndim)      # 1

# ── 배열 연산 (Python list와 달리 원소별 연산) ───────────────────────────
print(a + b)       # [11 22 33 44 55]   (list면 연결)
print(a * 2)       # [2 4 6 8 10]
print(a ** 2)      # [1 4 9 16 25]
print(a > 3)       # [False False False  True  True]

# 불리언 인덱싱
print(a[a > 3])    # [4 5]  (조건에 맞는 원소만)
print(b[a % 2 == 0])  # [20 40]  (a의 짝수 인덱스의 b 값)

# ── 2D 배열 (행렬) ────────────────────────────────────────────────────────
matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

print(matrix.shape)    # (3, 3)
print(matrix[0])       # [1 2 3]  (첫 번째 행)
print(matrix[:, 0])    # [1 4 7]  (첫 번째 열)
print(matrix[1, 2])    # 6        (2행 3열)
print(matrix.T)        # 전치 행렬

# 행렬 연산
print(np.dot(matrix, matrix))  # 행렬 곱
print(matrix.sum())            # 45  (전체 합)
print(matrix.sum(axis=0))      # [12 15 18]  (열 합계)
print(matrix.sum(axis=1))      # [6 15 24]   (행 합계)
print(matrix.mean())           # 5.0
print(matrix.std())            # 표준편차

# ── 배열 생성 ─────────────────────────────────────────────────────────────
print(np.zeros((3, 4)))          # 0으로 채운 3x4 배열
print(np.ones((2, 3)))           # 1로 채운 2x3 배열
print(np.eye(3))                 # 3x3 단위 행렬
print(np.arange(0, 10, 2))       # [0 2 4 6 8]  (range와 유사)
print(np.linspace(0, 1, 5))      # [0. 0.25 0.5 0.75 1.]  (균등 간격 5개)
print(np.random.rand(3, 3))      # 0~1 랜덤 3x3 배열
print(np.random.randint(0, 100, size=(3, 3)))  # 정수 랜덤

print("\n" + "=" * 60)
print("Pandas - 테이블 데이터 (DataFrame)")
print("= DataFrame = DB 테이블 / Excel 시트")
print("=" * 60)

# ── DataFrame 생성 ────────────────────────────────────────────────────────
df = pd.DataFrame({
    "name":   ["Alice", "Bob", "Charlie", "Dave", "Eve"],
    "age":    [25, 30, 35, 28, 22],
    "city":   ["서울", "부산", "서울", "대구", "서울"],
    "salary": [50000, 60000, 80000, 55000, 45000],
    "active": [True, True, False, True, True],
})

print(df)
print(df.dtypes)       # 컬럼 타입
print(df.shape)        # (5, 5)  → (행 수, 열 수)
print(df.info())       # 요약 정보
print(df.describe())   # 숫자형 컬럼 통계

# ── 컬럼 선택 ─────────────────────────────────────────────────────────────
print(df["name"])             # Series (단일 컬럼)
print(df[["name", "salary"]]) # DataFrame (여러 컬럼)

# ── 행 선택 ───────────────────────────────────────────────────────────────
print(df.iloc[0])          # 인덱스로 첫 번째 행
print(df.iloc[1:3])        # 인덱스로 2~3번째 행
print(df.loc[0, "name"])   # 레이블로 접근

# ── 필터링  (SQL WHERE / Java stream.filter()) ────────────────────────────
# 서울 거주자
seoul = df[df["city"] == "서울"]
print(seoul)

# 나이 30 이상이고 활성 사용자
filtered = df[(df["age"] >= 30) & (df["active"] == True)]
print(filtered)

# isin  (SQL IN)
big_cities = df[df["city"].isin(["서울", "부산"])]
print(big_cities)

# query 메서드 (SQL 문법처럼)
print(df.query("age > 25 and salary > 50000"))

# ── 정렬  (SQL ORDER BY) ─────────────────────────────────────────────────
print(df.sort_values("salary", ascending=False))
print(df.sort_values(["city", "age"]))   # 여러 컬럼

# ── 집계  (SQL GROUP BY / Java Collectors.groupingBy) ────────────────────
# 도시별 평균 급여
print(df.groupby("city")["salary"].mean())

# 도시별 여러 통계
print(df.groupby("city").agg({
    "salary": ["mean", "max", "count"],
    "age":    "mean"
}))

# ── 컬럼 추가 / 변환 ──────────────────────────────────────────────────────
df["salary_m"] = df["salary"] / 10000        # 만원 단위
df["senior"]   = df["age"] >= 30              # 30세 이상 시니어
df["grade"]    = pd.cut(df["age"],
                        bins=[0, 25, 30, 100],
                        labels=["주니어", "미들", "시니어"])
print(df[["name", "age", "grade", "salary_m"]])

# ── 결측치 처리  (NULL 처리) ──────────────────────────────────────────────
df_with_null = pd.DataFrame({
    "name":   ["Alice", "Bob", None, "Dave"],
    "salary": [50000, None, 80000, 55000],
    "city":   ["서울", "부산", "서울", None],
})

print(df_with_null.isnull())          # 결측치 위치
print(df_with_null.isnull().sum())    # 컬럼별 결측치 수
print(df_with_null.dropna())          # 결측치 행 제거
print(df_with_null.fillna({          # 결측치 채우기
    "salary": df_with_null["salary"].mean(),
    "city":   "미입력",
    "name":   "이름없음"
}))

# ── 파일 입출력 ───────────────────────────────────────────────────────────
# CSV
df.to_csv("/tmp/output.csv", index=False, encoding="utf-8-sig")  # Excel 호환
df_loaded = pd.read_csv("/tmp/output.csv")

# JSON
df.to_json("/tmp/output.json", orient="records", force_ascii=False, indent=2)
df_from_json = pd.read_json("/tmp/output.json")

# ── 실전: API 응답 → DataFrame → 분석 ───────────────────────────────────
orders = [
    {"order_id": 1, "user": "Alice", "product": "노트북",  "amount": 1500000, "date": "2024-01-15"},
    {"order_id": 2, "user": "Bob",   "product": "마우스",  "amount": 50000,   "date": "2024-01-16"},
    {"order_id": 3, "user": "Alice", "product": "키보드",  "amount": 120000,  "date": "2024-01-17"},
    {"order_id": 4, "user": "Charlie","product": "노트북", "amount": 1200000, "date": "2024-01-18"},
    {"order_id": 5, "user": "Bob",   "product": "노트북",  "amount": 1500000, "date": "2024-01-19"},
]

df_orders = pd.DataFrame(orders)
df_orders["date"] = pd.to_datetime(df_orders["date"])

print("\n=== 주문 분석 ===")
print(f"총 주문 수: {len(df_orders)}")
print(f"총 매출: {df_orders['amount'].sum():,}원")
print(f"\n사용자별 매출:")
print(df_orders.groupby("user")["amount"].sum().sort_values(ascending=False))
print(f"\n제품별 주문 수:")
print(df_orders.groupby("product")["order_id"].count())
print(f"\n일별 매출 추이:")
print(df_orders.groupby("date")["amount"].sum())
