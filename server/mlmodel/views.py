from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import CaptionModel
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import io


@csrf_exempt
def caption_generation_view(request):

    print("here")
    if request.method == 'POST' and request.FILES.get('image'):
        print("inside")
        # Handle uploaded image
        uploaded_image = request.FILES['image']
        print("got image")
        # image_path = default_storage.save('uploads/' + uploaded_image.name, ContentFile(uploaded_image.read()))
        image_bytes = uploaded_image.read()
        image = Image.open(io.BytesIO(image_bytes))
        image = image.resize((224, 224))

        # Load model
        model = CaptionModel()
        print("caption model")

        # Perform caption generation
        # image = preprocess_image(image_path)  # Implement your preprocessing function
        caption = model.generate_caption(image)
        print(caption)

        return HttpResponse(caption)

    return HttpResponse("ERROR in caption generation")