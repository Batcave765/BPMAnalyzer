import numpy as np
import scipy.io.wavfile as wav
import argparse

def generate_metronome(bpm, duration_sec=10, sr=44100):
    """
    Generates a simple metronome click track.
    """
    # Calculate samples per beat
    spb = int(sr * 60 / bpm)
    
    # Create a short click sound (10ms of noise)
    click_len = int(sr * 0.01)
    click = np.random.uniform(-1, 1, click_len) * 0.8
    # Apply fade out to click
    click *= np.linspace(1, 0, click_len)
    
    # Create the full audio buffer
    total_samples = int(sr * duration_sec)
    audio = np.zeros(total_samples)
    
    # Place clicks
    for i in range(0, total_samples, spb):
        if i + click_len < total_samples:
            audio[i:i+click_len] = click
            
    return audio

def main():
    parser = argparse.ArgumentParser(description="Generate a test audio file with a specific BPM.")
    parser.add_argument("--bpm", type=int, default=120, help="Beats per minute")
    parser.add_argument("--duration", type=int, default=10, help="Duration in seconds")
    parser.add_argument("--output", type=str, default="test_audio.wav", help="Output filename")
    
    args = parser.parse_args()
    
    print(f"Generating {args.output} at {args.bpm} BPM for {args.duration} seconds...")
    audio = generate_metronome(args.bpm, args.duration)
    
    # Save as 16-bit PCM WAV
    wav.write(args.output, 44100, (audio * 32767).astype(np.int16))
    print("Done!")

if __name__ == "__main__":
    main()
