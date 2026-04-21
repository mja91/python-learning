# =============================================================================
# tuple (튜플)  |  Java: record (불변 값 객체) / List.of() / 좌표 쌍
# =============================================================================
# tuple은 list와 비슷하지만 생성 후 변경 불가 (immutable)
# 딕셔너리 키, 함수 다중 반환값 등에 활용

# ── 선언 ──────────────────────────────────────────────────────────────────
empty   = ()
point   = (10, 20)
rgb     = (255, 128, 0)
person  = ("민혁", 34, "서울")
single  = (42,)          # ★ 원소 1개짜리는 반드시 쉼표 필요 (42)는 그냥 int임

print(type(point))   # <class 'tuple'>
print(type((42)))    # <class 'int'>   - 주의!
print(type((42,)))   # <class 'tuple'> - 올바른 1개짜리 튜플

# ── 접근 (list와 동일) ────────────────────────────────────────────────────
print(point[0])     # 10
print(point[-1])    # 20
print(point[0:2])   # (10, 20)

# ★ 수정 불가
# point[0] = 99     # TypeError: 'tuple' object does not support item assignment

# ── 언패킹 (Python 특유, 매우 자주 사용) ─────────────────────────────────
x, y = point                     # 기본 언패킹
print(x, y)                      # 10 20

name, age, city = person
print(f"{name}({age}), {city}")  # 민혁(34), 서울

# 나머지 모으기 (Python 3+)
first, *rest = [1, 2, 3, 4, 5]
print(first)   # 1
print(rest)    # [2, 3, 4, 5]

*rest, last = [1, 2, 3, 4, 5]
print(rest)    # [1, 2, 3, 4]
print(last)    # 5

a, *middle, z = [1, 2, 3, 4, 5]
print(a, middle, z)  # 1 [2, 3, 4] 5

# ── 함수 다중 반환값 (Python 특유, 실무에서 매우 자주 사용) ─────────────
# Java: 다중 반환을 위해 별도 클래스/record 필요
def get_min_max(nums):
    return min(nums), max(nums)    # 실제로는 tuple 반환

lo, hi = get_min_max([3, 1, 4, 1, 5, 9])
print(f"최솟값: {lo}, 최댓값: {hi}")  # 최솟값: 1, 최댓값: 9

# divmod도 tuple 반환
quotient, remainder = divmod(17, 5)
print(f"17 ÷ 5 = {quotient} 나머지 {remainder}")

# ── 딕셔너리 키로 사용 (list는 불가) ─────────────────────────────────────
# tuple은 hashable이라 dict 키, set 원소로 사용 가능
cache = {}
cache[(1, 2)] = "좌표(1,2)의 결과"
cache[(3, 4)] = "좌표(3,4)의 결과"
print(cache[(1, 2)])   # '좌표(1,2)의 결과'

# ── 변환 ──────────────────────────────────────────────────────────────────
lst = [1, 2, 3]
t = tuple(lst)     # list → tuple
l = list(t)        # tuple → list
print(t, l)

# ── namedtuple: 이름 있는 tuple (Java record와 유사) ─────────────────────
from collections import namedtuple

Point  = namedtuple("Point", ["x", "y"])
Person = namedtuple("Person", ["name", "age", "city"])

p = Point(10, 20)
print(p.x, p.y)   # 10 20   (인덱스 또는 이름으로 접근)
print(p[0])       # 10

alice = Person("Alice", 30, "Seoul")
print(alice.name, alice.age)   # Alice 30
print(alice._asdict())         # OrderedDict([('name', 'Alice'), ('age', 30), ('city', 'Seoul')])

# ── typing.NamedTuple: 타입 힌트 포함 버전 ────────────────────────────────
from typing import NamedTuple

class Coordinate(NamedTuple):
    lat: float
    lon: float
    label: str = "unknown"    # 기본값 가능

seoul = Coordinate(37.5665, 126.9780, "서울")
print(seoul)        # Coordinate(lat=37.5665, lon=126.978, label='서울')
print(seoul.lat)    # 37.5665

# ── 실전: 함수 반환 패턴 ─────────────────────────────────────────────────
from typing import Tuple, Optional

def parse_pagination(params: dict) -> Tuple[int, int]:
    """쿼리 파라미터에서 page, size 추출"""
    page = max(1, int(params.get("page", 1)))
    size = min(100, int(params.get("size", 20)))
    return page, size

def calculate_offset(page: int, size: int) -> Tuple[int, int]:
    """offset, limit 계산"""
    return (page - 1) * size, size

page, size = parse_pagination({"page": "3", "size": "15"})
offset, limit = calculate_offset(page, size)
print(f"page={page}, size={size}, offset={offset}, limit={limit}")
# page=3, size=15, offset=30, limit=15
