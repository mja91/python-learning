# =============================================================================
# str (문자열)  |  Java: String
# =============================================================================
# Python str은 Java String과 비슷하나 슬라이싱, 반복 등 강력한 기능 추가

# ── 선언 ──────────────────────────────────────────────────────────────────
s1 = "hello"
s2 = 'world'
s3 = """여러 줄
문자열 가능"""        # Java: String.join("\n", ...) 또는 text block
s4 = r"C:\Users\nash" # raw string: 백슬래시를 이스케이프로 처리하지 않음

# ── f-string (Java의 String.format / formatted string) ───────────────────
name = "민혁"
age  = 34
score = 95.678

print(f"이름: {name}, 나이: {age}")      # 기본
print(f"점수: {score:.2f}")              # 소수점 2자리 → 95.68
print(f"점수: {score:06.1f}")            # 총 6자리, 0 패딩 → 0095.7
print(f"{age:>10}")                      # 오른쪽 정렬 10자리
print(f"{name!r}")                       # repr() 형식 → '민혁'

# ── 기본 연산 ─────────────────────────────────────────────────────────────
print("hello" + " " + "world")   # 연결  (Java +)
print("ha" * 3)                   # 반복  → hahaha  (Java 없음)
print(len("hello"))               # 5     (Java .length())
print("l" in "hello")             # True  (Java .contains())
print("x" not in "hello")        # True

# ── 인덱싱 & 슬라이싱 ─────────────────────────────────────────────────────
s = "Python"
print(s[0])     # 'P'   첫 번째
print(s[-1])    # 'n'   마지막 (Java: s.charAt(s.length()-1))
print(s[1:4])   # 'yth'  s[start:end]  (end 미포함)
print(s[:3])    # 'Pyt'  처음부터 3번째까지
print(s[3:])    # 'hon'  4번째부터 끝까지
print(s[::-1])  # 'nohtyP'  문자열 뒤집기  (Java: new StringBuilder(s).reverse())

# ── 주요 메서드 ───────────────────────────────────────────────────────────
s = "  Hello, World!  "

# 대소문자
print(s.upper())        # 대문자  (Java .toUpperCase())
print(s.lower())        # 소문자  (Java .toLowerCase())
print("hello world".title())  # Hello World  (각 단어 첫글자 대문자)

# 공백 제거
print(s.strip())        # "Hello, World!"  (Java .trim())
print(s.lstrip())       # 왼쪽 공백 제거
print(s.rstrip())       # 오른쪽 공백 제거

# 검색
s2 = "Hello, World!"
print(s2.find("World"))     # 7   (Java .indexOf())  없으면 -1
print(s2.index("World"))    # 7   없으면 ValueError 발생
print(s2.count("l"))        # 3   (문자 개수)
print(s2.startswith("Hello"))  # True  (Java .startsWith())
print(s2.endswith("!"))        # True  (Java .endsWith())

# 치환 & 분리
print(s2.replace("World", "Python"))  # "Hello, Python!" (Java .replace())
parts = "a,b,c,d".split(",")          # ['a', 'b', 'c', 'd']  (Java .split(","))
print(parts)
print(",".join(parts))                # "a,b,c,d"  (Java String.join(",", list))

# 검사
print("123".isdigit())    # True   (Java Character.isDigit()와 다름, 전체 확인)
print("abc".isalpha())    # True
print("abc123".isalnum()) # True
print("  ".isspace())     # True

# 패딩
print("42".zfill(5))       # "00042"   (Java String.format("%05d", 42))
print("hi".ljust(10, '-')) # "hi--------"
print("hi".rjust(10, '-')) # "--------hi"
print("hi".center(10, '-'))# "----hi----"

# ── 문자열 비교 ───────────────────────────────────────────────────────────
# ★ Java와 달리 Python은 == 로 문자열 내용 비교 가능 (Java는 .equals() 필요)
print("hello" == "hello")   # True
print("hello" is "hello")   # True (단, 인터닝된 소규모 문자열만 - 일반적으로 == 사용)

# 빈 문자열 체크
name = ""
print(not name)             # True  (Python다운 방식 - 빈 문자열은 Falsy)
print(len(name) == 0)       # True
print("   ".strip() == "")  # True  (공백만 있는 경우 - Java .isBlank())

# ── 실전: URL 파싱 / 문자열 처리 ──────────────────────────────────────────
url = "https://api.example.com/users/123?page=1&size=10"

# 경로 추출
path = url.split("?")[0]                     # 'https://api.example.com/users/123'
query = url.split("?")[1]                    # 'page=1&size=10'
params = dict(p.split("=") for p in query.split("&"))  # {'page': '1', 'size': '10'}
print(params)

# 이메일 검증 (간단 버전)
email = "user@example.com"
is_valid = "@" in email and "." in email.split("@")[-1]
print(f"{email}: {'유효' if is_valid else '무효'}")

# ── 실전: 문자열 정규식 (re 모듈) ─────────────────────────────────────────
import re

text = "전화: 010-1234-5678, 이메일: user@example.com"

phone = re.search(r'\d{3}-\d{4}-\d{4}', text)
if phone:
    print(f"전화번호: {phone.group()}")   # 010-1234-5678

emails = re.findall(r'[\w.-]+@[\w.-]+\.\w+', text)
print(f"이메일: {emails}")               # ['user@example.com']

# 치환
clean = re.sub(r'\d{3}-\d{4}-\d{4}', '***-****-****', text)
print(clean)  # 전화: ***-****-****, 이메일: user@example.com
