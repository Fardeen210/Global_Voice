# AI Projects

A collection of AI-powered applications and tools.

## Projects

### 🌍 Global Voice - Multimodal Translator

A web application that processes YouTube videos for translation and transcription using FastAPI backend and Streamlit frontend.

#### Features
- YouTube video processing
- Audio extraction and processing
- Multi-language support (English, Spanish, French, German, Arabic, Hindi, Chinese)
- Web-based interface with Streamlit
- RESTful API with FastAPI

#### Project Structure
```
global-voice/
├── backend/
│   ├── api.py          # FastAPI application
│   └── media_utils.py  # Media processing utilities
├── frontend/
│   ├── streamlit.py    # Streamlit web interface
│   └── requirements.txt # Frontend dependencies
└── temp/               # Temporary files storage
```

#### Setup Instructions

1. **Install Dependencies**
   ```bash
   # Install Python dependencies
   pip install -r global-voice/frontend/requirements.txt
   pip install fastapi uvicorn
   ```

2. **Run the Backend**
   ```bash
   cd global-voice/backend
   uvicorn api:app --reload
   ```

3. **Run the Frontend**
   ```bash
   cd global-voice/frontend
   streamlit run streamlit.py
   ```

4. **Access the Application**
   - Frontend: http://localhost:8501
   - API: http://localhost:8000

#### API Endpoints

- `GET /` - Welcome message
- `GET /process_youtube` - Process YouTube video (params: url, lang)
- `POST /upload` - Upload file

## Development

This project uses:
- **Python** for backend and frontend
- **FastAPI** for REST API
- **Streamlit** for web interface
- **uv** for dependency management

## License

MIT License
