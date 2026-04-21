# =============================================================================
# float (실수)  |  Java: double / BigDecimal
# =============================================================================
# Python float = Java double (64비트 IEEE 754)
# ★ 금융 계산은 반드시 Decimal 모듈 사용!

# ── 선언 ──────────────────────────────────────────────────────────────────
a = 3.14
b = 1e6       # 1,000,000  (과학적 표기법)
c = 1.5e-3    # 0.0015

print(type(a))   # <class 'float'>

# ── ★ 부동소수점 함정 (Java도 동일한 문제) ────────────────────────────────
print(0.1 + 0.2)          # 0.30000000000000004  (!!!)
print(0.1 + 0.2 == 0.3)   # False  → 직접 == 비교 금지!

import math
print(math.isclose(0.1 + 0.2, 0.3))  # True  (올바른 비교 방법)

# ── ★ 금융 계산: Decimal (Java의 BigDecimal) ──────────────────────────────
from decimal import Decimal, ROUND_HALF_UP

price    = Decimal("19.99")
tax_rate = Decimal("0.1")
total    = price + price * tax_rate         # 21.989

# 소수점 2자리 반올림 (일반적인 반올림)
rounded = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
print(rounded)   # 21.99

# Java: new BigDecimal("19.99").add(new BigDecimal("19.99").multiply(new BigDecimal("0.1")))

# ── 형변환 ────────────────────────────────────────────────────────────────
print(float(10))       # 10.0   (int → float,  Java (double)10)
print(float("3.14"))   # 3.14   (str → float,  Java Double.parseDouble())
print(int(3.9))        # 3      (float → int,  버림! 반올림 아님)

# ── 수학 함수 ─────────────────────────────────────────────────────────────
import math

print(math.floor(3.7))   # 3      (내림 - Java Math.floor())
print(math.ceil(3.2))    # 4      (올림 - Java Math.ceil())
print(math.sqrt(16))     # 4.0    (제곱근 - Java Math.sqrt())
print(math.log10(1000))  # 3.0
print(math.pi)           # 3.141592653589793
print(math.inf)          # inf    (Java Double.POSITIVE_INFINITY)
print(math.isnan(float('nan')))  # True  (Java Double.isNaN())

# ── f-string 포매팅 ───────────────────────────────────────────────────────
value = 1234567.89

print(f"{value:.2f}")      # 1234567.89   (소수 2자리)
print(f"{value:,.2f}")     # 1,234,567.89 (천 단위 구분자)
print(f"{value:.2e}")      # 1.23e+06     (과학적 표기)
print(f"{0.156:.1%}")      # 15.6%        (퍼센트)
print(f"{value:>15.2f}")   # 오른쪽 정렬 15자리

# ── Python round() 주의사항: 은행 반올림 ─────────────────────────────────
# 0.5일 때 가장 가까운 짝수로 반올림 (Banker's rounding)
print(round(0.5))   # 0  (!!!)  일반적인 반올림과 다름
print(round(1.5))   # 2
print(round(2.5))   # 2  (!!!)

# 일반 반올림이 필요하면 Decimal 사용
print(float(Decimal("2.5").quantize(Decimal("1"), rounding=ROUND_HALF_UP)))  # 3.0

# ── 실전: 할인 계산 ───────────────────────────────────────────────────────
original = 29900
discount = 0.15

final = original * (1 - discount)
print(f"원가: {original:,}원")
print(f"할인율: {discount:.0%}")
print(f"최종가: {final:,.0f}원")   # 25,415원
