# =============================================================================
# bool (불리언) & None  |  Java: boolean / null
# =============================================================================

# ── bool 기본 ─────────────────────────────────────────────────────────────
a = True
b = False

print(type(a))   # <class 'bool'>
print(int(True)) # 1  (bool은 int의 서브클래스)
print(int(False))# 0

# ── 논리 연산자 ───────────────────────────────────────────────────────────
# Java: &&  ||  !
# Python: and  or  not
print(True and False)   # False
print(True or False)    # True
print(not True)         # False

# ── 비교 연산자 ───────────────────────────────────────────────────────────
print(10 == 10)   # True
print(10 != 5)    # True
print(10 > 5)     # True
print("a" < "b")  # True  (사전 순)

# ★ Python 특유: 연쇄 비교 (Java 불가)
score = 85
print(60 <= score < 90)   # True  (Java: score >= 60 && score < 90)

# ── ★ Truthy / Falsy (Python 특유 개념) ──────────────────────────────────
# 다음 값들이 False로 평가됨 (Java는 boolean만 조건식에 사용):
falsy_values = [
    False,      # bool False
    0,          # 정수 0
    0.0,        # 실수 0.0
    "",         # 빈 문자열
    [],         # 빈 리스트
    {},         # 빈 딕셔너리
    (),         # 빈 튜플
    set(),      # 빈 셋
    None,       # None
]

for v in falsy_values:
    print(f"bool({v!r:10}) = {bool(v)}")  # 모두 False

x = falsy_values[0]  # False
y = falsy_values[1]  # 0
print(f"bool({x!r}) == bool({y!r}) → {bool(x) == bool(y)}") # bool(False) == bool(0) → True

# 실무 활용 - Java: if (list != null && !list.isEmpty())
items = []
if not items:
    print("목록이 비어있습니다")   # Python다운 방식

name = "  "
if not name.strip():
    print("이름이 없습니다")       # Java .isBlank() 대응
else:
    print("이름 있음")

# ── 단락 평가 (Short-circuit evaluation) ─────────────────────────────────
# Java와 동일하게 동작하지만 Python은 값을 반환함

# or: 첫 번째 Truthy 값 반환
print("" or "기본값")          # '기본값'  (Java: str != null ? str : "기본값")
print("실제값" or "기본값")    # '실제값'

# and: 첫 번째 Falsy 값 반환, 모두 Truthy면 마지막 값
print(None and "무언가")       # None
print("값" and "다른값")       # '다른값'

# ── 실전: None 처리 ─────────────────────────────────────────────────────
# None = Java의 null

data = None

# None 비교는 is / is not 사용 (Java의 == null / != null)
print(data is None)      # True   (권장)
print(data is not None)  # False  (권장)
print(data == None)      # True   (동작하지만 비권장)

# None 안전 처리 - Java Optional 대응
def get_user_name(user: dict) -> str:
    # Java: Optional.ofNullable(user).map(u -> u.get("name")).orElse("unknown")
    return user.get("name") if user else "unknown"

print(get_user_name({"name": "MH"}))  # MH
print(get_user_name(None))             # unknown
print(get_user_name({}))               # unknown

# ── isinstance (Java의 instanceof) ───────────────────────────────────────
x = 42
print(isinstance(x, int))          # True
print(isinstance(x, (int, float))) # True  (여러 타입 동시 확인)
print(isinstance(x, str))          # False

# ── 비교 연산자 심화 ──────────────────────────────────────────────────────
# == : 값 비교  (Java .equals())
# is : 동일 객체 비교  (Java ==)

a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)   # True  (값이 같음)
print(a is b)   # False (서로 다른 객체)
print(a is c)   # True  (같은 객체 참조)

# ★ None, True, False는 싱글톤이므로 is 사용 권장
val = None
if val is None:     # O 권장
    pass
if val == None:     # X 비권장 (동작은 하지만)
    pass

# is는 None 비교 시에만 주로 활용, 이외 값 비교는 "==" 활용