"""
영어 발음 학습 웹 앱 (Streamlit)
사용자가 녹음하고 즉시 피드백을 받을 수 있습니다
"""

import streamlit as st
import tempfile
import os
from pronunciation_analyzer import PronunciationAnalyzer

# 페이지 설정
st.set_page_config(
    page_title="영어 발음 AI 코치",
    page_icon="🎤",
    layout="wide"
)

# 세션 상태 초기화
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = PronunciationAnalyzer(model_size="base")
if 'history' not in st.session_state:
    st.session_state.history = []

# 앱 헤더
st.title("🎤 영어 발음 AI 코치")
st.markdown("""
**AI가 당신의 영어 발음을 분석하고 개선 방법을 알려드립니다!**
- ✅ 실시간 발음 정확도 측정
- ✅ 음소 단위 상세 분석
- ✅ 개인 맞춤 피드백
""")

st.divider()

# 사이드바 - 설정
with st.sidebar:
    st.header("⚙️ 설정")
    
    # 연습 문장 선택
    practice_mode = st.selectbox(
        "연습 모드",
        ["기본 문장", "사용자 입력", "일상 회화", "비즈니스 영어"]
    )
    
    if practice_mode == "사용자 입력":
        custom_text = st.text_area(
            "연습할 문장을 입력하세요",
            placeholder="예: How are you doing today?"
        )
        reference_text = custom_text if custom_text else "Hello world"
    elif practice_mode == "일상 회화":
        reference_text = st.selectbox(
            "문장 선택",
            [
                "How are you doing today?",
                "Nice to meet you",
                "What's the weather like?",
                "I'd like a cup of coffee please"
            ]
        )
    elif practice_mode == "비즈니스 영어":
        reference_text = st.selectbox(
            "문장 선택",
            [
                "Let's schedule a meeting",
                "Could you send me the report?",
                "I'll get back to you soon",
                "Thank you for your time"
            ]
        )
    else:
        reference_text = "Hello world, how are you today?"
    
    st.divider()
    
    # 분석 옵션
    st.subheader("분석 옵션")
    analyze_prosody = st.checkbox("운율 분석 (속도, 억양)", value=True)
    show_phonemes = st.checkbox("음소 상세 보기", value=False)
    
    st.divider()
    
    # 통계
    if st.session_state.history:
        st.subheader("📈 학습 통계")
        avg_score = sum(h['score'] for h in st.session_state.history) / len(st.session_state.history)
        st.metric("평균 점수", f"{avg_score:.1f}점")
        st.metric("총 연습 횟수", len(st.session_state.history))

# 메인 영역
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🎯 연습할 문장")
    st.info(reference_text)
    
    # 발음 팁
    with st.expander("💡 발음 팁"):
        st.markdown("""
        - 천천히, 또박또박 발음하세요
        - 각 단어의 강세를 신경쓰세요
        - 자연스러운 속도로 말하세요
        - 문장 끝의 억양에 주의하세요
        """)
    
    st.divider()
    
    # 오디오 업로드 또는 녹음
    st.subheader("🎙️ 음성 입력")
    
    audio_source = st.radio(
        "입력 방식",
        ["파일 업로드", "녹음하기"],
        horizontal=True
    )
    
    audio_file = None
    
    if audio_source == "파일 업로드":
        uploaded_file = st.file_uploader(
            "오디오 파일을 업로드하세요 (mp3, wav, m4a)",
            type=['mp3', 'wav', 'm4a', 'ogg']
        )
        if uploaded_file:
            audio_file = uploaded_file
            st.audio(uploaded_file, format='audio/wav')
    else:
        # 브라우저 녹음 (Streamlit audio_recorder 사용 가능)
        st.info("📱 녹음 기능은 브라우저의 마이크 권한이 필요합니다")
        # audio_recorder 대신 파일 업로드로 대체 (데모용)
        st.warning("현재 데모 버전에서는 파일 업로드를 사용해주세요")
    
    # 분석 버튼
    analyze_button = st.button(
        "🔍 발음 분석 시작",
        type="primary",
        disabled=(audio_file is None),
        use_container_width=True
    )

