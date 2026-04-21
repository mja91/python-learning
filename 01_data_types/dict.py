# =============================================================================
# dict (딕셔너리)  |  Java: Map<K,V> / HashMap<K,V>
# =============================================================================
# Python dict는 3.7+ 버전부터 삽입 순서 유지 (Java LinkedHashMap과 유사)

# ── 선언 ──────────────────────────────────────────────────────────────────
empty = {}                               # Java: new HashMap<>()
user = {
    "id":    1,
    "name":  "민혁",
    "age":   34,
    "active": True
}

print(type(user))    # <class 'dict'>
print(len(user))     # 4   (Java .size())

# ── 읽기 ──────────────────────────────────────────────────────────────────
print(user["name"])                   # '민혁'  (Java .get("name"))
print(user.get("email"))              # None    (없으면 None - Java .get() → null)
print(user.get("email", "없음"))      # '없음'  (Java .getOrDefault("email", "없음"))

# 키 존재 확인  (Java .containsKey())
print("name" in user)        # True
print("email" in user)       # False
print("email" not in user)   # True

# 값 존재 확인  (Java .containsValue())
print("민혁" in user.values())  # True

# ── 쓰기 / 수정 / 삭제 ────────────────────────────────────────────────────
user["email"] = "minhyuk@gmail.com"   # 추가 or 수정  (Java .put())

# 없을 때만 추가  (Java .putIfAbsent())
user.setdefault("role", "USER")       # role이 없으면 "USER"로 세팅

# 삭제
del user["active"]                    # 키 삭제  (Java .remove())
removed = user.pop("role")            # 삭제 후 값 반환
removed2 = user.pop("nothing", "기본값")  # 없을 때 기본값 반환

# ── 반복 ──────────────────────────────────────────────────────────────────
d = {"a": 1, "b": 2, "c": 3}

for key in d:                  # 키만 순회  (Java for (K key : map.keySet()))
    print(key)

for value in d.values():       # 값만 순회  (Java for (V v : map.values()))
    print(value)

for key, value in d.items():   # 키-값 쌍 순회  (Java for (Map.Entry<K,V> e : map.entrySet()))
    print(f"{key}: {value}")

# ── 병합 ──────────────────────────────────────────────────────────────────
defaults = {"theme": "dark", "lang": "ko", "size": 10}
overrides = {"lang": "en", "size": 20}

# 방법 1: update (Java .putAll())
merged = defaults.copy()
merged.update(overrides)
print(merged)   # {'theme': 'dark', 'lang': 'en', 'size': 20}

# 방법 2: ** 언패킹 (Python 3.5+)
merged2 = {**defaults, **overrides}
print(merged2)  # 동일 결과  (overrides가 덮어씀)

# 방법 3: | 연산자 (Python 3.9+)
merged3 = defaults | overrides
print(merged3)  # 동일 결과

# ── 딕셔너리 컴프리헨션 ──────────────────────────────────────────────────
# Java: Map.Entry stream().collect(Collectors.toMap(...))

# 리스트 → 딕셔너리
keys   = ["a", "b", "c"]
values = [1, 2, 3]
d = {k: v for k, v in zip(keys, values)}
print(d)   # {'a': 1, 'b': 2, 'c': 3}

# 값 변환
prices    = {"apple": 1000, "banana": 500, "cherry": 2000}
discounted = {k: int(v * 0.9) for k, v in prices.items()}
print(discounted)   # {'apple': 900, 'banana': 450, 'cherry': 1800}

# 필터링  (Java stream().filter())
expensive = {k: v for k, v in prices.items() if v >= 1000}
print(expensive)    # {'apple': 1000, 'cherry': 2000}

# ── 중첩 딕셔너리 ─────────────────────────────────────────────────────────
config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "mydb"
    },
    "redis": {
        "host": "localhost",
        "port": 6379
    }
}

print(config["database"]["host"])   # 'localhost'

# 안전하게 중첩 접근
db_host = config.get("database", {}).get("host", "localhost")
print(db_host)

# ── 실전: API 응답 포맷 만들기 ────────────────────────────────────────────
def make_response(data=None, message="OK", success=True, status=200):
    return {
        "success": success,
        "status":  status,
        "message": message,
        "data":    data
    }

response = make_response(data={"id": 1, "name": "민혁"})
print(response)
# {'success': True, 'status': 200, 'message': 'OK', 'data': {'id': 1, 'name': '민혁'}}

# ── 실전: 그룹핑 ──────────────────────────────────────────────────────────
# Java: stream().collect(Collectors.groupingBy(...))
orders = [
    {"user": "Alice", "amount": 100},
    {"user": "Bob",   "amount": 200},
    {"user": "Alice", "amount": 150},
    {"user": "Bob",   "amount": 300},
]

grouped = {}
for order in orders:
    user = order["user"]
    grouped.setdefault(user, []).append(order["amount"])

print(grouped)  # {'Alice': [100, 150], 'Bob': [200, 300]}
totals = {user: sum(amounts) for user, amounts in grouped.items()}
print(totals)   # {'Alice': 250, 'Bob': 500}

# ── 실전: 빈도 카운트 ─────────────────────────────────────────────────────
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]

# 방법 1: setdefault
count = {}
for w in words:
    count[w] = count.get(w, 0) + 1
print(count)   # {'apple': 3, 'banana': 2, 'cherry': 1}

# 방법 2: Counter (더 Pythonic)
from collections import Counter
count2 = Counter(words)
print(count2)               # Counter({'apple': 3, 'banana': 2, 'cherry': 1})
print(count2.most_common(2))  # [('apple', 3), ('banana', 2)]
