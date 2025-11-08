from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
import base64
import mimetypes
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import PyPDF2
import io
from PIL import Image

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def get_hf_client():
    """Get Hugging Face client"""
    return OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=os.getenv('HUGGINGFACE_API_KEY')
    )

@app.route('/')
def home():
    """Serve the main page"""
    return render_template('index.html')

def convert_pdf_to_text(file_content):
    """Extract text from PDF file"""
    try:
        pdf_file = io.BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")

def encode_image_to_base64(image_content):
    """Convert image to base64 for API"""
    try:
        # Verify it's a valid image
        image = Image.open(io.BytesIO(image_content))
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save as JPEG
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='JPEG', quality=85)
        img_buffer.seek(0)
        
        # Encode to base64
        encoded_image = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        return f"data:image/jpeg;base64,{encoded_image}"
    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads and process with Hugging Face model"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        prompt = request.form.get('prompt', 'Describe this content.')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check API key
        if not os.getenv('HUGGINGFACE_API_KEY'):
            return jsonify({'error': 'Hugging Face API key not configured'}), 500
        
        file_content = file.read()
        filename = secure_filename(file.filename)
        mime_type = mimetypes.guess_type(filename)[0]
        
        if not mime_type:
            return jsonify({'error': 'Unable to determine file type'}), 400
        
        # Process based on file type
        if mime_type.startswith('image/'):
            # Handle image files
            try:
                image_url = encode_image_to_base64(file_content)
                
                client = get_hf_client()
                completion = client.chat.completions.create(
                    model="deepseek-ai/DeepSeek-OCR:novita",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": prompt
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": image_url
                                    }
                                }
                            ]
                        }
                    ],
                )
                
                ai_response = completion.choices[0].message.content
                
            except Exception as e:
                return jsonify({'error': f'Error processing image: {str(e)}'}), 500
                
        elif mime_type == 'application/pdf':
            # Handle PDF files
            try:
                extracted_text = convert_pdf_to_text(file_content)
                
                client = get_hf_client()
                completion = client.chat.completions.create(
                    model="deepseek-ai/DeepSeek-OCR:novita",
                    messages=[
                        {
                            "role": "user",
                            "content": f"{prompt}\n\nDocument content:\n{extracted_text[:4000]}"  # Limit text length
                        }
                    ],
                )
                
                ai_response = completion.choices[0].message.content
                
            except Exception as e:
                return jsonify({'error': f'Error processing PDF: {str(e)}'}), 500
        else:
            return jsonify({'error': f'Unsupported file type: {mime_type}'}), 400
        
        return jsonify({
            'response': ai_response,
            'filename': filename,
            'file_type': mime_type,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Handle text-only chat requests"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Check if API key is set
        if not os.getenv('HUGGINGFACE_API_KEY'):
            return jsonify({'error': 'Hugging Face API key not configured'}), 500
        
        # Make request to Hugging Face API
        client = get_hf_client()
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-OCR:novita",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ],
        )
        
        ai_response = completion.choices[0].message.content
        
        return jsonify({
            'response': ai_response,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({'status': 'healthy', 'message': 'App is running!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)