# =============================================================================
# 함수  |  Java: 메서드, lambda, 함수형 인터페이스
# =============================================================================

# ── 기본 함수 ─────────────────────────────────────────────────────────────
def greet(name: str) -> str:           # 타입 힌트는 선택적 (검사 X, 문서화 목적)
    return f"안녕하세요, {name}님!"     # Java: public String greet(String name)

print(greet("민혁"))

# ── 기본값 파라미터  (Java 오버로딩 대신 사용) ───────────────────────────
def create_user(name: str, role: str = "USER", active: bool = True) -> dict:
    return {"name": name, "role": role, "active": active}

print(create_user("민혁"))                      # role="USER", active=True 기본값
print(create_user("Admin", role="ADMIN"))       # 키워드 인수
print(create_user("Guest", "GUEST", False))     # 위치 인수

# ── *args: 가변 위치 인수  (Java: String... args) ─────────────────────────
def sum_all(*nums) -> int:
    return sum(nums)

print(sum_all(1, 2, 3))       # 6
print(sum_all(1, 2, 3, 4, 5)) # 15

# ── **kwargs: 가변 키워드 인수  (Java: Map<String, Object> 에 가까움) ─────
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

print_info(name="민혁", age=34, city="서울")

# 실전: 공통 쿼리 파라미터 처리
def build_query(table: str, **filters) -> str:
    conditions = " AND ".join(f"{k}='{v}'" for k, v in filters.items())
    return f"SELECT * FROM {table}" + (f" WHERE {conditions}" if conditions else "")

print(build_query("users", name="민혁", active=True))
# SELECT * FROM users WHERE name='민혁' AND active='True'

# ── 리스트/딕셔너리 언패킹으로 함수 호출 ────────────────────────────────
def connect(host, port, db):
    print(f"Connecting to {host}:{port}/{db}")

args   = ["localhost", 5432, "mydb"]
kwargs = {"host": "localhost", "port": 5432, "db": "mydb"}

connect(*args)    # 리스트 언패킹
connect(**kwargs) # 딕셔너리 언패킹

# ── 반환값 여러 개  (tuple 반환) ─────────────────────────────────────────
def get_stats(nums: list) -> tuple:
    return min(nums), max(nums), sum(nums) / len(nums)

lo, hi, avg = get_stats([3, 1, 4, 1, 5, 9])
print(f"최솟값={lo}, 최댓값={hi}, 평균={avg:.2f}")

# ── lambda (익명 함수) ─────────────────────────────────────────────────────
# Java: Comparator.comparing(User::getName)
double = lambda x: x * 2
add    = lambda x, y: x + y

print(double(5))    # 10
print(add(3, 4))    # 7

# 정렬, map, filter에서 주로 활용
users = [
    {"name": "Charlie", "age": 30},
    {"name": "Alice",   "age": 25},
    {"name": "Bob",     "age": 35},
]
users.sort(key=lambda u: u["age"])
print([u["name"] for u in users])   # ['Alice', 'Charlie', 'Bob']

# map / filter  (Java: stream().map().filter())
nums = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, nums))  # [2, 4, 6, 8, 10]
evens   = list(filter(lambda x: x % 2 == 0, nums))  # [2, 4]
print(doubled, evens)

# ★ 실무에서는 lambda보다 컴프리헨션이 더 Pythonic
doubled2 = [x * 2 for x in nums]
evens2   = [x for x in nums if x % 2 == 0]

# ── 함수를 변수에 저장 / 고차함수 ────────────────────────────────────────
# Java: Function<Integer, Integer>, Consumer<T>

def apply(func, value):         # 함수를 인수로 받음
    return func(value)

def square(x): return x ** 2
def cube(x):   return x ** 3

print(apply(square, 5))   # 25
print(apply(cube, 3))     # 27

# 함수 반환
def make_multiplier(factor: int):
    def multiplier(x):
        return x * factor      # factor를 클로저로 캡처
    return multiplier

triple = make_multiplier(3)
print(triple(10))   # 30

# ── 데코레이터 (Spring Boot의 @Annotation과 유사 개념) ───────────────────
# Java: @Transactional, @Cacheable, @PreAuthorize 등과 유사

import time
import functools

# 실행 시간 측정 데코레이터
def timer(func):
    @functools.wraps(func)    # 원래 함수 이름/docstring 유지
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"[{func.__name__}] {elapsed:.4f}초 소요")
        return result
    return wrapper

@timer
def slow_function(n: int) -> int:
    time.sleep(0.01)
    return sum(range(n))

print(slow_function(1000))

# 로깅 데코레이터
def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"▶ {func.__name__}({args}, {kwargs}) 호출")
        result = func(*args, **kwargs)
        print(f"◀ {func.__name__} 반환: {result}")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

add(3, 5)

# 인수를 받는 데코레이터 (Java: @Retry(maxAttempts=3) 같은 것)
def retry(max_attempts: int = 3, delay: float = 0.1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    print(f"시도 {attempt}/{max_attempts} 실패: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.05)
def unstable_api_call(fail_count=[0]):
    fail_count[0] += 1
    if fail_count[0] < 3:
        raise ConnectionError("연결 실패")
    return "성공!"

print(unstable_api_call())

# 데코레이터 여러 개 적용  (아래서 위 순서로 실행)
@timer
@log_calls
def compute(n):
    return sum(range(n))

# ── 타입 힌트 심화  (mypy로 정적 분석 가능) ─────────────────────────────
from typing import Optional, List, Dict, Union, Callable, Any

def find_user(
    user_id: int,
    db: Dict[int, dict]
) -> Optional[dict]:                    # None 반환 가능
    return db.get(user_id)

def process_items(
    items: List[str],
    transform: Callable[[str], str]     # 함수 타입 힌트
) -> List[str]:
    return [transform(item) for item in items]

result = process_items(["hello", "world"], str.upper)
print(result)   # ['HELLO', 'WORLD']

# Union: 여러 타입 허용  (Python 3.10+: int | str)
def to_int(value: Union[int, str]) -> int:
    return int(value)

print(to_int("42"))   # 42
print(to_int(42))     # 42
