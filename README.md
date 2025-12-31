# BPM Bat 🦇

A modern Python web application to detect the Beats Per Minute (BPM) of your music tracks instantly. Built with **Streamlit** and **Librosa**.

## Features

-   **Multi-file Upload**: Drag and drop multiple MP3 or WAV files at once.
-   **Analyze All**: Process your entire queue with a single click.
-   **Modern UI**: Dark mode interface with a clean, horizontal "track card" layout.
-   **Persistent Results**: Results are saved in the session so you don't lose them as you work.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Batcave765/BPMAnalyzer.git
    cd BPMAnalyzer
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the application locally:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## Technologies

-   [Streamlit](https://streamlit.io/) - Frontend
-   [Librosa](https://librosa.org/) - Audio Analysis
