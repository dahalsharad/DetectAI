from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.shortcuts import render


from .utils import predict_text,store_file,read_file,store_image,predict_image

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
        if file:
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
        data = {'path': path, 'confidence': confidence, 'final_prediction': final_prediction}
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})







