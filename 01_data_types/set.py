# =============================================================================
# set (셋)  |  Java: Set<T> / HashSet<T>
# =============================================================================
# 중복 없음, 순서 없음 (Python 3.7+도 set은 순서 미보장)

# ── 선언 ──────────────────────────────────────────────────────────────────
# ★ {} 는 빈 dict!  빈 set은 반드시 set() 사용
empty  = set()                       # Java: new HashSet<>()
tags   = {"python", "java", "sql"}
nums   = {1, 2, 3, 2, 1}            # 중복 자동 제거

print(type(tags))   # <class 'set'>
print(nums)         # {1, 2, 3}  (중복 제거됨)
print(len(tags))    # 3   (Java .size())

# ── CRUD ──────────────────────────────────────────────────────────────────
tags.add("docker")        # 추가  (Java .add())
tags.discard("java")      # 삭제 (없어도 에러 없음)  (Java .remove())
tags.remove("sql")        # 삭제 (없으면 KeyError)

print("python" in tags)   # True  (Java .contains())
popped = tags.pop()       # 임의의 원소 제거 후 반환 (순서 없으므로 임의)

# ── 집합 연산 (Python 특유의 강점) ───────────────────────────────────────
a = {1, 2, 3, 4, 5}
b = {3, 4, 5, 6, 7}

# 합집합 (union)  Java: addAll()
print(a | b)           # {1, 2, 3, 4, 5, 6, 7}
print(a.union(b))      # 동일

# 교집합 (intersection)  Java: retainAll()
print(a & b)                  # {3, 4, 5}
print(a.intersection(b))      # 동일

# 차집합 (difference)  Java: removeAll()
print(a - b)              # {1, 2}  (a에만 있는 것)
print(b - a)              # {6, 7}  (b에만 있는 것)
print(a.difference(b))    # {1, 2}

# 대칭 차집합 (symmetric difference)  - 둘 중 하나에만 있는 것
print(a ^ b)                         # {1, 2, 6, 7}
print(a.symmetric_difference(b))     # 동일

# 부분집합 / 상위집합
small = {3, 4}
print(small.issubset(a))     # True  (small ⊆ a)
print(a.issuperset(small))   # True  (a ⊇ small)
print(a.isdisjoint({8, 9}))  # True  (공통 원소 없음)

# ── 변환 ──────────────────────────────────────────────────────────────────
lst = [1, 2, 3, 2, 1, 3]
unique = list(set(lst))      # 중복 제거 후 리스트 (순서 미보장)
print(unique)                # [1, 2, 3] (순서는 다를 수 있음)

# 순서 유지하며 중복 제거 (Python 3.7+)
seen = list(dict.fromkeys(lst))   # dict는 삽입 순서 유지 → 키만 추출
print(seen)   # [1, 2, 3]  (원래 순서 유지)

# ── frozenset: 불변 set (hashable, dict 키로 사용 가능) ──────────────────
fs = frozenset([1, 2, 3])
# fs.add(4)  # AttributeError: frozenset은 수정 불가

cache = {frozenset(["read", "write"]): "editor"}
print(cache[frozenset(["write", "read"])])  # 'editor'  (순서 무관)

# ── set 컴프리헨션 ────────────────────────────────────────────────────────
words = ["hello", "world", "hello", "python"]
unique_lengths = {len(w) for w in words}
print(unique_lengths)   # {5, 6}  (중복 길이 제거)

# ── 실전: 권한 체크 ───────────────────────────────────────────────────────
def check_permissions(user_roles: set, required: set) -> bool:
    return required.issubset(user_roles)   # 필요 권한이 모두 있는지 확인

user_roles = {"read", "write", "admin"}
print(check_permissions(user_roles, {"read", "write"}))  # True
print(check_permissions(user_roles, {"read", "delete"})) # False

# ── 실전: 방문자 수집 / 중복 URL 제거 ───────────────────────────────────
visited = set()
urls = [
    "https://example.com/a",
    "https://example.com/b",
    "https://example.com/a",   # 중복
    "https://example.com/c",
]

new_urls = [url for url in urls if url not in visited and not visited.add(url)]
print(new_urls)
# ['https://example.com/a', 'https://example.com/b', 'https://example.com/c']
