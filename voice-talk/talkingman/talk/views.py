from django.shortcuts import render
from django.http import JsonResponse
from googletrans import Translator
import pytesseract
from PIL import Image
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import ImageUploadForm, AudioUploadForm
from django.core.files.storage import default_storage
import speech_recognition as sr
from pydub import AudioSegment
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import os
import pytesseract
from .forms import ImageUploadForm

def text_view(request):
    return render(request, 'text.html')

def language(request):
    return render(request, 'inputindex.html')

def image_view(request):
    return render(request, 'imageupload.html')

def audio_view(request):
    return render(request, 'audio.html')

def language_selection(request):
    return render(request, 'language_selection.html')

def translation_page(request):
    return render(request, 'translation_page.html')

def text(request):
    return render(request, 'text.html')

def home(request):
    return render(request, 'index.html')

def home_page(request):
    if request.method == 'POST':
        pass
        # input_language = request.POST.get('inputLanguage')
        # output_language = request.POST.get('outputLanguage')

        # Pass the selected languages to the template or perform any other logic
        # context = {
        #     'input_language': input_language,
        #     'output_language': output_language,
        # }
        # return render(request, 'home_page.html', context)
    return render(request, 'home_page.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('select_language')  # Replace 'home' with your main page
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')


def index_selection(request):
    if request.method == 'POST':
        input_language = request.POST.get('inputLanguage')
        output_language = request.POST.get('outputLanguage')
        # Save the languages to the session (if needed)
        request.session['input_language'] = input_language
        request.session['output_language'] = output_language

        # Redirect to the next page (adjust 'translation_page' as needed)
        return render(request,'inputindex.html')  # Change to your actual translation view name

    # If the request is GET, just render the input index template
    return render(request, "inputindex.html")

def handle_input_selection(request):
    if request.method == 'POST':
        selected_input = request.POST.get('selectedIndex')
        input_language = request.session['input_language']
        output_language = request.session['output_language'] 
        context = {
            'input_language':input_language,
            'output_language': output_language
        }
        # print("qwerty", input)

        if selected_input == 'text':
            return render(request, 'text.html', context)  # URL pattern name for the text page
        elif selected_input == 'image':
            return render(request, 'imageupload.html', context)  # URL pattern name for the image page
        elif selected_input == 'audio':
            return render(request, 'audio.html', context)  # URL pattern name for the audio page
        else:
            return redirect('index_selection')  # URL pattern for the index page, in case no selection

    return render(request, 'inputindex.html')


# Text translation view
def translate_text1(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        language = request.POST.get('language')
        translated = translator.translate(text, dest=language)
        return JsonResponse({'translated_text': translated.text})



translator = Translator()
#*****************************************************************************************************************************

# Assuming VALID_LANGUAGES is a list of valid language codes for translation
VALID_LANGUAGES = ['en', 'hi', 'te', 'ta', 'es', 'fr', 'de', 'it', 'zh-cn', 'ru', 'hi-IN']  # Add other languages as needed
VALID_OCR_LANGUAGES = {'en': 'eng', 'hi': 'hin', 'te': 'tel', 'ta': 'tam'}  # Mapping of output languages to Tesseract OCR languages

def upload_image(request):
    if request.method == 'POST':
        try:
            image_file = request.FILES.get('image')
            if not image_file:
                return JsonResponse({'error': 'No image file provided'}, status=400)

            input_language = request.POST.get('input_language', 'en')  # Default to English for OCR
            output_language = request.POST.get('output_language', 'en')  # Default to English for output translation

            print("input", input_language)
            print("output", output_language)

            # Ensure the output language is valid for translation
            if output_language not in VALID_LANGUAGES:
                return JsonResponse({'error': 'Invalid output language'}, status=400)

            # Map input language to Tesseract OCR language
            ocr_language = VALID_OCR_LANGUAGES.get(input_language, 'eng')  # Default to English OCR if unsupported language

            # Extract text from the image using pytesseract for the selected input language
            image = Image.open(image_file)
            extracted_text = pytesseract.image_to_string(image, lang=ocr_language)  # OCR in the selected language

            if not extracted_text.strip():
                return JsonResponse({'error': 'No text extracted from the image'}, status=400)

            # Initialize the translator
            translator = Translator()

            # Translate the extracted text to the selected output language
            translation = translator.translate(extracted_text, src=input_language, dest=output_language)  # Translate from input to output language
            translated_text = translation.text

            return JsonResponse({'translated_text': translated_text})

        except Exception as e:
            print(f"Error: {str(e)}")  # Log the error in the console
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)





#################################################################################################################################
VALID_LANGUAGES = ['en', 'hi', 'te', 'ta', 'es', 'fr', 'de', 'it', 'zh-cn', 'ru']
VALID_SPEECH_RECOGNITION_LANGUAGES = {'en': 'en-US', 'hi': 'hi-IN', 'te': 'te-IN', 'ta': 'ta-IN'}

@csrf_exempt
def upload_audio(request):
    if request.method == "POST" and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
        input_language = request.POST.get('input_language', 'en')  # Use input language for recognition
        output_language = request.POST.get('output_language', 'en')  # Use output language for translation

        # Save the audio file
        file_name = default_storage.save(audio_file.name, audio_file)  # Save in MEDIA_ROOT
        file_path = default_storage.path(file_name)  # Get the full path of the saved file

        # Process the audio file to extract text
        extracted_text = process_audio(file_path, input_language)

        # Translate extracted text to output language
        translated_text = translate_text(extracted_text, output_language)

        # Remove the uploaded file if you don't need to keep it
        if os.path.exists(file_path):
            os.remove(file_path)

        return JsonResponse({'translated_text': translated_text})

    return JsonResponse({'error': 'Invalid request'}, status=400)

def process_audio(file_path, language):
    recognizer = sr.Recognizer()

    # Convert the audio file to WAV format if necessary
    wav_file_path = file_path.replace(".mp3", ".wav") if file_path.endswith('.mp3') else file_path

    if file_path.endswith('.mp3'):
        audio = AudioSegment.from_mp3(file_path)
        audio.export(wav_file_path, format="wav")  # Convert to WAV format

    try:
        with sr.AudioFile(wav_file_path) as source:
            audio_data = recognizer.record(source)  # Read the audio file

            # Recognize the speech in the audio file
            if language == 'en':
                text = recognizer.recognize_google(audio_data)
            else:
                text = recognizer.recognize_google(audio_data, language=language)  # Specify language if needed

            return text

    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"
    finally:
        # Clean up the temporary files safely
        if os.path.exists(wav_file_path):
            os.remove(wav_file_path)  # Remove the WAV file if created
        if os.path.exists(file_path):
            os.remove(file_path)  # Remove the original uploaded file
        else:
            print(f"File not found: {file_path}")

def translate_text(text, output_language):
    # Initialize the Google Translator
    translator = Translator()
    
    try:
        # Translate the text to the output language
        translated = translator.translate(text, dest=output_language)
        return translated.text
    except Exception as e:
        print(f"Translation error: {e}")
        return "Translation error occurred."
# ****************************************************************************************************************************








