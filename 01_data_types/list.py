# =============================================================================
# list (리스트)  |  Java: List<T> / ArrayList<T>
# =============================================================================
# Python list는 Java ArrayList와 유사하지만 타입 혼합 가능, 슬라이싱 지원

# ── 선언 ──────────────────────────────────────────────────────────────────
empty   = []                         # Java: new ArrayList<>()
nums    = [1, 2, 3, 4, 5]
mixed   = [1, "hello", True, None]   # Java와 달리 타입 혼합 가능
nested  = [[1, 2], [3, 4], [5, 6]]   # 중첩 리스트

print(type(nums))    # <class 'list'>
print(len(nums))     # 5   (Java .size())

# ── 인덱싱 & 슬라이싱 ─────────────────────────────────────────────────────
a = [10, 20, 30, 40, 50]

print(a[0])     # 10   첫 번째   (Java .get(0))
print(a[-1])    # 50   마지막    (Java .get(list.size()-1))
print(a[-2])    # 40   뒤에서 두 번째

# 슬라이싱 [start:end:step]  (end는 미포함)
print(a[1:4])   # [20, 30, 40]
print(a[:3])    # [10, 20, 30]   처음부터 3개
print(a[2:])    # [30, 40, 50]   3번째부터 끝
print(a[::2])   # [10, 30, 50]   2칸씩 (짝수 인덱스)
print(a[::-1])  # [50, 40, 30, 20, 10]  뒤집기

# ── CRUD 메서드 ───────────────────────────────────────────────────────────
a = [1, 2, 3]

# 추가
a.append(4)          # 끝에 추가  (Java .add(4))     → [1,2,3,4]
a.insert(1, 99)      # 인덱스에 삽입 (Java .add(1, 99)) → [1,99,2,3,4]
a.extend([5, 6])     # 다른 리스트 합치기 (Java .addAll()) → [1,99,2,3,4,5,6]
print(a)

# 제거
a.remove(99)         # 값으로 제거 (Java .remove(Integer.valueOf(99)))
popped = a.pop()     # 마지막 제거 후 반환 (Java .remove(list.size()-1))
popped2 = a.pop(0)   # 인덱스로 제거 후 반환 (Java .remove(0))
print(a, popped, popped2)

# 수정
a[0] = 100           # 인덱스로 수정 (Java .set(0, 100))

# 검색
nums = [10, 20, 30, 20, 40]
print(20 in nums)        # True   (Java .contains(20))
print(nums.index(20))    # 1      (Java .indexOf(20))
print(nums.count(20))    # 2      (등장 횟수)

# ── 정렬 ──────────────────────────────────────────────────────────────────
nums = [3, 1, 4, 1, 5, 9, 2, 6]

# sort(): 원본 수정  (Java Collections.sort())
nums.sort()
print(nums)             # [1, 1, 2, 3, 4, 5, 6, 9]

nums.sort(reverse=True) # 내림차순
print(nums)             # [9, 6, 5, 4, 3, 2, 1, 1]

# sorted(): 원본 유지, 새 리스트 반환  (Java stream().sorted())
original = [3, 1, 4, 1, 5]
new_list = sorted(original)
print(original)   # [3, 1, 4, 1, 5]  (원본 그대로)
print(new_list)   # [1, 1, 3, 4, 5]

# key 함수로 정렬
users = [
    {"name": "Charlie", "age": 30},
    {"name": "Alice",   "age": 25},
    {"name": "Bob",     "age": 35},
]
users.sort(key=lambda u: u["age"])          # 나이 오름차순
print([u["name"] for u in users])           # ['Alice', 'Charlie', 'Bob']

users.sort(key=lambda u: u["name"])         # 이름 알파벳순
users.sort(key=lambda u: (-u["age"], u["name"]))  # 나이 내림차순, 같으면 이름순

# ── 리스트 컴프리헨션 (Python 특유, 매우 중요) ────────────────────────────
# Java: list.stream().map(...).collect(Collectors.toList())

# 기본
squares = [x ** 2 for x in range(1, 6)]
print(squares)   # [1, 4, 9, 16, 25]

# 조건 필터
evens = [x for x in range(10) if x % 2 == 0]
print(evens)     # [0, 2, 4, 6, 8]

# 변환 + 필터 동시
result = [x ** 2 for x in range(10) if x % 2 == 0]
print(result)    # [0, 4, 16, 36, 64]

# 중첩 (행렬 평탄화)
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [n for row in matrix for n in row]
print(flat)      # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# ── 유용한 내장 함수 ──────────────────────────────────────────────────────
nums = [3, 1, 4, 1, 5, 9]

print(sum(nums))     # 23   (Java stream().mapToInt(x->x).sum())
print(max(nums))     # 9
print(min(nums))     # 1
print(len(nums))     # 6

# zip: 두 리스트를 묶어서 동시 순회  (Java stream + zip 없음, 직접 구현)
names  = ["Alice", "Bob", "Charlie"]
scores = [90, 85, 92]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# enumerate: 인덱스 포함 순회  (Java: for(int i=0; i<list.size(); i++))
for i, name in enumerate(names, start=1):
    print(f"{i}. {name}")

# ── 복사 주의사항 ─────────────────────────────────────────────────────────
original = [1, 2, 3]

# 얕은 복사 (shallow copy)
a = original         # 참조 복사  (같은 객체!)
b = original.copy()  # 얕은 복사  (Java new ArrayList<>(original))
c = original[:]      # 슬라이싱 복사 (얕은 복사)

a.append(99)
print(original)  # [1, 2, 3, 99]  a는 같은 객체이므로 원본도 변경됨!
print(b)         # [1, 2, 3]      b는 독립적

# 깊은 복사 (deep copy)
import copy
nested = [[1, 2], [3, 4]]
deep = copy.deepcopy(nested)
nested[0][0] = 99
print(nested)   # [[99, 2], [3, 4]]
print(deep)     # [[1, 2], [3, 4]]  영향 없음

# ── 실전: 페이지네이션 슬라이싱 ──────────────────────────────────────────
all_items = list(range(1, 51))  # 1~50
page, size = 2, 10
page_items = all_items[(page - 1) * size : page * size]
print(page_items)  # [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
