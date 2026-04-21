# =============================================================================
# 예외처리 & 파일 I/O  |  Java: try-catch-finally, IOException
# =============================================================================

# ── 기본 예외처리  (Java: try-catch-finally) ──────────────────────────────
try:
    result = 10 / 0
except ZeroDivisionError as e:          # Java: catch (ArithmeticException e)
    print(f"나누기 오류: {e}")
except (TypeError, ValueError) as e:   # 여러 예외 한번에  (Java: catch 여러 개)
    print(f"타입/값 오류: {e}")
except Exception as e:                 # 모든 예외  (Java: catch (Exception e))
    print(f"예상치 못한 오류: {e}")
else:                                  # ★ 예외 없을 때만 실행  (Java 없음)
    print(f"성공: {result}")
finally:                               # 항상 실행  (Java: finally)
    print("정리 완료")

# ── 주요 내장 예외 ────────────────────────────────────────────────────────
# ValueError      - 잘못된 값       int("abc")
# TypeError       - 잘못된 타입     "a" + 1
# KeyError        - dict 키 없음    d["없는키"]
# IndexError      - 인덱스 범위 초과 list[99]
# AttributeError  - 속성 없음       obj.없는_속성
# FileNotFoundError - 파일 없음
# PermissionError - 권한 없음
# ConnectionError - 네트워크 오류
# TimeoutError    - 타임아웃
# NotImplementedError - 미구현 (Java: UnsupportedOperationException)
# StopIteration   - 이터레이터 소진

# ── 예외 발생  (Java: throw) ──────────────────────────────────────────────
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다")   # Java: throw new ValueError(...)
    return a / b

try:
    print(divide(10, 0))
except ValueError as e:
    print(f"오류: {e}")

# ── 커스텀 예외  (Java: custom Exception 클래스) ─────────────────────────
class AppError(Exception):
    """애플리케이션 기본 예외"""
    def __init__(self, message: str, code: int = 500):
        super().__init__(message)
        self.code = code

class NotFoundError(AppError):
    def __init__(self, resource: str, resource_id):
        super().__init__(f"{resource} not found: {resource_id}", code=404)
        self.resource    = resource
        self.resource_id = resource_id

class ValidationError(AppError):
    def __init__(self, field: str, message: str):
        super().__init__(f"Validation failed - {field}: {message}", code=400)
        self.field = field

# 사용
def get_user(user_id: int) -> dict:
    users = {1: {"name": "민혁"}}
    if user_id not in users:
        raise NotFoundError("User", user_id)
    return users[user_id]

def create_user(name: str) -> dict:
    if not name or not name.strip():
        raise ValidationError("name", "이름은 필수입니다")
    if len(name) > 50:
        raise ValidationError("name", "이름은 50자 이하여야 합니다")
    return {"name": name}

for user_id in [1, 999]:
    try:
        user = get_user(user_id)
        print(f"사용자: {user}")
    except NotFoundError as e:
        print(f"[{e.code}] {e}")

# ── 예외 체이닝  (Java: throw new RuntimeException("...", cause)) ─────────
try:
    int("not a number")
except ValueError as e:
    raise RuntimeError("데이터 파싱 실패") from e   # 원인 예외 연결

# ── 컨텍스트 매니저: with  (Java: try-with-resources) ────────────────────
# 파일 / DB 연결 / 락 등 자원을 자동으로 닫아줌

# ── 파일 입출력 ───────────────────────────────────────────────────────────
import os, json, csv
from pathlib import Path

# 디렉토리 준비
tmp = Path("/tmp/python_learning")
tmp.mkdir(exist_ok=True)

# 텍스트 파일 쓰기
file_path = tmp / "sample.txt"
with open(file_path, "w", encoding="utf-8") as f:   # Java: FileWriter + BufferedWriter
    f.write("첫 번째 줄\n")
    f.write("두 번째 줄\n")
    f.writelines(["세 번째 줄\n", "네 번째 줄\n"])

# 텍스트 파일 읽기
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()            # 전체 읽기
    print(repr(content[:20]))

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()         # 줄 목록으로 읽기
    print(lines[0].strip())

with open(file_path, "r", encoding="utf-8") as f:
    for line in f:                # 줄 단위 순회 (메모리 효율적)
        print(line.strip())

# 파일 추가
with open(file_path, "a", encoding="utf-8") as f:
    f.write("추가된 줄\n")

# ── JSON 파일  (Spring Boot의 ObjectMapper와 비슷) ────────────────────────
data = {
    "users": [
        {"id": 1, "name": "민혁", "email": "minhyuk@gmail.com"},
        {"id": 2, "name": "Alice", "email": "alice@example.com"},
    ],
    "total": 2
}

json_path = tmp / "data.json"

# JSON 저장
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)   # ensure_ascii=False: 한글 유지

# JSON 로드
with open(json_path, "r", encoding="utf-8") as f:
    loaded = json.load(f)
print(loaded["users"][0]["name"])   # 민혁

# 직렬화/역직렬화 (파일 없이)
json_str = json.dumps(data, ensure_ascii=False)   # dict → str
parsed   = json.loads(json_str)                    # str → dict

# ── CSV 파일 ──────────────────────────────────────────────────────────────
csv_path = tmp / "users.csv"

# CSV 쓰기
rows = [
    {"name": "민혁", "age": 34, "city": "서울"},
    {"name": "Alice", "age": 25, "city": "부산"},
]
with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:  # utf-8-sig: Excel 호환
    writer = csv.DictWriter(f, fieldnames=["name", "age", "city"])
    writer.writeheader()
    writer.writerows(rows)

# CSV 읽기
with open(csv_path, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(dict(row))

# ── Path 객체 (pathlib) ────────────────────────────────────────────────────
from pathlib import Path

# Java: Paths.get(...), Files.exists() 등
base = Path("/tmp/python_learning")

print(base.exists())             # True
print(base.is_dir())             # True
print(base / "data.json")        # /tmp/python_learning/data.json

p = base / "data.json"
print(p.name)       # data.json
print(p.stem)       # data
print(p.suffix)     # .json
print(p.parent)     # /tmp/python_learning

# 디렉토리 내 파일 목록
for f in base.iterdir():
    print(f.name)

# 패턴 매칭
for f in base.glob("*.json"):
    print(f)

# 파일 크기
print(p.stat().st_size, "bytes")

# ── 환경변수 (Spring Boot의 @Value, application.yml 대응) ────────────────
import os

db_host = os.getenv("DB_HOST", "localhost")    # 기본값 포함
db_port = int(os.getenv("DB_PORT", "5432"))
api_key  = os.environ.get("API_KEY")           # 없으면 None

if api_key is None:
    print("경고: API_KEY 환경변수가 설정되지 않았습니다")

# .env 파일 읽기 (pip install python-dotenv)
# from dotenv import load_dotenv
# load_dotenv()  # .env 파일 자동 로드
