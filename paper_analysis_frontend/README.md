# 논문 분석 프론트엔드

Paper Analysis API를 위한 깔끔하고 미니멀한 웹 인터페이스입니다.

## 기능

- 📄 PDF 파일 업로드
- ⚙️ 분석 옵션 설정 (페이지 수, 템플릿)
- 🤖 Gemini Flash 2.5로 논문 분석
- 📝 마크다운 결과 표시
- 📋 결과 복사 및 다운로드

## 디자인 원칙

이 프론트엔드는 다음 원칙을 준수합니다:

1. **깔끔한 디자인**: 정신없지 않은 미니멀한 UI
2. **무채색 위주**: RGB 색상과 그라데이션 최소화
3. **단순한 색상**: 흰색, 회색, 검정 + 파란색 accent만 사용
4. **모듈화**: HTML, CSS, JS 분리
5. **Readability**: 명확한 네이밍과 구조
6. **Single Responsibility**: 각 모듈은 하나의 책임만

## 파일 구조

```
paper_analysis_frontend/
├── index.html          # 메인 HTML 구조
├── css/
│   └── styles.css      # 스타일 정의
└── js/
    ├── markdown.js     # 마크다운 렌더러
    └── app.js          # 메인 애플리케이션 로직
```

## 사용 방법

### 1. API 서버 실행

먼저 백엔드 API 서버가 실행 중이어야 합니다:

```bash
cd C:\Users\gridone\Downloads\추출
python -m uvicorn paper_analysis_api.main:app --host 127.0.0.1 --port 8000
```

### 2. 프론트엔드 열기

브라우저에서 `index.html` 파일을 직접 열거나, 간단한 HTTP 서버를 실행합니다:

**Python HTTP 서버:**
```bash
cd paper_analysis_frontend
python -m http.server 8080
```

그 다음 브라우저에서 http://localhost:8080 접속

**또는 직접 열기:**
```bash
# Windows
start index.html

# 또는 브라우저에서 직접 파일 열기
```

### 3. 논문 분석

1. **PDF 파일 선택**: "파일 선택" 버튼을 클릭하여 분석할 PDF 선택
2. **옵션 설정**: 분석할 페이지 수와 템플릿 선택
3. **분석 시작**: "분석 시작" 버튼 클릭
4. **결과 확인**: 분석 완료 후 결과를 확인하고 복사 또는 다운로드

## 기술 스택

- **순수 HTML/CSS/JavaScript**: 외부 라이브러리 없음
- **모던 ES6+**: Clean한 JavaScript 코드
- **Responsive Design**: 모바일 친화적 레이아웃
- **Accessible**: ARIA 레이블과 시맨틱 HTML

## 색상 팔레트

```css
--color-white: #FFFFFF       /* 배경 */
--color-gray-50: #F9FAFB     /* 섹션 배경 */
--color-gray-900: #111827    /* 주요 텍스트 */
--color-blue: #3B82F6        /* Accent 색상 */
--color-blue-dark: #2563EB   /* Hover 상태 */
```

## 브라우저 지원

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## 개발

모든 코드는 다음 원칙을 따릅니다:

- ✅ 명확한 변수/함수명
- ✅ Single Responsibility
- ✅ No Magic Values (상수 정의)
- ✅ 순수 함수 우선
- ✅ 주석은 "왜"만 설명
