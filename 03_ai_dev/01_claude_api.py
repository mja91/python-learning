# =============================================================================
# Claude API (Anthropic SDK)
# =============================================================================
# 설치: pip install anthropic
# API 키: https://console.anthropic.com → API Keys
# 환경변수: export ANTHROPIC_API_KEY="sk-ant-..."
#
# 모델 선택 가이드:
#   claude-opus-4-7       - 가장 강력, 복잡한 추론
#   claude-sonnet-4-6     - 균형 (속도/성능/비용) ← 일반적으로 추천
#   claude-haiku-4-5-20251001 - 빠르고 저렴, 간단한 작업

import os
import anthropic

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)
MODEL = "claude-sonnet-4-6"

# ── 1. 기본 메시지 ─────────────────────────────────────────────────────────
def basic_message():
    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "파이썬으로 피보나치 수열을 구하는 코드를 작성해줘"}
        ]
    )
    print(message.content[0].text)
    print(f"\n[토큰 사용] 입력: {message.usage.input_tokens}, 출력: {message.usage.output_tokens}")

# ── 2. 시스템 프롬프트  (AI 역할/페르소나 지정) ───────────────────────────
def with_system_prompt():
    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system="""당신은 Java Spring Boot 경력 5년의 개발자가 Python을 배우도록 돕는
        전문 튜터입니다. 모든 설명을 Java 개념과 비교해서 설명하세요.
        코드 예제를 항상 포함하세요.""",
        messages=[
            {"role": "user", "content": "Python의 dict comprehension을 설명해줘"}
        ]
    )
    print(message.content[0].text)

# ── 3. 멀티턴 대화  (대화 히스토리 유지) ─────────────────────────────────
def multi_turn_chat():
    conversation = []

    questions = [
        "Python list와 Java ArrayList의 차이점이 뭐야?",
        "그럼 Python에서 타입 안전한 리스트를 만들려면?",
        "typing 모듈 외에 다른 방법도 있어?",
    ]

    for question in questions:
        conversation.append({"role": "user", "content": question})

        response = client.messages.create(
            model=MODEL,
            max_tokens=512,
            system="당신은 Python 전문가입니다. 간결하게 답변하세요.",
            messages=conversation
        )

        answer = response.content[0].text
        conversation.append({"role": "assistant", "content": answer})

        print(f"Q: {question}")
        print(f"A: {answer[:200]}...")
        print("-" * 50)

# ── 4. 스트리밍  (응답을 실시간으로 출력) ────────────────────────────────
def streaming_response():
    print("스트리밍 응답: ", end="", flush=True)
    with client.messages.stream(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": "FastAPI의 장점을 설명해줘"}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
    print()   # 줄바꿈

# ── 5. 프롬프트 캐싱  (비용 절감 - 긴 컨텍스트 반복 사용 시) ───────────
def with_prompt_caching():
    # 긴 시스템 프롬프트나 문서를 캐시에 저장
    long_document = "..." * 500  # 긴 문서 내용

    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": long_document,
                "cache_control": {"type": "ephemeral"}  # 캐시 지정
            }
        ],
        messages=[{"role": "user", "content": "이 문서의 핵심을 요약해줘"}]
    )
    # 두 번째 호출부터 캐시 히트 → 비용 90% 절감
    print(f"캐시 생성 토큰: {message.usage.cache_creation_input_tokens}")
    print(f"캐시 읽기 토큰: {message.usage.cache_read_input_tokens}")

# ── 6. 구조화된 출력 (Tool Use / JSON 모드) ────────────────────────────────
def structured_output():
    tools = [
        {
            "name": "extract_user_info",
            "description": "텍스트에서 사용자 정보를 추출합니다",
            "input_schema": {
                "type": "object",
                "properties": {
                    "name":  {"type": "string",  "description": "사용자 이름"},
                    "age":   {"type": "integer", "description": "나이"},
                    "email": {"type": "string",  "description": "이메일 주소"},
                },
                "required": ["name"]
            }
        }
    ]

    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        tools=tools,
        tool_choice={"type": "auto"},
        messages=[{
            "role": "user",
            "content": "민혁, 34세, minhyuk@gmail.com 님의 계정을 만들어줘"
        }]
    )

    # tool_use 블록 추출
    for block in message.content:
        if block.type == "tool_use":
            print(f"함수: {block.name}")
            print(f"추출된 데이터: {block.input}")

