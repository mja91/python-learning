# =============================================================================
# 클래스 & OOP  |  Java: class, interface, abstract class, record
# =============================================================================

# ── 기본 클래스 ───────────────────────────────────────────────────────────
class Animal:
    # 클래스 변수  (Java: static 필드)
    species_count = 0

    # __init__ = Java의 생성자
    def __init__(self, name: str, age: int):
        # 인스턴스 변수  (Java: this.name = name)
        self.name = name
        self.age  = age
        Animal.species_count += 1

    # 인스턴스 메서드
    def speak(self) -> str:              # self = Java의 this
        return f"{self.name}이(가) 말합니다"

    # __repr__: Java의 toString()
    def __repr__(self) -> str:
        return f"Animal(name={self.name!r}, age={self.age})"

    # __eq__: Java의 equals()
    def __eq__(self, other) -> bool:
        if not isinstance(other, Animal):
            return NotImplemented
        return self.name == other.name and self.age == other.age

    # 클래스 메서드  (Java: static 메서드 + factory method)
    @classmethod
    def create_puppy(cls, name: str) -> "Animal":
        return cls(name, age=0)

    # 정적 메서드  (Java: static 메서드)
    @staticmethod
    def is_valid_age(age: int) -> bool:
        return 0 <= age <= 30

a = Animal("멍멍이", 3)
print(a)               # Animal(name='멍멍이', age=3)
print(a.speak())       # 멍멍이이(가) 말합니다
print(Animal.species_count)   # 1
puppy = Animal.create_puppy("강아지")
print(Animal.is_valid_age(5)) # True

# ── @property: getter / setter  (Java의 Lombok @Getter @Setter) ──────────
class Temperature:
    def __init__(self, celsius: float):
        self._celsius = celsius        # ★ _ 접두사 = protected 관례 (강제 아님)

    @property
    def celsius(self) -> float:        # getter
        return self._celsius

    @celsius.setter
    def celsius(self, value: float):   # setter
        if value < -273.15:
            raise ValueError(f"절대 영도 이하: {value}")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:     # 계산 프로퍼티 (setter 없음 = read-only)
        return self._celsius * 9/5 + 32

t = Temperature(100)
print(t.celsius)     # 100
print(t.fahrenheit)  # 212.0
t.celsius = 0
print(t.fahrenheit)  # 32.0

# ── 상속  (Java: extends) ─────────────────────────────────────────────────
class Dog(Animal):
    def __init__(self, name: str, age: int, breed: str):
        super().__init__(name, age)     # Java: super(name, age)
        self.breed = breed

    def speak(self) -> str:             # 오버라이딩  (Java: @Override)
        return f"{self.name}: 멍멍!"

    def __repr__(self) -> str:
        return f"Dog(name={self.name!r}, breed={self.breed!r})"

dog = Dog("바둑이", 2, "시바견")
print(dog.speak())              # 바둑이: 멍멍!
print(isinstance(dog, Animal))  # True   (Java instanceof)
print(isinstance(dog, Dog))     # True

# ── 추상 클래스  (Java: abstract class / interface) ───────────────────────
from abc import ABC, abstractmethod

class Shape(ABC):                       # ABC = Abstract Base Class
    @abstractmethod
    def area(self) -> float:            # 반드시 구현 필요  (Java abstract method)
        ...

    @abstractmethod
    def perimeter(self) -> float:
        ...

    def describe(self) -> str:          # 구체 메서드  (Java concrete method)
        return f"넓이={self.area():.2f}, 둘레={self.perimeter():.2f}"

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        import math
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width  = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

shapes = [Circle(5), Rectangle(4, 6)]
for shape in shapes:
    print(shape.describe())

# ── @dataclass: 보일러플레이트 제거  (Java: record / Lombok @Data) ─────────
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class User:
    id:       int
    name:     str
    email:    str
    role:     str   = "USER"           # 기본값
    tags:     List[str] = field(default_factory=list)  # 가변 기본값은 field() 사용
    active:   bool  = True

    def is_admin(self) -> bool:
        return self.role == "ADMIN"

# __init__, __repr__, __eq__ 자동 생성
u = User(id=1, name="민혁", email="minhyuk@gmail.com")
print(u)           # User(id=1, name='민혁', email='minhyuk@gmail.com', role='USER', ...)
print(u.is_admin())  # False

# Java record처럼 불변으로 만들려면
@dataclass(frozen=True)
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
# p.x = 99  # FrozenInstanceError

# ── 매직 메서드 (Dunder methods) ──────────────────────────────────────────
# Java의 Comparable, Iterable, Closeable 등과 유사
class Money:
    def __init__(self, amount: int, currency: str = "KRW"):
        self.amount   = amount
        self.currency = currency

    def __repr__(self):   return f"Money({self.amount} {self.currency})"
    def __str__(self):    return f"{self.amount:,} {self.currency}"  # print() 시 사용
    def __add__(self, other):   # +  연산자
        if self.currency != other.currency:
            raise ValueError("통화 단위가 다릅니다")
        return Money(self.amount + other.amount, self.currency)
    def __lt__(self, other):    # < 비교 (Java Comparable.compareTo)
        return self.amount < other.amount
    def __eq__(self, other):    # == 비교
        return self.amount == other.amount and self.currency == other.currency

m1 = Money(1000)
m2 = Money(2000)
print(m1 + m2)     # 3,000 KRW
print(m1 < m2)     # True
print(sorted([m2, m1]))  # __lt__ 덕분에 정렬 가능

# ── 컨텍스트 매니저  (Java의 try-with-resources) ──────────────────────────
class DatabaseConnection:
    def __init__(self, url: str):
        self.url = url
        self.conn = None

    def __enter__(self):               # try-with-resources의 초기화
        print(f"DB 연결: {self.url}")
        self.conn = {"connected": True}
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):  # finally 블록
        print("DB 연결 해제")
        self.conn = None
        return False   # True 반환하면 예외 억제

with DatabaseConnection("postgresql://localhost/mydb") as conn:
    print(f"쿼리 실행 중: {conn}")
# 블록 종료 시 자동으로 __exit__ 호출

# ── 실전: 서비스 레이어 패턴 (Spring Boot @Service와 유사) ───────────────
from dataclasses import dataclass
from typing import Dict, Optional
import uuid

@dataclass
class Product:
    id:    str
    name:  str
    price: int
    stock: int = 0

class ProductRepository:
    def __init__(self):
        self._store: Dict[str, Product] = {}

    def save(self, product: Product) -> Product:
        self._store[product.id] = product
        return product

    def find_by_id(self, product_id: str) -> Optional[Product]:
        return self._store.get(product_id)

    def find_all(self) -> list:
        return list(self._store.values())

class ProductService:
    def __init__(self, repo: ProductRepository):   # 의존성 주입
        self._repo = repo

    def create_product(self, name: str, price: int, stock: int = 0) -> Product:
        product = Product(
            id    = str(uuid.uuid4())[:8],
            name  = name,
            price = price,
            stock = stock
        )
        return self._repo.save(product)

    def get_product(self, product_id: str) -> Product:
        product = self._repo.find_by_id(product_id)
        if product is None:
            raise ValueError(f"상품을 찾을 수 없습니다: {product_id}")
        return product

# 사용
repo    = ProductRepository()
service = ProductService(repo)

p1 = service.create_product("노트북", 1_500_000, stock=10)
p2 = service.create_product("마우스", 50_000, stock=50)
print(service.get_product(p1.id))
print([p.name for p in repo.find_all()])
