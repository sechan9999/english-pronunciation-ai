# 🚀 빠른 시작 가이드

영어 발음 AI 분석 시스템을 5분 안에 설치하고 실행하는 방법입니다.

## 📦 1단계: 설치 (3분)

```bash
# 1. Python 3.10+ 확인
python --version

# 2. 가상환경 생성 (권장)
python -m venv venv

# 3. 가상환경 활성화
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. 필수 패키지 설치
pip install -r requirements.txt

# 5. FFmpeg 설치 (오디오 처리용)
# Ubuntu/Debian:
sudo apt-get install ffmpeg
# macOS:
brew install ffmpeg
# Windows: https://ffmpeg.org/download.html
```

## 🎮 2단계: 데모 실행 (1분)

```bash
# 텍스트 기반 데모 (오디오 파일 불필요)
python demo.py
```

**출력 예시:**
```
======================================================================
               🎤 영어 발음 AI 분석 시스템 데모
======================================================================

테스트 1: 완벽한 발음
참조 문장: Hello world, how are you today?
인식 문장: Hello world, how are you today?

🎉 훌륭합니다! 발음이 매우 정확해요.
📊 점수: 100.0점
```

## 🌐 3단계: 웹 앱 실행 (1분)

### 방법 A: Streamlit (추천)

```bash
streamlit run app.py
```

브라우저가 자동으로 열립니다: `http://localhost:8501`

**기능:**
- ✅ 오디오 파일 업로드
- ✅ 실시간 분석 결과
- ✅ 시각적 피드백
- ✅ 학습 통계

### 방법 B: Flask API

```bash
python api.py
```

API 서버 실행: `http://localhost:5000`

**테스트:**
```bash
# 새 터미널에서
python test_api.py
```

## 🎯 사용 예제

### Python 코드에서 사용

```python
from pronunciation_analyzer import PronunciationAnalyzer

# 초기화
analyzer = PronunciationAnalyzer()

# 텍스트 기반 분석 (빠른 테스트)
result = analyzer.calculate_pronunciation_score(
    reference_text="Hello world",
    spoken_text="Hello world"
)

print(f"점수: {result['overall_score']}")
# 출력: 점수: 100.0

# 전체 분석 (오디오 파일 포함)
result = analyzer.full_analysis(
    audio_path="my_recording.wav",
    reference_text="Hello world, how are you?"
)

print(result['feedback'])
```

### API 호출

```bash
# cURL로 텍스트 기반 분석
curl -X POST http://localhost:5000/api/score \
  -H "Content-Type: application/json" \
  -d '{
    "reference_text": "Hello world",
    "spoken_text": "Hello world"
  }'
```

```python
# Python requests로 오디오 파일 분석
import requests

with open('recording.wav', 'rb') as audio:
    response = requests.post(
        'http://localhost:5000/api/analyze',
        files={'audio': audio},
        data={'reference_text': 'Hello world'}
    )
    
result = response.json()
print(f"점수: {result['data']['pronunciation']['overall_score']}")
```

## 📱 통합 예제

### React/JavaScript

```javascript
// 오디오 녹음 및 분석
async function recordAndAnalyze() {
    // 1. 녹음 (MediaRecorder API 사용)
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    const chunks = [];
    
    mediaRecorder.ondataavailable = (e) => chunks.push(e.data);
    mediaRecorder.onstop = async () => {
        const blob = new Blob(chunks, { type: 'audio/wav' });
        
        // 2. API로 전송
        const formData = new FormData();
        formData.append('audio', blob, 'recording.wav');
        formData.append('reference_text', 'Hello world');
        
        const response = await fetch('http://localhost:5000/api/analyze', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        console.log('점수:', result.data.pronunciation.overall_score);
    };
    
    mediaRecorder.start();
    setTimeout(() => mediaRecorder.stop(), 3000); // 3초 녹음
}
```

### Flutter/Dart

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<void> analyzePronunciation(String audioPath, String referenceText) async {
  var request = http.MultipartRequest(
    'POST',
    Uri.parse('http://localhost:5000/api/analyze'),
  );
  
  request.files.add(await http.MultipartFile.fromPath('audio', audioPath));
  request.fields['reference_text'] = referenceText;
  
  var response = await request.send();
  var responseData = await response.stream.bytesToString();
  var result = json.decode(responseData);
  
  print('점수: ${result['data']['pronunciation']['overall_score']}');
}
```

## 🔧 문제 해결

### 문제 1: Whisper 모델 로드 느림
```python
# 더 작은 모델 사용
analyzer = PronunciationAnalyzer(model_size="tiny")  # 빠름
analyzer = PronunciationAnalyzer(model_size="base")  # 권장
```

### 문제 2: 메모리 부족
```bash
# 환경 변수로 모델 크기 제한
export WHISPER_MODEL_SIZE=tiny
python api.py
```

### 문제 3: CORS 오류
```python
# api.py에서
from flask_cors import CORS
CORS(app, origins=["http://localhost:3000"])
```

## 📚 다음 단계

1. **README.md** - 전체 문서 읽기
2. **demo.py** - 다양한 예제 실행
3. **test_api.py** - API 테스트
4. **app.py** - 웹 인터페이스 커스터마이징

## 💡 유용한 팁

### 연습 문장 가져오기
```bash
curl http://localhost:5000/api/practice-sentences?level=beginner&category=daily
```

### 음소 분석
```bash
curl -X POST http://localhost:5000/api/phonemes \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world"}'
```

### 배치 처리
```python
# 여러 파일 동시 분석
import concurrent.futures

def analyze_file(filepath):
    return analyzer.full_analysis(filepath, "Hello world")

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(analyze_file, audio_files)
```

## 🎓 학습 리소스

- **Whisper 문서**: https://github.com/openai/whisper
- **Pronouncing 라이브러리**: https://pronouncing.readthedocs.io/
- **Librosa 튜토리얼**: https://librosa.org/doc/latest/tutorial.html
- **Flask REST API**: https://flask.palletsprojects.com/

## 📞 지원

질문이나 문제가 있으신가요?
- GitHub Issues에 등록
- README.md의 상세 문서 참조
- test_api.py로 API 동작 확인

---

**Happy Learning! 🎉**