with col2:
    st.header("📊 분석 결과")
    
    if analyze_button and audio_file:
        with st.spinner("AI가 발음을 분석하고 있습니다..."):
            # 임시 파일로 저장
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                tmp_file.write(audio_file.read())
                tmp_path = tmp_file.name
            
            try:
                # 전체 분석 실행
                result = st.session_state.analyzer.full_analysis(
                    tmp_path,
                    reference_text
                )
                
                # 결과 표시
                st.success("분석 완료!")
                
                # 인식된 텍스트
                st.subheader("🗣️ 인식된 텍스트")
                st.code(result['spoken_text'], language=None)
                
                # 점수 표시
                st.subheader("🎯 발음 점수")
                score = result['pronunciation']['overall_score']
                
                # 게이지 차트 (progress bar)
                score_color = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
                st.markdown(f"### {score_color} {score}점")
                st.progress(score / 100)
                
                # 세부 점수
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric(
                        "단어 정확도",
                        f"{result['pronunciation']['word_accuracy']}%"
                    )
                with col_b:
                    st.metric(
                        "음소 유사도",
                        f"{result['pronunciation']['phoneme_similarity']}%"
                    )
                
                st.divider()
                
                # 피드백
                st.subheader("💬 AI 피드백")
                st.markdown(result['feedback'])
                
                # 틀린 단어 상세
                if result['pronunciation']['mispronounced_words']:
                    st.divider()
                    st.subheader("❌ 개선이 필요한 부분")
                    
                    for error in result['pronunciation']['mispronounced_words']:
                        with st.container():
                            st.markdown(
                                f"**위치 {error['position'] + 1}**: "
                                f"`{error['expected']}` → 당신: `{error['spoken']}`"
                            )
                
                # 음소 상세 (옵션)
                if show_phonemes:
                    st.divider()
                    st.subheader("🔤 음소 분석")
                    ref_phonemes = st.session_state.analyzer.get_phonemes(reference_text)
                    spoken_phonemes = st.session_state.analyzer.get_phonemes(result['spoken_text'])
                    
                    col_p1, col_p2 = st.columns(2)
                    with col_p1:
                        st.caption("참조 음소")
                        st.code(' '.join(ref_phonemes), language=None)
                    with col_p2:
                        st.caption("인식 음소")
                        st.code(' '.join(spoken_phonemes), language=None)
                
                # 운율 분석 (옵션)
                if analyze_prosody and result['prosody'].get('speaking_rate', 0) > 0:
                    st.divider()
                    st.subheader("🎵 운율 분석")
                    
                    col_pr1, col_pr2, col_pr3 = st.columns(3)
                    with col_pr1:
                        st.metric("말하기 속도", f"{result['prosody']['speaking_rate']:.1f}")
                    with col_pr2:
                        st.metric("피치 변화", f"{result['prosody']['pitch_variation']:.1f}")
                    with col_pr3:
                        st.metric("에너지 변화", f"{result['prosody']['energy_variation']:.4f}")
                
                # 히스토리에 추가
                st.session_state.history.append({
                    'reference': reference_text,
                    'spoken': result['spoken_text'],
                    'score': score
                })
                
            except Exception as e:
                st.error(f"분석 중 오류 발생: {e}")
                st.info("오디오 파일 형식을 확인해주세요. WAV 파일을 권장합니다.")
            
            finally:
                # 임시 파일 삭제
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
    
    elif not audio_file:
        st.info("👆 왼쪽에서 음성을 녹음하거나 파일을 업로드하세요")

# 푸터
st.divider()
st.caption("💡 Powered by OpenAI Whisper, Pronouncing Library & AI Analysis")

# 학습 히스토리
if st.session_state.history:
    with st.expander("📚 최근 학습 기록"):
        for i, record in enumerate(reversed(st.session_state.history[-5:])):
            st.text(f"{len(st.session_state.history) - i}. {record['reference'][:50]}... - 점수: {record['score']:.1f}점")
