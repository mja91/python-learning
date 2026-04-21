# =============================================================================
# 제어 흐름: 조건문 / 반복문 / 컴프리헨션  |  Java if/for/while과 비교
# =============================================================================

# ── if / elif / else ──────────────────────────────────────────────────────
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:       # Java: else if
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
print(grade)   # B

# 삼항 연산자  (Java: score >= 60 ? "합격" : "불합격")
result = "합격" if score >= 60 else "불합격"
print(result)

# ── match-case (Python 3.10+, Java의 switch-case보다 강력) ───────────────
status_code = 404

match status_code:
    case 200:
        print("OK")
    case 404:
        print("Not Found")
    case 500:
        print("Internal Server Error")
    case _:                      # Java: default
        print("Unknown")

# 타입 매칭 + 조건 가드
def process(value):
    match value:
        case int(n) if n < 0:
            return f"음수 정수: {n}"
        case int(n):
            return f"양수 정수: {n}"
        case str(s) if len(s) > 10:
            return f"긴 문자열"
        case str(s):
            return f"문자열: {s}"
        case None:
            return "None"
        case _:
            return "기타"

print(process(-5))      # 음수 정수: -5
print(process("hi"))    # 문자열: hi

# dict 구조 매칭  (API 응답 처리에 유용)
event = {"type": "click", "x": 10, "y": 20}

match event:
    case {"type": "click", "x": x, "y": y}:
        print(f"클릭: ({x}, {y})")
    case {"type": "keypress", "key": key}:
        print(f"키 입력: {key}")

# ── for 반복문 ────────────────────────────────────────────────────────────
items = ["apple", "banana", "cherry"]

# 기본 for-each  (Java: for (String item : items))
for item in items:
    print(item)

# 인덱스 포함  (Java: for(int i=0; i<items.size(); i++))
for i, item in enumerate(items):
    print(f"{i}: {item}")

for i, item in enumerate(items, start=1):   # 1부터 시작
    print(f"{i}. {item}")

# 범위  (Java: for(int i=0; i<5; i++))
for i in range(5):          # 0, 1, 2, 3, 4
    print(i, end=" ")
print()

for i in range(1, 6):       # 1, 2, 3, 4, 5
    print(i, end=" ")
print()

for i in range(0, 10, 2):   # 0, 2, 4, 6, 8  (step=2)
    print(i, end=" ")
print()

for i in range(10, 0, -1):  # 10, 9, ..., 1  (역방향)
    print(i, end=" ")
print()

# 두 리스트 동시 순회  (Java: 직접 구현 필요)
names  = ["Alice", "Bob", "Charlie"]
scores = [90, 85, 92]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# 딕셔너리 순회
user = {"name": "민혁", "age": 34, "city": "서울"}
for key, value in user.items():
    print(f"{key}: {value}")

# ── while ─────────────────────────────────────────────────────────────────
count = 0
while count < 5:
    print(count, end=" ")
    count += 1    # ★ count++ 없음!
print()

# break / continue  (Java와 동일)
for i in range(10):
    if i == 3:
        continue   # 건너뜀
    if i == 7:
        break      # 중단
    print(i, end=" ")
print()   # 0 1 2 4 5 6

# for-else: 루프가 break 없이 완료되면 else 실행  (Java에 없음)
nums = [1, 3, 5, 7]
for n in nums:
    if n % 2 == 0:
        print(f"{n}은 짝수")
        break
else:
    print("짝수가 없습니다")   # break 없이 완료 → else 실행

# ── 컴프리헨션 (Python 핵심 기능) ─────────────────────────────────────────
# Java: stream().map(...).filter(...).collect(...)

# 리스트 컴프리헨션
squares     = [x ** 2 for x in range(1, 6)]
even_squares = [x ** 2 for x in range(10) if x % 2 == 0]
print(squares)        # [1, 4, 9, 16, 25]
print(even_squares)   # [0, 4, 16, 36, 64]

# 딕셔너리 컴프리헨션
word_lengths = {word: len(word) for word in ["hello", "world", "python"]}
print(word_lengths)   # {'hello': 5, 'world': 5, 'python': 6}

# 셋 컴프리헨션
unique_lengths = {len(w) for w in ["hi", "hey", "hello", "world"]}
print(unique_lengths)  # {2, 3, 5}

# 제너레이터 표현식 (메모리 효율적 - 즉시 계산하지 않음)
# Java: stream() - 지연 평가
gen = (x ** 2 for x in range(1_000_000))   # 메모리에 바로 올리지 않음
print(next(gen))   # 0
print(next(gen))   # 1
print(sum(x for x in range(100) if x % 2 == 0))  # 2450

# ── 실전: 데이터 처리 파이프라인 ──────────────────────────────────────────
users = [
    {"name": "Alice",   "age": 17, "score": 90},
    {"name": "Bob",     "age": 25, "score": 55},
    {"name": "Charlie", "age": 30, "score": 82},
    {"name": "Dave",    "age": 22, "score": 67},
]

# 성인 중 점수 60 이상인 사람의 이름 목록, 점수 내림차순
result = sorted(
    [u["name"] for u in users if u["age"] >= 18 and u["score"] >= 60],
    key=lambda name: next(u["score"] for u in users if u["name"] == name),
    reverse=True
)
print(result)   # ['Charlie', 'Dave']

# Java 스타일로 비교:
# users.stream()
#   .filter(u -> u.getAge() >= 18 && u.getScore() >= 60)
#   .sorted(Comparator.comparingInt(User::getScore).reversed())
#   .map(User::getName)
#   .collect(Collectors.toList());
