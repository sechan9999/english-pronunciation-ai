"""
영어 발음 분석 모듈
STT → Phoneme 비교 → 스코어링 → 피드백 생성
"""

import io
import re
from difflib import SequenceMatcher
from typing import Dict, List, Tuple, Optional

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("Warning: Whisper not available, using fallback STT")

try:
    import pronouncing
    PRONOUNCING_AVAILABLE = True
except ImportError:
    PRONOUNCING_AVAILABLE = False
    print("Warning: pronouncing library not available")

try:
    import librosa
    import numpy as np
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False
    print("Warning: librosa not available, prosody analysis disabled")


class PronunciationAnalyzer:
    """영어 발음 및 유창성 분석 클래스"""
    
    def __init__(self, model_size: str = "base"):
        """
        초기화
        Args:
            model_size: Whisper 모델 크기 (tiny/base/small/medium)
        """
        self.model_size = model_size
        self.whisper_model = None
        
        if WHISPER_AVAILABLE:
            try:
                self.whisper_model = whisper.load_model(model_size)
                print(f"Whisper {model_size} 모델 로드 완료")
            except Exception as e:
                print(f"Whisper 로드 실패: {e}")
    
    def transcribe_audio(self, audio_path: str) -> str:
        """
        음성을 텍스트로 변환 (STT)
        Args:
            audio_path: 오디오 파일 경로
        Returns:
            변환된 텍스트
        """
        if self.whisper_model:
            try:
                result = self.whisper_model.transcribe(audio_path)
                return result["text"].strip().lower()
            except Exception as e:
                print(f"Whisper 변환 실패: {e}")
                return ""
        else:
            # Fallback: 시뮬레이션 (실제 환경에서는 다른 STT API 사용)
            return "hello world"
    
    def get_phonemes(self, text: str) -> List[str]:
        """
        텍스트를 음소(phoneme) 리스트로 변환
        Args:
            text: 입력 텍스트
        Returns:
            음소 리스트
        """
        if not PRONOUNCING_AVAILABLE:
            # Fallback: 간단한 음절 분리
            return text.lower().split()
        
        words = re.findall(r'\w+', text.lower())
        phonemes = []
        
        for word in words:
            phones = pronouncing.phones_for_word(word)
            if phones:
                # 첫 번째 발음 선택 (CMU Dict 기반)
                phonemes.extend(phones[0].split())
            else:
                # 사전에 없으면 문자 단위로
                phonemes.extend(list(word))
        
        return phonemes
    
    def calculate_pronunciation_score(
        self, 
        reference_text: str, 
        spoken_text: str
    ) -> Dict[str, any]:
        """
        발음 정확도 스코어 계산
        Args:
            reference_text: 참조(정답) 텍스트
            spoken_text: 사용자가 말한 텍스트 (STT 결과)
        Returns:
            스코어 정보 딕셔너리
        """
        ref_words = re.findall(r'\w+', reference_text.lower())
        spoken_words = re.findall(r'\w+', spoken_text.lower())
        
        # 1. 단어 레벨 정확도
        word_matches = 0
        mispronounced_words = []
        
        max_len = max(len(ref_words), len(spoken_words))
        for i in range(max_len):
            ref_word = ref_words[i] if i < len(ref_words) else ""
            spoken_word = spoken_words[i] if i < len(spoken_words) else ""
            
            if ref_word and spoken_word:
                if ref_word == spoken_word:
                    word_matches += 1
                else:
                    mispronounced_words.append({
                        'expected': ref_word,
                        'spoken': spoken_word,
                        'position': i
                    })
        
        word_accuracy = (word_matches / len(ref_words) * 100) if ref_words else 0
        
        # 2. 음소 레벨 유사도
        ref_phonemes = self.get_phonemes(reference_text)
        spoken_phonemes = self.get_phonemes(spoken_text)
        
        phoneme_similarity = SequenceMatcher(
            None, 
            ' '.join(ref_phonemes), 
            ' '.join(spoken_phonemes)
        ).ratio() * 100
        
        # 3. 전체 스코어 (가중 평균)
        overall_score = (word_accuracy * 0.6) + (phoneme_similarity * 0.4)
        
        return {
            'overall_score': round(overall_score, 1),
            'word_accuracy': round(word_accuracy, 1),
            'phoneme_similarity': round(phoneme_similarity, 1),
            'mispronounced_words': mispronounced_words,
            'word_count': len(ref_words),
            'correct_words': word_matches
        }
    
    def analyze_prosody(self, audio_path: str) -> Dict[str, float]:
        """
        운율(prosody) 분석: 말하기 속도, 피치 변화 등
        Args:
            audio_path: 오디오 파일 경로
        Returns:
            운율 분석 결과
        """
        if not LIBROSA_AVAILABLE:
            return {
                'speaking_rate': 0.0,
                'pitch_variation': 0.0,
                'energy_variation': 0.0
            }
        
        try:
            # 오디오 로드
            y, sr = librosa.load(audio_path, sr=None)
            
            # 1. 말하기 속도 (초당 음절 수 추정)
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            speaking_rate = tempo / 60.0  # BPM to Hz
            
            # 2. 피치 변화 (F0 분석)
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            pitch_variation = np.std(pitch_values) if pitch_values else 0.0
            
            # 3. 에너지 변화
            rms = librosa.feature.rms(y=y)[0]
            energy_variation = np.std(rms)
            
            return {
                'speaking_rate': round(float(speaking_rate), 2),
                'pitch_variation': round(float(pitch_variation), 2),
                'energy_variation': round(float(energy_variation), 4)
            }
        
        except Exception as e:
            print(f"Prosody 분석 실패: {e}")
            return {
                'speaking_rate': 0.0,
                'pitch_variation': 0.0,
                'energy_variation': 0.0
            }
    
    def generate_feedback(
        self, 
        pronunciation_result: Dict, 
        prosody_result: Dict = None
    ) -> str:
        """
        분석 결과 기반 자연어 피드백 생성
        Args:
            pronunciation_result: 발음 분석 결과
            prosody_result: 운율 분석 결과 (선택)
        Returns:
            피드백 텍스트
        """
        score = pronunciation_result['overall_score']
        feedback_parts = []
        
        # 전체 평가
        if score >= 90:
            feedback_parts.append("🎉 훌륭합니다! 발음이 매우 정확해요.")
        elif score >= 75:
            feedback_parts.append("👍 좋아요! 발음이 꽤 정확합니다.")
        elif score >= 60:
            feedback_parts.append("📚 괜찮아요. 조금 더 연습하면 좋겠어요.")
        else:
            feedback_parts.append("💪 연습이 필요해요. 천천히 따라해보세요.")
        
        # 세부 점수
        feedback_parts.append(
            f"\n📊 점수: {score}점 "
            f"(단어 정확도: {pronunciation_result['word_accuracy']}%, "
            f"음소 유사도: {pronunciation_result['phoneme_similarity']}%)"
        )
        
        # 틀린 단어 피드백
        if pronunciation_result['mispronounced_words']:
            feedback_parts.append("\n❌ 개선이 필요한 단어:")
            for error in pronunciation_result['mispronounced_words'][:5]:  # 최대 5개
                feedback_parts.append(
                    f"  • '{error['expected']}' → 당신: '{error['spoken']}'"
                )
        
        # 운율 피드백
        if prosody_result and prosody_result.get('speaking_rate', 0) > 0:
            rate = prosody_result['speaking_rate']
            if rate < 1.5:
                feedback_parts.append("\n🐢 말하기 속도가 느려요. 좀 더 자연스럽게 말해보세요.")
            elif rate > 3.0:
                feedback_parts.append("\n🐇 말하기 속도가 빨라요. 천천히 또박또박 발음해보세요.")
            else:
                feedback_parts.append("\n✅ 말하기 속도가 적절해요.")
        
        return '\n'.join(feedback_parts)
    
    def full_analysis(
        self, 
        audio_path: str, 
        reference_text: str
    ) -> Dict:
        """
        전체 분석 파이프라인 실행
        Args:
            audio_path: 음성 파일 경로
            reference_text: 참조 텍스트
        Returns:
            완전한 분석 결과
        """
        # 1. STT
        spoken_text = self.transcribe_audio(audio_path)
        
        # 2. 발음 분석
        pronunciation_result = self.calculate_pronunciation_score(
            reference_text, 
            spoken_text
        )
        
        # 3. 운율 분석
        prosody_result = self.analyze_prosody(audio_path)
        
        # 4. 피드백 생성
        feedback = self.generate_feedback(pronunciation_result, prosody_result)
        
        return {
            'spoken_text': spoken_text,
            'reference_text': reference_text,
            'pronunciation': pronunciation_result,
            'prosody': prosody_result,
            'feedback': feedback
        }


# 테스트/데모용 함수
def demo_analysis():
    """분석기 데모"""
    analyzer = PronunciationAnalyzer()
    
    # 시뮬레이션 예제
    reference = "Hello world, how are you today?"
    spoken = "Hello world, how are you today"  # 마지막 단어 누락
    
    result = analyzer.calculate_pronunciation_score(reference, spoken)
    feedback = analyzer.generate_feedback(result)
    
    print("=" * 50)
    print("영어 발음 분석 데모")
    print("=" * 50)
    print(f"참조 텍스트: {reference}")
    print(f"인식 텍스트: {spoken}")
    print(f"\n{feedback}")
    print("=" * 50)


if __name__ == "__main__":
    demo_analysis()
