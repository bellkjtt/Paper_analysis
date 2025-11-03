# 📡 사내 네트워크 접근 가이드

논문 분석 시스템을 같은 네트워크의 다른 사람들과 공유하는 방법입니다.

## ✅ 현재 상태

**서버 설정 완료**:
- ✅ 프론트엔드: `http://0.0.0.0:3000`
- ✅ 백엔드: `http://0.0.0.0:8000`
- ✅ 환경변수 설정
- ✅ 외부 접근 가능 모드

**로컬 IP 주소**: `10.30.1.138`

## 🚀 사용 방법

### 1. 서버 시작 (이미 실행 중)

**백엔드 서버**:
```bash
cd C:\Users\gridone\Downloads\추출
python -m uvicorn paper_analysis_api.main:app --host 0.0.0.0 --port 8000
```

**프론트엔드 서버**:
```bash
cd C:\Users\gridone\Downloads\추출\paper-analysis-next
npm run dev
```

### 2. 접속 방법

**본인 컴퓨터**:
- http://localhost:3000

**같은 네트워크의 다른 사람들**:
- http://10.30.1.138:3000

### 3. Windows 방화벽 설정 (필수)

다른 사람들이 접속하려면 Windows 방화벽에서 포트를 열어야 합니다.

**방법 1: PowerShell (관리자 권한)**
```powershell
# 프론트엔드 포트 3000 열기
New-NetFirewallRule -DisplayName "Paper Analysis Frontend" -Direction Inbound -Protocol TCP -LocalPort 3000 -Action Allow

# 백엔드 포트 8000 열기
New-NetFirewallRule -DisplayName "Paper Analysis Backend" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
```

**방법 2: GUI**
1. Windows 검색에서 "방화벽" 검색
2. "고급 보안이 포함된 Windows Defender 방화벽" 열기
3. 왼쪽에서 "인바운드 규칙" 클릭
4. 오른쪽에서 "새 규칙..." 클릭
5. 규칙 유형: "포트" 선택
6. 프로토콜: TCP, 특정 로컬 포트: 3000 입력
7. 작업: "연결 허용" 선택
8. 프로필: 모두 선택
9. 이름: "Paper Analysis Frontend" 입력
10. **8000 포트도 동일하게 반복**

### 4. 테스트

**다른 컴퓨터에서**:
1. 브라우저 열기
2. `http://10.30.1.138:3000` 접속
3. PDF 파일 업로드
4. 분석 결과 확인

**문제 발생 시**:
- 같은 Wi-Fi/네트워크에 연결되어 있는지 확인
- 방화벽 설정이 올바른지 확인
- 서버가 실행 중인지 확인: `netstat -ano | findstr ":3000"`

## 🔧 추가 설정

### IP 주소 변경 시 (다른 네트워크로 이동)

1. 새로운 IP 주소 확인:
```bash
ipconfig | findstr "IPv4"
```

2. `.env.local` 파일 수정:
```bash
# paper-analysis-next/.env.local
NEXT_PUBLIC_API_URL=http://새로운IP주소:8000
```

3. 프론트엔드 재시작

### 서버 중지 방법

**프론트엔드**:
```bash
# 포트 3000 사용 프로세스 찾기
netstat -ano | findstr ":3000"
# PID 확인 후 종료
taskkill //F //PID <PID번호>
```

**백엔드**:
```bash
# 포트 8000 사용 프로세스 찾기
netstat -ano | findstr ":8000"
# PID 확인 후 종료
taskkill //F //PID <PID번호>
```

## 📊 현재 서버 상태

**프론트엔드**: ✅ 실행 중 (Port 3000)
**백엔드**: ✅ 실행 중 (Port 8000)
**네트워크 접근**: ✅ 활성화

## 🔒 보안 참고사항

⚠️ **주의**: 이 설정은 **사내 네트워크 테스트용**입니다.

- 같은 Wi-Fi/네트워크에 있는 모든 사람이 접근 가능
- 인터넷에서는 접근 불가 (라우터 포트포워딩 미설정)
- 민감한 논문 업로드 시 주의
- 테스트 완료 후 방화벽 규칙 삭제 권장

## 📝 트러블슈팅

### 문제: 다른 사람이 접속 안 됨
- [ ] 같은 네트워크인가?
- [ ] 방화벽 포트가 열려있나?
- [ ] IP 주소가 맞나? (`ipconfig` 재확인)
- [ ] 서버가 실행 중인가?

### 문제: 백엔드 연결 실패
- [ ] `.env.local` 파일의 IP 주소 확인
- [ ] 백엔드 서버가 `0.0.0.0:8000`으로 실행 중인지 확인
- [ ] 포트 8000 방화벽 규칙 확인

### 문제: 이미지가 안 보임
- [ ] 백엔드 API URL이 올바른지 확인
- [ ] 브라우저 개발자 도구(F12)에서 네트워크 탭 확인
- [ ] CORS 오류 확인
