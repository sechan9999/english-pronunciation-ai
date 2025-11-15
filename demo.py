#!/usr/bin/env python3
"""
영어 발음 분석 CLI 데모
실제 오디오 파일 없이도 텍스트 기반으로 테스트 가능
"""

from pronunciation_analyzer import PronunciationAnalyzer
import json


def print_separator(char='=', length=70):
    """구분선 출력"""
    print(char * length)


def demo_text_analysis():
    """텍스트 기반 발음 분석 데모"""
    print_separator()
    print("📝 텍스트 기반 발음 분석 데모")
    print_separator()
    
    analyzer = PronunciationAnalyzer()
    
    # 테스트 케이스들
    test_cases = [
        {
            'name': '완벽한 발음',
            'reference': 'Hello world, how are you today?',
            'spoken': 'Hello world, how are you today?'
        },
        {
            'name': '한 단어 누락',
            'reference': 'Hello world, how are you today?',
            'spoken': 'Hello world, how are you?'
        },
        {
            'name': '발음 오류 (철자 차이)',
            'reference': 'The weather is beautiful today',
            'spoken': 'The weater is butiful today'
        },
        {
            'name': '단어 순서 변경',
            'reference': 'I love learning English',
            'spoken': 'I English learning love'
        },
        {
            'name': '추가 단어',
            'reference': 'Good morning',
            'spoken': 'Good morning sir'
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"테스트 {i}: {case['name']}")
        print(f"{'='*70}")
        print(f"📖 참조 문장: {case['reference']}")
        print(f"🗣️  인식 문장: {case['spoken']}")
        print()
        
        # 분석 실행
        result = analyzer.calculate_pronunciation_score(
            case['reference'],
            case['spoken']
        )
        
        # 피드백 생성
        feedback = analyzer.generate_feedback(result)
        
        # 결과 출력
        print(feedback)
        
        # 상세 정보
        print(f"\n📊 상세 점수:")
        print(f"  • 전체 점수: {result['overall_score']}점")
        print(f"  • 단어 정확도: {result['word_accuracy']}%")
        print(f"  • 음소 유사도: {result['phoneme_similarity']}%")
        print(f"  • 정확한 단어: {result['correct_words']}/{result['word_count']}")
        
        if result['mispronounced_words']:
            print(f"\n🔍 틀린 단어 상세:")
            for error in result['mispronounced_words']:
                print(f"  위치 {error['position'] + 1}: "
                      f"'{error['expected']}' → '{error['spoken']}'")


def demo_phoneme_extraction():
    """음소 추출 데모"""
    print("\n\n")
    print_separator()
    print("🔤 음소 추출 데모")
    print_separator()
    
    analyzer = PronunciationAnalyzer()
    
    test_sentences = [
        "Hello world",
        "How are you?",
        "The quick brown fox",
        "I love programming",
        "Beautiful weather today"
    ]
    
    for sentence in test_sentences:
        phonemes = analyzer.get_phonemes(sentence)
        print(f"\n문장: {sentence}")
        print(f"음소: {' '.join(phonemes)}")
        print(f"음소 개수: {len(phonemes)}")


def demo_interactive_mode():
    """대화형 모드"""
    print("\n\n")
    print_separator()
    print("🎮 대화형 발음 테스트")
    print_separator()
    print("\n연습할 문장을 선택하세요:")
    
    practice_sentences = [
        "Hello, how are you?",
        "Nice to meet you",
        "What's the weather like today?",
        "I'd like a cup of coffee please",
        "Thank you for your time"
    ]
    
    for i, sentence in enumerate(practice_sentences, 1):
        print(f"{i}. {sentence}")
    
    try:
        choice = int(input("\n번호를 선택하세요 (1-5): "))
        if 1 <= choice <= 5:
            reference = practice_sentences[choice - 1]
            print(f"\n📖 연습할 문장: {reference}")
            print("🗣️  위 문장을 똑같이 입력해보세요:")
            
            spoken = input("> ")
            
            analyzer = PronunciationAnalyzer()
            result = analyzer.calculate_pronunciation_score(reference, spoken)
            feedback = analyzer.generate_feedback(result)
            
            print("\n" + "="*70)
            print(feedback)
            
        else:
            print("잘못된 선택입니다.")
    
    except (ValueError, KeyboardInterrupt):
        print("\n테스트를 종료합니다.")


def demo_comparison():
    """다양한 발음 수준 비교"""
    print("\n\n")
    print_separator()
    print("📊 발음 수준별 비교 분석")
    print_separator()
    
    analyzer = PronunciationAnalyzer()
    reference = "The weather is beautiful today"
    
    levels = [
        {
            'level': '고급 (95점)',
            'spoken': 'The weather is beautiful today',
            'description': '완벽한 발음'
        },
        {
            'level': '중급 (75점)',
            'spoken': 'The weather is beautful today',
            'description': '사소한 철자 오류'
        },
        {
            'level': '초급 (50점)',
            'spoken': 'The wether butiful today',
            'description': '여러 단어 오류'
        }
    ]
    
    print(f"\n참조 문장: {reference}\n")
    
    for level_info in levels:
        print(f"\n{'-'*70}")
        print(f"수준: {level_info['level']}")
        print(f"설명: {level_info['description']}")
        print(f"발음: {level_info['spoken']}")
        
        result = analyzer.calculate_pronunciation_score(
            reference,
            level_info['spoken']
        )
        
        print(f"실제 점수: {result['overall_score']}점")
        print(f"단어 정확도: {result['word_accuracy']}%")


def show_api_examples():
    """API 사용 예제"""
    print("\n\n")
    print_separator()
    print("🌐 API 사용 예제")
    print_separator()
    
    examples = {
        'Python': '''
# Python 클라이언트 예제
import requests

url = "http://localhost:5000/api/score"
data = {
    "reference_text": "Hello world",
    "spoken_text": "Hello world"
}

response = requests.post(url, json=data)
result = response.json()
print(f"점수: {result['score']}")
        ''',
        
        'JavaScript': '''
// JavaScript (fetch API) 예제
const analyzeText = async () => {
    const response = await fetch('http://localhost:5000/api/score', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            reference_text: 'Hello world',
            spoken_text: 'Hello world'
        })
    });
    
    const result = await response.json();
    console.log(`점수: ${result.score}`);
};
        ''',
        
        'cURL': '''
# cURL 예제
curl -X POST http://localhost:5000/api/score \\
  -H "Content-Type: application/json" \\
  -d '{
    "reference_text": "Hello world",
    "spoken_text": "Hello world"
  }'
        '''
    }
    
    for lang, code in examples.items():
        print(f"\n{lang}:")
        print(code)


def main():
    """메인 함수"""
    print("\n")
    print("=" * 70)
    print(" " * 15 + "🎤 영어 발음 AI 분석 시스템 데모")
    print("=" * 70)
    print("\n이 데모는 실제 오디오 없이 텍스트 기반으로 작동합니다.")
    print("프로덕션에서는 Whisper STT가 음성을 텍스트로 변환합니다.\n")
    
    # 모든 데모 실행
    demo_text_analysis()
    demo_phoneme_extraction()
    demo_comparison()
    
    # 대화형 모드 (선택)
    print("\n\n")
    try_interactive = input("대화형 모드를 실행하시겠습니까? (y/n): ")
    if try_interactive.lower() == 'y':
        demo_interactive_mode()
    
    # API 예제 표시
    show_api_examples()
    
    # 마무리
    print("\n\n")
    print_separator()
    print("✅ 데모 완료!")
    print_separator()
    print("\n다음 단계:")
    print("1. Streamlit 웹 앱 실행: streamlit run app.py")
    print("2. Flask API 서버 실행: python api.py")
    print("3. API 테스트: python test_api.py")
    print("\n자세한 정보는 README.md를 참조하세요.")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n프로그램을 종료합니다.")
    except Exception as e:
        print(f"\n오류 발생: {e}")
