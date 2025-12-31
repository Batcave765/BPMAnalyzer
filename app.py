import streamlit as st
import librosa
import numpy as np
import tempfile
import os

# --- Configuration & Styling ---
st.set_page_config(
    page_title="BPM Analyser", 
    page_icon="🎵",
)

# Custom CSS for a modern, cleaner look
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .track-name {
        font-size: 1rem;
        font-weight: 500;
        color: #e0e0e0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .bpm-result {
        font-size: 1.5rem;
        font-weight: 700;
        color: #00e676; /* Bright Green */
    }
    /* Button Styling */
    .stButton button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- Logic ---

def analyze_bpm(file_obj):
    """
    Analyzes the BPM of the given file-like object.
    Handles temp file creation and cleanup internally.
    """
    tmp_file_path = None
    try:
        # Save uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_obj.name)[1]) as tmp_file:
            tmp_file.write(file_obj.getvalue())
            tmp_file_path = tmp_file.name

        # Load audio file (sr=None preserves original sampling rate)
        y, sr = librosa.load(tmp_file_path, sr=None)
        
        # Calculate onset envelope
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        
        # Estimate tempo
        tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
        
        # Handle scalar vs array return type
        if isinstance(tempo, np.ndarray):
             tempo = tempo[0]
             
        return round(tempo, 2)
    except Exception as e:
        st.error(f"Error processing {file_obj.name}: {e}")
        return None
    finally:
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)

def main():
    st.title("🎵 BPM Bat 🦇")
    st.markdown("Upload multiple tracks to detect their Beats Per Minute (BPM).")

    # Session State for storing results
    if 'bpm_results' not in st.session_state:
        st.session_state['bpm_results'] = {}

    # Collapsible uploader to save space and hide the default file list
    with st.expander("📂 Upload Audio Files", expanded=True):
        uploaded_files = st.file_uploader(
            "Drop your audio files here...", 
            type=["mp3", "wav"], 
            accept_multiple_files=True
        )

    if uploaded_files:
        st.markdown("---")
        
        # "Analyze All" Button
        if st.button("🚀 Analyze All Tracks", type="primary", use_container_width=True):
             with st.spinner("Analyzing all tracks..."):
                for uploaded_file in uploaded_files:
                    file_id = uploaded_file.name
                    if file_id not in st.session_state['bpm_results']:
                         bpm = analyze_bpm(uploaded_file)
                         if bpm:
                             st.session_state['bpm_results'][file_id] = bpm
                st.rerun()

        st.markdown("") # Spacing

        # Header Row
        # Using vertical_alignment="center" to align items in the middle vertically
        col1, col2, col3 = st.columns([2, 3, 1], vertical_alignment="center")
        col1.markdown("**Track Name**")
        col2.markdown("**Audio Preview**")
        col3.markdown("**BPM**")
        st.divider()

        for uploaded_file in uploaded_files:
            file_id = uploaded_file.name
            
            # Row Layout
            c1, c2, c3 = st.columns([2, 3, 1], vertical_alignment="center")
            
            with c1:
                st.markdown(f'<div class="track-name" title="{file_id}">💿 {file_id}</div>', unsafe_allow_html=True)
            
            with c2:
                st.audio(uploaded_file, format='audio/mp3')

            with c3:
                if file_id in st.session_state['bpm_results']:
                    bpm = st.session_state['bpm_results'][file_id]
                    st.markdown(f'<div class="bpm-result">{bpm}</div>', unsafe_allow_html=True)
                else:
                    if st.button("Analyze", key=f"btn_{file_id}"):
                         with st.spinner("..."):
                            bpm = analyze_bpm(uploaded_file)
                            if bpm:
                                st.session_state['bpm_results'][file_id] = bpm
                                st.rerun()

if __name__ == "__main__":
    main()
