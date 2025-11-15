"""
영어 발음 분석 REST API (Flask)
모바일 앱, 웹 앱에서 호출 가능한 API 엔드포인트
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import tempfile
import os
from pronunciation_analyzer import PronunciationAnalyzer

app = Flask(__name__)
CORS(app)  # CORS 허용 (프론트엔드 연결용)

# 글로벌 분석기 인스턴스
analyzer = PronunciationAnalyzer(model_size="base")


@app.route('/health', methods=['GET'])
def health_check():
    """서버 상태 확인"""
    return jsonify({
        'status': 'healthy',
        'service': 'pronunciation-analyzer',
        'version': '1.0.0'
    })


@app.route('/api/analyze', methods=['POST'])
def analyze_pronunciation():
    """
    발음 분석 API
    
    Request:
        - audio: 오디오 파일 (multipart/form-data)
        - reference_text: 참조 텍스트 (string)
        - analyze_prosody: 운율 분석 여부 (boolean, optional)
    
    Response:
        - spoken_text: 인식된 텍스트
        - pronunciation: 발음 분석 결과
        - prosody: 운율 분석 결과 (옵션)
        - feedback: AI 피드백
    """
    try:
        # 파라미터 검증
        if 'audio' not in request.files:
            return jsonify({
                'error': 'audio file is required',
                'code': 'MISSING_AUDIO'
            }), 400
        
        if 'reference_text' not in request.form:
            return jsonify({
                'error': 'reference_text is required',
                'code': 'MISSING_REFERENCE'
            }), 400
        
        audio_file = request.files['audio']
        reference_text = request.form['reference_text']
        analyze_prosody_flag = request.form.get('analyze_prosody', 'true').lower() == 'true'
        
        # 오디오 파일을 임시 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            audio_file.save(tmp_file.name)
            tmp_path = tmp_file.name
        
        try:
            # 전체 분석 실행
            result = analyzer.full_analysis(tmp_path, reference_text)
            
            # 운율 분석 제외 옵션
            if not analyze_prosody_flag:
                result['prosody'] = None
            
            return jsonify({
                'success': True,
                'data': result
            }), 200
        
        finally:
            # 임시 파일 삭제
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'code': 'ANALYSIS_FAILED'
        }), 500


@app.route('/api/transcribe', methods=['POST'])
def transcribe_only():
    """
    음성을 텍스트로만 변환 (STT only)
    
    Request:
        - audio: 오디오 파일
    
    Response:
        - text: 변환된 텍스트
    """
    try:
        if 'audio' not in request.files:
            return jsonify({
                'error': 'audio file is required',
                'code': 'MISSING_AUDIO'
            }), 400
        
        audio_file = request.files['audio']
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            audio_file.save(tmp_file.name)
            tmp_path = tmp_file.name
        
        try:
            spoken_text = analyzer.transcribe_audio(tmp_path)
            
            return jsonify({
                'success': True,
                'text': spoken_text
            }), 200
        
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'code': 'TRANSCRIPTION_FAILED'
        }), 500


@app.route('/api/score', methods=['POST'])
def score_pronunciation():
    """
    텍스트 기반 발음 스코어링 (오디오 없이)
    
    Request:
        - reference_text: 참조 텍스트
        - spoken_text: 사용자가 말한 텍스트
    
    Response:
        - score: 발음 스코어
        - details: 상세 분석 결과
    """
    try:
        data = request.get_json()
        
        if not data or 'reference_text' not in data or 'spoken_text' not in data:
            return jsonify({
                'error': 'reference_text and spoken_text are required',
                'code': 'MISSING_PARAMETERS'
            }), 400
        
        reference_text = data['reference_text']
        spoken_text = data['spoken_text']
        
        result = analyzer.calculate_pronunciation_score(reference_text, spoken_text)
        feedback = analyzer.generate_feedback(result)
        
        return jsonify({
            'success': True,
            'score': result['overall_score'],
            'details': result,
            'feedback': feedback
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'code': 'SCORING_FAILED'
        }), 500


@app.route('/api/phonemes', methods=['POST'])
def get_phonemes():
    """
    텍스트의 음소 추출
    
    Request:
        - text: 입력 텍스트
    
    Response:
        - phonemes: 음소 리스트
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'text is required',
                'code': 'MISSING_TEXT'
            }), 400
        
        text = data['text']
        phonemes = analyzer.get_phonemes(text)
        
        return jsonify({
            'success': True,
            'text': text,
            'phonemes': phonemes,
            'phoneme_count': len(phonemes)
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'code': 'PHONEME_EXTRACTION_FAILED'
        }), 500


@app.route('/api/practice-sentences', methods=['GET'])
def get_practice_sentences():
    """
    연습용 문장 목록 제공
    
    Query Parameters:
        - level: beginner/intermediate/advanced
        - category: daily/business/travel
    """
    level = request.args.get('level', 'beginner')
    category = request.args.get('category', 'daily')
    
    sentences = {
        'beginner': {
            'daily': [
                "Hello, how are you?",
                "Nice to meet you",
                "What's your name?",
                "I am fine, thank you"
            ],
            'business': [
                "Good morning",
                "Thank you for your time",
                "Please send me the file",
                "Let's have a meeting"
            ],
            'travel': [
                "Where is the hotel?",
                "How much is this?",
                "I need help please",
                "Thank you very much"
            ]
        },
        'intermediate': {
            'daily': [
                "What's the weather like today?",
                "I'd like a cup of coffee please",
                "Could you help me with this?",
                "That sounds like a great idea"
            ],
            'business': [
                "Could you send me the report?",
                "Let's schedule a meeting next week",
                "I'll get back to you soon",
                "What's your opinion on this?"
            ],
            'travel': [
                "How do I get to the airport?",
                "I'd like to make a reservation",
                "Is there a pharmacy nearby?",
                "What time does it close?"
            ]
        },
        'advanced': {
            'daily': [
                "I've been thinking about trying that new restaurant",
                "It's been quite challenging to manage everything lately",
                "The presentation went better than I expected",
                "I appreciate your understanding in this matter"
            ],
            'business': [
                "We need to reassess our strategy moving forward",
                "I'd like to discuss the quarterly projections",
                "Could you elaborate on your proposal?",
                "Let's align our objectives for the next quarter"
            ],
            'travel': [
                "I'd like to extend my reservation for two more nights",
                "Could you recommend any local attractions?",
                "Is there a shuttle service to the city center?",
                "What's the best way to get around the city?"
            ]
        }
    }
    
    return jsonify({
        'success': True,
        'level': level,
        'category': category,
        'sentences': sentences.get(level, {}).get(category, [])
    }), 200


# 에러 핸들러
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'endpoint not found',
        'code': 'NOT_FOUND'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'internal server error',
        'code': 'INTERNAL_ERROR'
    }), 500


if __name__ == '__main__':
    # 개발 서버 실행
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
