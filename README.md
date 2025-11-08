# Hugging Face File Processor for Render

A Python web application that uses Hugging Face's DeepSeek-OCR model to analyze uploaded files (images, PDFs) and provide AI-powered insights. Perfect for learning how to deploy Python applications with file processing capabilities on Render!

## 🚀 Features

- File upload interface (supports images: JPG, PNG, GIF, etc. and PDF documents)
- Hugging Face DeepSeek-OCR model integration for content analysis
- Text-based chat functionality
- Ready for Render deployment
- Environment variable configuration
- Health check endpoint
- Responsive design with drag-and-drop file upload

## 📋 Prerequisites

Before you begin, make sure you have:

1. **Python 3.9+** installed on your local machine
2. **Hugging Face API Key** - Get one from [Hugging Face Hub](https://huggingface.co/settings/tokens)
3. **Render Account** - Sign up at [render.com](https://render.com)
4. **Git** installed for version control

## 🛠️ Local Setup

### 1. Clone or Download the Project

```bash
# If using git
git clone <your-repo-url>
cd render

# Or download and extract the files to your project directory
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\\Scripts\\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Hugging Face API key
# Replace 'your_huggingface_api_key_here' with your actual API key
```

Your `.env` file should look like:
```
HUGGINGFACE_API_KEY=hf_your-actual-huggingface-token-here
FLASK_ENV=development
```

### 5. Run the Application Locally

```bash
python app.py
```

Visit `http://localhost:5000` in your browser to test the application!

## 🌐 Deploying to Render

### Method 1: Using GitHub (Recommended)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Connect to Render:**
   - Go to [render.com](https://render.com) and sign in
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository
   - Choose your repository and branch

3. **Configure the service:**
   - **Name:** `openai-chat-app` (or any name you prefer)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT app:app`

4. **Set Environment Variables:**
   - In the Render dashboard, go to "Environment" tab
   - Add: `HUGGINGFACE_API_KEY` = `your_actual_huggingface_token`

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment to complete (usually 2-5 minutes)

### Method 2: Using render.yaml

If you prefer infrastructure as code:

1. The `render.yaml` file is already configured
2. Push to GitHub and connect via Render Dashboard
3. Render will automatically detect the `render.yaml` file
4. Add your environment variables in the Render dashboard

## 📁 Project Structure

```
render/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── render.yaml           # Render deployment configuration
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── templates/
│   └── index.html       # Web interface
├── README.md            # This file
└── public/              # Static assets (existing)
    └── index.html
```

## 🔧 Key Files Explained

### `app.py`
- Main Flask application with Hugging Face integration
- `/` route serves the file upload and chat interface
- `/upload` API endpoint handles file uploads and processing
- `/chat` API endpoint handles text-only conversations
- `/health` endpoint for Render health checks
- Supports image files (JPG, PNG, etc.) and PDF documents

### `requirements.txt`
- Lists all Python dependencies
- Flask for web framework
- openai (newer version) for Hugging Face API integration
- PyPDF2 for PDF text extraction
- Pillow for image processing
- python-dotenv for environment variables
- gunicorn for production server

### `render.yaml`
- Deployment configuration for Render
- Specifies Python environment and commands

## 🎯 Learning Objectives

This project teaches you:

1. **Flask Web Development** - File uploads and API endpoints
2. **Hugging Face API Integration** - Using alternative AI models
3. **File Processing** - Handling images and PDFs
4. **Environment Configuration** - Managing secrets safely
5. **Cloud Deployment** - Deploying to Render platform
6. **Frontend Integration** - File upload UI and JavaScript

## 🚀 Next Steps to Master Render

Now that you have a basic app, try these enhancements:

### Beginner Level:
- [ ] Add support for more file types (DOCX, TXT)
- [ ] Store analysis history in a database
- [ ] Add different AI models for different tasks
- [ ] Implement file size limits and validation
- [ ] Add user authentication

### Intermediate Level:
- [ ] Add PostgreSQL database (Render provides free tier)
- [ ] Implement Redis for session management
- [ ] Add file upload capabilities
- [ ] Create multiple pages/routes

### Advanced Level:
- [ ] Set up background jobs with Celery
- [ ] Add WebSocket support for real-time chat
- [ ] Implement CI/CD with GitHub Actions
- [ ] Add monitoring and logging
- [ ] Create multiple services (microservices)

## 🔍 Troubleshooting

### Common Issues:

1. **Hugging Face API Key Error:**
   - Make sure your API key is correctly set in Render environment variables
   - Check that your Hugging Face account has access to the DeepSeek-OCR model
   - Verify the API key has the correct permissions

2. **Build Failures:**
   - Check the build logs in Render dashboard
   - Ensure `requirements.txt` is properly formatted

3. **App Won't Start:**
   - Verify the start command: `gunicorn --bind 0.0.0.0:$PORT app:app`
   - Check that `app.py` has the correct Flask app instance

4. **Local Development Issues:**
   - Make sure virtual environment is activated
   - Check that `.env` file exists with correct API key

## 💡 Tips for Render

1. **Free Tier Limits:** Render free tier apps sleep after 15 minutes of inactivity
2. **Environment Variables:** Always set sensitive data as environment variables
3. **Logs:** Use Render dashboard to view application logs
4. **Monitoring:** Use the `/health` endpoint to monitor your app
5. **Scaling:** Render makes it easy to upgrade to paid plans for better performance

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

## 🤝 Contributing

This is a learning project! Feel free to:
- Fork and experiment
- Add new features
- Improve the documentation
- Share your enhanced versions

---

**Happy Learning and Building! 🎉**

Remember: This is just the beginning. Use this foundation to build more complex applications and master the Render platform!