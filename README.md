# 🎤 영어 발음 AI 분석 시스템

AI 기반 영어 발음 및 유창성 분석 플랫폼입니다. OpenAI Whisper STT, 음소 분석, 운율 분석을 통해 실시간 피드백을 제공합니다.

## ✨ 주요 기능

- **🎯 발음 정확도 측정**: 단어 및 음소 수준의 정밀 분석
- **🗣️ 실시간 STT**: OpenAI Whisper 기반 고정확도 음성 인식
- **🎵 운율 분석**: 말하기 속도, 피치, 에너지 변화 측정
- **💬 AI 피드백**: 개인 맞춤 개선 방법 제안
- **🌐 REST API**: 웹/모바일 앱 통합 가능
- **📱 웹 인터페이스**: Streamlit 기반 사용자 친화적 UI

## 🏗️ 시스템 아키텍처

```
┌─────────────────┐
│  사용자 입력    │ (음성 녹음 또는 파일 업로드)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   STT Engine    │ OpenAI Whisper
│  음성 → 텍스트   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  발음 분석기     │
├─────────────────┤
│ • 단어 매칭     │
│ • 음소 비교     │
│ • 유사도 계산   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  운율 분석기     │
├─────────────────┤
│ • 말하기 속도   │
│ • 피치 변화     │
│ • 에너지 분석   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  피드백 생성기   │
│  AI 코칭        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  사용자 출력    │ (점수 + 상세 피드백)
└─────────────────┘
```

## 📦 설치 방법

### 1. 필수 요구사항

- Python 3.10 이상
- FFmpeg (오디오 처리용)
- 최소 4GB RAM (Whisper 모델용)

### 2. 라이브러리 설치

```bash
# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 필수 라이브러리 설치
pip install openai-whisper
pip install SpeechRecognition
pip install pronouncing
pip install pocketsphinx
pip install librosa
pip install soundfile
pip install numpy
pip install flask
pip install flask-cors
pip install streamlit
pip install pydub
pip install gtts

# FFmpeg 설치 (Ubuntu/Debian)
sudo apt-get install ffmpeg

# FFmpeg 설치 (macOS)
brew install ffmpeg

# FFmpeg 설치 (Windows)
# https://ffmpeg.org/download.html 에서 다운로드
```

### 3. 프로젝트 구조

```
pronunciation-analyzer/
│
├── pronunciation_analyzer.py  # 핵심 분석 모듈
├── api.py                     # Flask REST API
├── app.py                     # Streamlit 웹 앱
├── test_api.py                # API 테스트 스크립트
├── requirements.txt           # 의존성 목록
└── README.md                  # 이 파일
```

## 🚀 사용 방법

### 방법 1: 웹 인터페이스 (Streamlit)

```bash
# Streamlit 앱 실행
streamlit run app.py

# 브라우저에서 자동으로 열림 (http://localhost:8501)
```

**기능:**
- 📝 연습 문장 선택 (일상/비즈니스/여행)
- 🎙️ 음성 녹음 또는 파일 업로드
- 📊 실시간 분석 결과 및 피드백
- 📈 학습 통계 추적

### 방법 2: REST API 서버

```bash
# Flask API 서버 실행
python api.py

# 서버가 http://localhost:5000 에서 실행됨
```

### 방법 3: Python 모듈로 사용

```python
from pronunciation_analyzer import PronunciationAnalyzer

# 분석기 초기화
analyzer = PronunciationAnalyzer(model_size="base")

# 전체 분석
result = analyzer.full_analysis(
    audio_path="recording.wav",
    reference_text="Hello world, how are you?"
)

print(f"점수: {result['pronunciation']['overall_score']}")
print(f"피드백: {result['feedback']}")
```

## 📡 API 엔드포인트

### 1. 서버 상태 확인
```
GET /health
```

**Response:**
```json
{
    "status": "healthy",
    "service": "pronunciation-analyzer",
    "version": "1.0.0"
}
```

### 2. 발음 분석 (전체)
```
POST /api/analyze
Content-Type: multipart/form-data
```

**Parameters:**
- `audio` (file): 오디오 파일 (wav, mp3, m4a)
- `reference_text` (string): 참조 텍스트
- `analyze_prosody` (boolean, optional): 운율 분석 여부

**Response:**
```json
{
    "success": true,
    "data": {
        "spoken_text": "hello world how are you",
        "pronunciation": {
            "overall_score": 85.5,
            "word_accuracy": 80.0,
            "phoneme_similarity": 93.2,
            "mispronounced_words": [...]
        },
        "prosody": {
            "speaking_rate": 2.5,
            "pitch_variation": 45.2,
            "energy_variation": 0.0152
        },
        "feedback": "👍 좋아요! 발음이 꽤 정확합니다..."
    }
}
```

### 3. STT만 실행
```
POST /api/transcribe
Content-Type: multipart/form-data
```

