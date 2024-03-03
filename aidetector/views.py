from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.shortcuts import render
import shutil


from .utils import *
from .texttoimage import *
from .ocr import *

def get_text(request):
    return render(request, 'text.html')

def get_about(request):
    return render(request, 'about.html')

def get_index(request):
    return render(request, 'index.html')

def get_image(request):
    return render(request, 'image.html')

    
@csrf_exempt
def process_text(request):
    if request.method == 'POST':
        file =request.FILES.get("fileToUpload")
        text = request.POST.get("inputText")
        heatmap = 1
        if file and heatmap == 1:
            file_extension = os.path.splitext(file.name)[1].lower()
            store_file(file,file_extension)
            if file_extension == ".pdf":
                pdf_to_image("uploads/files/temp.pdf", "uploads/temp/output")
            else:
                file_to_image(file_extension,"uploads/files/","uploads/temp/output")
            document_authenticity,final_confidence = start_img_processing(heatmap)

            data = {'confidence': final_confidence, 'final_prediction': document_authenticity}
            if heatmap == 1:
                create_highlighted_pdf()

            shutil.rmtree("uploads/temp/output")
            shutil.rmtree("uploads/highlight")
            return JsonResponse(data)
        

        elif file and heatmap != 1:
            file_extension = os.path.splitext(file.name)[1].lower()
            store_file(file,file_extension)
            text_from_file = read_file(file_extension)
            random_text,prediction,confidence,final_prediction=predict_text(text_from_file)
            data = {'confidence': confidence, 'final_prediction': final_prediction}
            return JsonResponse(data)
        

        elif not file and text:
            random_text,prediction,confidence,final_prediction=predict_text(text)
            data = {'confidence': confidence, 'final_prediction': final_prediction}
            return JsonResponse(data)
        

        else:
            data ={'error': "either text or file required"}
            return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})


@csrf_exempt
def process_image(request):
    if request.method == 'POST':
        image =request.FILES.get("fileToUpload")
        store_image(image, image.name)
        image_path = os.path.join('aidetector/static/image',image.name)
        path,confidence,final_prediction=predict_image(image_path)
        image_heatmap_generator(image_path)
        heatmap_path = "http://127.0.0.1:8000/aidetector/static/image_heatmap.jpg"
        data = {'path': heatmap_path, 'confidence': confidence, 'final_prediction': final_prediction}
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})







