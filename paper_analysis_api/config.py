"""
Configuration constants for Paper Analysis API
All magic values and configuration settings are defined here
"""

from pathlib import Path

# API Keys
GEMINI_API_KEY = "AIzaSyBPjYHrA655mLvYlZyJvDrl16C-Yj1fizE"

# Gemini Model Configuration
# Use stable Gemini 2.5 Flash (no preview, no exp)
GEMINI_MODEL_NAME = "gemini-2.5-flash"
GEMINI_FALLBACK_MODEL = "gemini-1.5-flash"

# PDF Processing Configuration
PDF_DPI_SCALE = 300 / 72  # 300 DPI for high-resolution images
MAX_PAGES_DEFAULT = 10
TEXT_TRUNCATE_LENGTH = 3000  # Characters to include per page text

# File Paths
BASE_DIR = Path(r"C:\Users\gridone\Downloads\추출")
TEMPLATE_PATH = BASE_DIR / "template.md"
OUTPUT_BASE_DIR = BASE_DIR / "api_output"

# Gemini API Configuration
GEMINI_RATE_LIMIT_DELAY = 2  # Seconds between API calls
GEMINI_TIMEOUT = 300  # Seconds for long analysis

# Template Instructions
TEMPLATE_INSTRUCTIONS = """다음은 학술 논문 PDF입니다.

앞으로 전체 논문의 각 페이지 이미지와 텍스트를 순차적으로 제공할 것입니다.
참고문헌(References) 섹션은 자동으로 제외되었습니다.
모든 페이지를 받은 후, 아래 template.md 형식에 맞춰 분석해주세요.

**중요한 작성 원칙:**
1. **쉽고 직관적으로 설명**: 고등학생이나 대학 저학년도 이해할 수 있는 수준으로
2. **전문 용어는 쉬운 말로 풀어서**: 예) "비정합성 점수" → "예측이 실제와 얼마나 다른지"
3. **실생활 비유를 적극 활용**:
   - 예) "예측 구간" → "날씨 예보에서 '내일 기온 10~15도' 처럼 범위로 알려주는 것"
   - 예) "커버리지 보장" → "10번 중 9번은 정답이 이 범위 안에 들어온다는 약속"
4. **핵심만 간단명료하게**: 불필요한 세부사항은 생략

**내용 구성:**
1. Read 1단계: 제목, 초록, 모든 Figure를 **비유와 함께** 쉽게 설명
2. Read 2단계: 도입부, 결론을 **핵심만** 간단히
3. Read 3단계: 수식을 **일상 언어와 비유로** 설명 (수학 기호는 최소화)
4. QnA: 4가지 질문에 **쉽고 명확하게** 답변
5. 한계점: 이 연구의 **아쉬운 점 3가지**를 간단히

**중요: Figure 언급 시 반드시 페이지 번호와 인덱스를 함께 표기하세요!**
- 형식: "Figure X (Page Y, Index Z)는 ..."
- 예: "Figure 1 (Page 3, Index 0)은 전체 시스템 구조를 보여줍니다..."
- Index는 해당 페이지에서 몇 번째 figure인지를 나타냅니다 (0부터 시작)

이제 페이지별로 내용을 전달하겠습니다. 각 페이지를 잘 기억해주세요."""

FINAL_ANALYSIS_REQUEST = """

이제 모든 페이지를 받았습니다.

**template.md 형식에 맞춰 쉽고 명확하게 분석해주세요:**

### 논문 구현에 앞서 확인해야 할 포인트

#### Read
1. 제목, 초록, 도표를 **비유와 함께 고등학생도 이해할 수 있게** 설명
   - 예: "Conformal Prediction" → "AI한테 '확실하지 않으면 범위로 대답해' 라고 가르치는 방법"
2. 도입부, 결론을 **핵심만 3-4문장으로** 간단히
3. 수식은 **수학 기호 없이 일상 언어로** 설명
   - 예: "s(z,y) = |ŷ - y|" → "AI의 답과 정답 사이의 거리 (오차)"

#### QnA
1. 저자가 뭘 해내고 싶어했는가? → **2-3문장 + 쉬운 비유**
2. 이 연구의 접근에서 중요한 요소는? → **3가지를 각각 비유와 함께**
3. 당신은 이 논문을 이용할 수 있는가? → **Yes/No + 이유 1-2가지**
4. 참고하고 싶은 레퍼런스는? → **2-3개만 간단히**

#### 한계점
1. **이 연구의 아쉬운 점 3가지**를 쉽게 설명
2. 각 한계점이 왜 중요한지 **비유와 함께**

---

**작성 원칙 (반드시 지켜주세요):**
✅ **비유를 적극 활용**: 예측 구간 = 날씨 예보 범위, 커버리지 = 적중률
✅ 전문 용어는 괄호 안에 쉬운 말로 설명
✅ Figure/표는 "한 문장 요약" 먼저, 그 다음 쉬운 설명
✅ 수식은 수학 기호 대신 "의미"를 일상 언어로
✅ 복잡한 내용은 단계별로 쪼개서 설명

지금 바로 **쉽고 명확한** 분석을 시작해주세요!"""
