"""
API 테스트 및 사용 예제
"""

import requests
import json

# API 베이스 URL
BASE_URL = "http://localhost:5000"


def test_health_check():
    """서버 상태 확인 테스트"""
    print("=" * 60)
    print("1. 서버 상태 확인 테스트")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_practice_sentences():
    """연습 문장 가져오기 테스트"""
    print("=" * 60)
    print("2. 연습 문장 가져오기 테스트")
    print("=" * 60)
    
    # 초급 일상 회화
    response = requests.get(f"{BASE_URL}/api/practice-sentences", params={
        'level': 'beginner',
        'category': 'daily'
    })
    print(f"초급 일상 회화:")
    print(json.dumps(response.json(), indent=2))
    print()
    
    # 중급 비즈니스
    response = requests.get(f"{BASE_URL}/api/practice-sentences", params={
        'level': 'intermediate',
        'category': 'business'
    })
    print(f"중급 비즈니스:")
    print(json.dumps(response.json(), indent=2))
    print()


def test_phoneme_extraction():
    """음소 추출 테스트"""
    print("=" * 60)
    print("3. 음소 추출 테스트")
    print("=" * 60)
    
    test_texts = [
        "Hello world",
        "How are you today?",
        "The quick brown fox"
    ]
    
    for text in test_texts:
        response = requests.post(f"{BASE_URL}/api/phonemes", json={
            'text': text
        })
        result = response.json()
        print(f"Text: {text}")
        print(f"Phonemes: {result.get('phonemes', [])}")
        print(f"Count: {result.get('phoneme_count', 0)}")
        print()


def test_text_scoring():
    """텍스트 기반 스코어링 테스트"""
    print("=" * 60)
    print("4. 텍스트 기반 스코어링 테스트")
    print("=" * 60)
    
    test_cases = [
        {
            'reference': "Hello world how are you",
            'spoken': "Hello world how are you",
            'description': "완벽한 매칭"
        },
        {
            'reference': "Hello world how are you",
            'spoken': "Hello world how you",
            'description': "한 단어 누락"
        },
        {
            'reference': "Hello world how are you",
            'spoken': "Halo world how are you",
            'description': "발음 오류"
        }
    ]
    
    for case in test_cases:
        print(f"\n테스트: {case['description']}")
        print(f"참조: {case['reference']}")
        print(f"인식: {case['spoken']}")
        
        response = requests.post(f"{BASE_URL}/api/score", json={
            'reference_text': case['reference'],
            'spoken_text': case['spoken']
        })
        
        result = response.json()
        if result.get('success'):
            print(f"점수: {result['score']}")
            print(f"피드백:\n{result['feedback']}")
        print("-" * 60)


def test_audio_analysis():
    """오디오 파일 분석 테스트 (샘플 파일 필요)"""
    print("=" * 60)
    print("5. 오디오 파일 분석 테스트")
    print("=" * 60)
    
    # 실제 오디오 파일 경로 (예시)
    audio_file_path = "sample_audio.wav"
    reference_text = "Hello world how are you today"
    
    print(f"오디오 파일이 필요합니다: {audio_file_path}")
    print(f"참조 텍스트: {reference_text}")
    print()
    
    # 파일이 존재하는 경우 테스트
    try:
        with open(audio_file_path, 'rb') as audio_file:
            files = {'audio': audio_file}
            data = {
                'reference_text': reference_text,
                'analyze_prosody': 'true'
            }
            
            response = requests.post(
                f"{BASE_URL}/api/analyze",
                files=files,
                data=data
            )
            
            result = response.json()
            if result.get('success'):
                print("분석 성공!")
                print(json.dumps(result['data'], indent=2))
            else:
                print(f"분석 실패: {result.get('error')}")
    
    except FileNotFoundError:
        print("⚠️ 샘플 오디오 파일이 없습니다.")
        print("테스트를 위해 'sample_audio.wav' 파일을 준비해주세요.")
    print()


def create_sample_client_code():
    """클라이언트 샘플 코드 생성"""
    print("=" * 60)
    print("6. 클라이언트 통합 샘플 코드")
    print("=" * 60)
    
    sample_code = '''
# JavaScript (React/Vue) 예제
async function analyzePronunciation(audioBlob, referenceText) {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.wav');
    formData.append('reference_text', referenceText);
    formData.append('analyze_prosody', 'true');
    
    try {
        const response = await fetch('http://localhost:5000/api/analyze', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            console.log('점수:', result.data.pronunciation.overall_score);
            console.log('피드백:', result.data.feedback);
            return result.data;
        } else {
            console.error('분석 실패:', result.error);
        }
    } catch (error) {
        console.error('API 호출 실패:', error);
    }
}

# Python 클라이언트 예제
import requests

def analyze_pronunciation(audio_file_path, reference_text):
    with open(audio_file_path, 'rb') as audio:
        files = {'audio': audio}
        data = {
            'reference_text': reference_text,
            'analyze_prosody': 'true'
        }
        
        response = requests.post(
            'http://localhost:5000/api/analyze',
            files=files,
            data=data
        )
        
        return response.json()

# 사용 예
result = analyze_pronunciation('my_recording.wav', 'Hello world')
print(f"점수: {result['data']['pronunciation']['overall_score']}")

# Swift (iOS) 예제
func analyzePronunciation(audioURL: URL, referenceText: String) {
    let url = URL(string: "http://localhost:5000/api/analyze")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    
    let boundary = UUID().uuidString
    request.setValue("multipart/form-data; boundary=\\(boundary)", 
                    forHTTPHeaderField: "Content-Type")
    
    var body = Data()
    
    // Add audio file
    body.append("--\\(boundary)\\r\\n")
    body.append("Content-Disposition: form-data; name=\\"audio\\"; filename=\\"recording.wav\\"\\r\\n")
    body.append("Content-Type: audio/wav\\r\\n\\r\\n")
    body.append(try! Data(contentsOf: audioURL))
    body.append("\\r\\n")
    
    // Add reference text
    body.append("--\\(boundary)\\r\\n")
    body.append("Content-Disposition: form-data; name=\\"reference_text\\"\\r\\n\\r\\n")
    body.append(referenceText)
    body.append("\\r\\n--\\(boundary)--\\r\\n")
    
    request.httpBody = body
    
    URLSession.shared.dataTask(with: request) { data, response, error in
        // Handle response
    }.resume()
}
'''
    
    print(sample_code)
    print()


def run_all_tests():
    """모든 테스트 실행"""
    print("\n🚀 영어 발음 분석 API 테스트 시작\n")
    
    try:
        test_health_check()
        test_practice_sentences()
        test_phoneme_extraction()
        test_text_scoring()
        test_audio_analysis()
        create_sample_client_code()
        
        print("=" * 60)
        print("✅ 모든 테스트 완료!")
        print("=" * 60)
    
    except requests.exceptions.ConnectionError:
        print("❌ API 서버에 연결할 수 없습니다.")
        print("먼저 'python api.py'를 실행해서 서버를 시작하세요.")
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")


if __name__ == "__main__":
    run_all_tests()
