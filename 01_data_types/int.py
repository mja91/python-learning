# =============================================================================
# int (정수)  |  Java: int / long / BigInteger
# =============================================================================
# ★ Python int는 크기 제한 없음 (자동으로 BigInteger처럼 동작)

# ── 선언 ──────────────────────────────────────────────────────────────────
a = 10
b = 3
googol = 10 ** 100      # Java에서는 BigInteger 필요, Python은 그냥 됨

print(type(a))          # <class 'int'>   (Java: a.getClass())

# ── 사칙연산 ───────────────────────────────────────────────────────────────
print(a + b)   # 13
print(a - b)   # 7
print(a * b)   # 30
print(a / b)   # 3.3333...  ★ Java int/int=3 과 달리 항상 float 반환!
print(a // b)  # 3          (정수 나눗셈 - Java int/int 결과와 같음)
print(a % b)   # 1          (나머지)
print(a ** b)  # 1000       (거듭제곱 - Java Math.pow())
print(-a)      # -10

# ★ Python에는 ++, -- 없음!  → x += 1 사용

# ── 복합 대입 연산자 ────────────────────────────────────────────────────────
x = 10
x += 5   # 15
x -= 3   # 12
x *= 2   # 24
x //= 5  # 4   (정수 나눗셈 대입)
x **= 3  # 64  (거듭제곱 대입)
print(x)

# ── 비교 (Java와 동일) ────────────────────────────────────────────────────
print(a > b)   # True
print(a == 10) # True

# ★ Python 특유: 연쇄 비교
score = 85
print(80 <= score < 90)  # True  (Java: score >= 80 && score < 90)

# ── 형변환 ────────────────────────────────────────────────────────────────
print(int("42"))    # 42    (Java Integer.parseInt())
print(int(3.9))     # 3     (소수점 버림! 반올림 아님)
print(int(True))    # 1
print(int(False))   # 0

# ── 진법 변환 ─────────────────────────────────────────────────────────────
print(bin(10))          # '0b1010'  (2진수)
print(hex(255))         # '0xff'   (16진수)
print(int('ff', 16))    # 255      (16진수 → int)
print(int('1010', 2))   # 10       (2진수 → int)

# ── 내장 함수 ─────────────────────────────────────────────────────────────
print(abs(-42))          # 42           (Java Math.abs())
print(max(1, 5, 3))      # 5            (Java Math.max() - 인자 여러 개 가능)
print(min(1, 5, 3))      # 1
print(divmod(10, 3))     # (3, 1)       몫·나머지 동시 반환 (Java 없음)
print(round(3.567, 2))   # 3.57         소수점 N자리 반올림

# ── 실전: 페이지네이션 ─────────────────────────────────────────────────────
total_items = 105
page_size   = 10
page        = 3

total_pages = (total_items + page_size - 1) // page_size   # 올림 나눗셈
offset      = (page - 1) * page_size
print(f"총 {total_pages}페이지, offset={offset}, limit={page_size}")
# 총 11페이지, offset=20, limit=10
