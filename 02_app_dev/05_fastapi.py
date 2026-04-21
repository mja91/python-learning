# =============================================================================
# FastAPI  |  Spring Boot REST API와 1:1 비교
# =============================================================================
# 설치: pip install fastapi uvicorn[standard] pydantic
# 실행: uvicorn 05_fastapi:app --reload --port 8000
# Swagger UI: http://localhost:8000/docs
#
# Spring Boot 비교표:
#   @RestController          →  APIRouter / app
#   @GetMapping("/users")    →  @app.get("/users")
#   @PostMapping             →  @app.post
#   @RequestBody DTO         →  Pydantic BaseModel
#   @PathVariable            →  def func(id: int)
#   @RequestParam            →  def func(page: int = 1)
#   ResponseEntity<T>        →  JSONResponse / 그냥 dict 반환
#   @ControllerAdvice        →  @app.exception_handler
#   @Autowired               →  Depends()
#   @Transactional           →  직접 구현 or SQLAlchemy
#   application.yml          →  pydantic-settings BaseSettings

from fastapi import FastAPI, HTTPException, Depends, Query, Path, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime
import uuid

# ── 앱 초기화 ─────────────────────────────────────────────────────────────
app = FastAPI(
    title="My API",
    description="Spring Boot 개발자를 위한 FastAPI 예제",
    version="1.0.0",
)

# CORS 설정  (Spring: CorsConfiguration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Pydantic 모델 (DTO)  =  Spring의 @RequestBody DTO ────────────────────
class UserCreate(BaseModel):           # Java: record UserCreate(String name, ...)
    name:  str  = Field(..., min_length=1, max_length=50)
    email: str  = Field(..., pattern=r"^[\w.-]+@[\w.-]+\.\w+$")
    age:   int  = Field(..., ge=0, le=150)
    role:  str  = Field(default="USER")

    @field_validator("name")           # Java: @NotBlank, @Size, @Valid
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("이름은 공백일 수 없습니다")
        return v.strip()

class UserResponse(BaseModel):         # 응답 DTO
    id:         str
    name:       str
    email:      str
    role:       str
    created_at: datetime

class UserUpdate(BaseModel):
    name:  Optional[str]  = None
    email: Optional[str]  = None
    role:  Optional[str]  = None

class PageResponse(BaseModel):
    items: List[UserResponse]
    total: int
    page:  int
    size:  int
    pages: int

# ── 인메모리 DB (예제용) ──────────────────────────────────────────────────
fake_db: dict[str, dict] = {}

def get_db():                          # Java: @Autowired Repository
    return fake_db                     # 실제로는 SQLAlchemy Session 반환

# ── CRUD 엔드포인트 ────────────────────────────────────────────────────────

# CREATE
@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="사용자 생성",
)
def create_user(
    body: UserCreate,                  # @RequestBody UserCreate body
    db:   dict = Depends(get_db),      # @Autowired Db db
):
    # 이메일 중복 체크
    if any(u["email"] == body.email for u in db.values()):
        raise HTTPException(           # Java: throw new ResponseStatusException(409, ...)
            status_code=status.HTTP_409_CONFLICT,
            detail=f"이미 사용 중인 이메일: {body.email}"
        )

    user = {
        "id":         str(uuid.uuid4()),
        "name":       body.name,
        "email":      body.email,
        "age":        body.age,
        "role":       body.role,
        "created_at": datetime.now(),
    }
    db[user["id"]] = user
    return user

# READ - 목록 (페이지네이션)
@app.get("/users", response_model=PageResponse)
def list_users(
    page:   int = Query(default=1, ge=1,     description="페이지 번호"),
    size:   int = Query(default=10, ge=1, le=100, description="페이지 크기"),
    search: Optional[str] = Query(default=None, description="이름 검색"),
    db:     dict = Depends(get_db),
):
    items = list(db.values())

    if search:
        items = [u for u in items if search.lower() in u["name"].lower()]

    total = len(items)
    start = (page - 1) * size
    end   = start + size

    return PageResponse(
        items = items[start:end],
        total = total,
        page  = page,
        size  = size,
        pages = (total + size - 1) // size,
    )

# READ - 단건
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: str = Path(..., description="사용자 ID"),
    db: dict = Depends(get_db),
):
    user = db.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"사용자를 찾을 수 없습니다: {user_id}"
        )
    return user

# UPDATE (PATCH - 부분 업데이트)
@app.patch("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str,
    body:    UserUpdate,
    db:      dict = Depends(get_db),
):
    user = db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자 없음")

    # None이 아닌 필드만 업데이트  (Java: Optional<T>와 유사)
    update_data = body.model_dump(exclude_none=True)
    user.update(update_data)
    return user

# DELETE
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: str,
    db:      dict = Depends(get_db),
):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="사용자 없음")
    del db[user_id]

# ── 전역 예외 핸들러  (Java: @ControllerAdvice) ───────────────────────────
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"success": False, "message": str(exc)},
    )

# ── 의존성 주입 심화  (Java: @Autowired, Spring Security) ─────────────────
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: dict = Depends(get_db),
) -> dict:
    token = credentials.credentials
    # 실제로는 JWT 검증 (pip install python-jose[cryptography])
    if token != "valid-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"id": "user-1", "role": "USER"}

@app.get("/me", response_model=dict)
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user

# ── 라우터 분리  (Java: @RequestMapping("/api/v1/products")) ─────────────
from fastapi import APIRouter

product_router = APIRouter(prefix="/products", tags=["products"])

@product_router.get("")
def list_products():
    return {"products": []}

@product_router.get("/{product_id}")
def get_product(product_id: str):
    return {"id": product_id}

app.include_router(product_router, prefix="/api/v1")
# → /api/v1/products, /api/v1/products/{id}

# ── 설정 관리  (Spring: application.yml) ─────────────────────────────────
# pip install pydantic-settings
# from pydantic_settings import BaseSettings
#
# class Settings(BaseSettings):
#     database_url: str = "postgresql://localhost/mydb"
#     secret_key:   str = "change-this-in-production"
#     debug:        bool = False
#
#     class Config:
#         env_file = ".env"
#
# settings = Settings()  # 환경변수 > .env > 기본값 순서로 적용

# ── 실행 (직접 실행 시) ───────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("05_fastapi:app", host="0.0.0.0", port=8000, reload=True)
    # curl http://localhost:8000/docs 에서 Swagger UI 확인