**Parameters:**
- `audio` (file): 오디오 파일

**Response:**
```json
{
    "success": true,
    "text": "hello world how are you"
}
```

### 4. 텍스트 기반 스코어링
```
POST /api/score
Content-Type: application/json
```

**Request Body:**
```json
{
    "reference_text": "Hello world",
    "spoken_text": "Hello world"
}
```

**Response:**
```json
{
    "success": true,
    "score": 100.0,
    "details": {...},
    "feedback": "🎉 훌륭합니다!..."
}
```

### 5. 음소 추출
```
POST /api/phonemes
Content-Type: application/json
```

**Request Body:**
```json
{
    "text": "Hello world"
}
```

**Response:**
```json
{
    "success": true,
    "text": "Hello world",
    "phonemes": ["HH", "AH0", "L", "OW1", "W", "ER1", "L", "D"],
    "phoneme_count": 8
}
```

### 6. 연습 문장 목록
```
GET /api/practice-sentences?level=beginner&category=daily
```

**Parameters:**
- `level`: beginner / intermediate / advanced
- `category`: daily / business / travel

**Response:**
```json
{
    "success": true,
    "level": "beginner",
    "category": "daily",
    "sentences": [
        "Hello, how are you?",
        "Nice to meet you",
        ...
    ]
}
```

## 🧪 테스트

```bash
# API 테스트 실행 (서버가 실행 중이어야 함)
python test_api.py
```

## 🎯 스코어링 알고리즘

발음 점수는 다음과 같이 계산됩니다:

```
전체 점수 = (단어 정확도 × 0.6) + (음소 유사도 × 0.4)

단어 정확도 = (정확한 단어 수 / 전체 단어 수) × 100
음소 유사도 = SequenceMatcher(참조 음소, 인식 음소) × 100
```

**점수 등급:**
- 90-100점: 🟢 훌륭함
- 75-89점: 🟡 좋음
- 60-74점: 🟠 보통
- 0-59점: 🔴 개선 필요

## 💡 개선 방향

### 현재 구현
- ✅ OpenAI Whisper STT
- ✅ 텍스트 기반 음소 비교
- ✅ 기본 운율 분석
- ✅ REST API
- ✅ 웹 인터페이스

### 향후 계획
- [ ] **음향 모델 통합**: PocketSphinx acoustic scoring
- [ ] **실시간 녹음**: 브라우저 WebRTC 통합
- [ ] **음소 시각화**: 스펙트로그램 표시
- [ ] **학습 트래킹**: 사용자별 진도 관리
- [ ] **모바일 앱**: React Native 또는 Flutter
- [ ] **다국어 지원**: 다른 언어 발음 학습
- [ ] **AI 튜터 대화**: GPT 기반 대화형 학습
- [ ] **발음 비디오**: 입모양 시각화

## 🔧 문제 해결

### Whisper 모델 로드 실패
```bash
# GPU 메모리 부족 시 작은 모델 사용
analyzer = PronunciationAnalyzer(model_size="tiny")  # tiny, base, small
```

### FFmpeg 오류
```bash
# FFmpeg 설치 확인
ffmpeg -version

# 재설치
pip uninstall ffmpeg-python
pip install ffmpeg-python
```

### 네트워크 오류
```bash
# CORS 오류 시 Flask-CORS 설정 확인
# api.py에서 CORS(app, origins=["http://localhost:3000"]) 추가
```

## 📊 성능 최적화

### Whisper 모델 선택

| 모델 | 크기 | 속도 | 정확도 | 메모리 |
|------|------|------|--------|--------|
| tiny | 39M | 매우 빠름 | 낮음 | ~1GB |
| base | 74M | 빠름 | 보통 | ~1GB |
| small | 244M | 보통 | 높음 | ~2GB |
| medium | 769M | 느림 | 매우 높음 | ~5GB |

**권장:** 프로덕션에서는 `base` 또는 `small` 모델 사용

### 캐싱 전략
```python
# 모델 한 번만 로드
@lru_cache(maxsize=1)
def get_analyzer():
    return PronunciationAnalyzer(model_size="base")
```

## 🌐 프로덕션 배포

### Docker 컨테이너화 (예정)
```dockerfile
FROM python:3.10-slim
RUN apt-get update && apt-get install -y ffmpeg
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app
CMD ["python", "api.py"]
```

### 환경 변수
```bash
# .env 파일
WHISPER_MODEL_SIZE=base
API_PORT=5000
DEBUG_MODE=false
MAX_AUDIO_LENGTH=60  # 초
```

## 📄 라이선스

MIT License - 자유롭게 사용 및 수정 가능

## 🤝 기여

Issue 및 Pull Request 환영합니다!

## 📞 지원

문제가 있으시면 GitHub Issues에 등록해주세요.

---

**Made with ❤️ for English Learners**