# ── 7. 실전: 코드 리뷰 봇 ─────────────────────────────────────────────────
def code_review_bot(code: str, language: str = "Python") -> dict:
    message = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system="""당신은 시니어 소프트웨어 엔지니어입니다.
코드를 리뷰하고 반드시 다음 JSON 형식으로만 응답하세요:
{
  "score": 0-100,
  "issues": [{"severity": "high|medium|low", "description": "...", "line": 번호}],
  "suggestions": ["개선 제안 1", "개선 제안 2"],
  "summary": "전반적인 평가"
}""",
        messages=[{
            "role": "user",
            "content": f"다음 {language} 코드를 리뷰해주세요:\n\n```{language}\n{code}\n```"
        }]
    )

    import json
    text = message.content[0].text
    # JSON 파싱 (실제로는 더 견고한 파싱 필요)
    start = text.find("{")
    end   = text.rfind("}") + 1
    if start != -1 and end > start:
        return json.loads(text[start:end])
    return {"summary": text}

# ── 8. 실전: 비동기 처리  (FastAPI와 함께 사용) ───────────────────────────
async def async_claude():
    """FastAPI async 엔드포인트에서 사용하는 비동기 버전"""
    async_client = anthropic.AsyncAnthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )

    message = await async_client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": "안녕하세요!"}]
    )
    return message.content[0].text

# FastAPI 엔드포인트에서 사용 예:
# @app.post("/chat")
# async def chat(request: ChatRequest):
#     response = await async_claude()
#     return {"message": response}

# ── 9. 실전: RAG 패턴 (검색 증강 생성) ──────────────────────────────────
def rag_example(query: str, documents: list[str]) -> str:
    """
    검색된 문서를 컨텍스트로 제공하여 정확한 답변 생성
    (Vector DB + Claude 조합의 핵심 패턴)
    """
    context = "\n\n".join([f"[문서 {i+1}]\n{doc}" for i, doc in enumerate(documents)])

    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system="""아래 제공된 문서들만을 근거로 질문에 답하세요.
문서에 없는 내용은 '제공된 정보에 없습니다'라고 하세요.""",
        messages=[{
            "role": "user",
            "content": f"[참고 문서]\n{context}\n\n[질문]\n{query}"
        }]
    )
    return message.content[0].text

# ── 10. 실전: 배치 처리 (Batch API) ──────────────────────────────────────
def batch_processing_example():
    """
    대량의 요청을 비동기 배치로 처리 (비용 50% 절감)
    결과는 24시간 내 완료
    """
    texts_to_analyze = [
        "이 제품 정말 좋아요!",
        "배송이 너무 느려서 실망했습니다.",
        "가격 대비 괜찮은 것 같아요.",
    ]

    requests = [
        {
            "custom_id": f"review-{i}",
            "params": {
                "model": MODEL,
                "max_tokens": 100,
                "messages": [{
                    "role": "user",
                    "content": f"다음 리뷰의 감정을 'positive', 'negative', 'neutral' 중 하나로만 답하세요: {text}"
                }]
            }
        }
        for i, text in enumerate(texts_to_analyze)
    ]

    # 배치 생성
    batch = client.messages.batches.create(requests=requests)
    print(f"배치 ID: {batch.id}")
    print(f"상태: {batch.processing_status}")
    # 완료 후: client.messages.batches.results(batch.id) 로 결과 조회

# ── 실행 예제 ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY 환경변수를 설정하세요:")
        print('  export ANTHROPIC_API_KEY="sk-ant-..."')
        exit(1)

    print("=" * 60)
    print("1. 기본 메시지")
    print("=" * 60)
    basic_message()

    print("\n" + "=" * 60)
    print("2. 스트리밍")
    print("=" * 60)
    streaming_response()

    print("\n" + "=" * 60)
    print("3. 코드 리뷰 봇")
    print("=" * 60)
    sample_code = """
def get_users(db, role):
    users = []
    for user in db:
        if user['role'] == role:
            users.append(user)
    return users
"""
    review = code_review_bot(sample_code)
    import json
    print(json.dumps(review, ensure_ascii=False, indent=2))
