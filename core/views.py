from django.shortcuts import render
from django.http import JsonResponse
from .forms import ImageUploadForm
from transformers import AutoProcessor, PaliGemmaForConditionalGeneration
from PIL import Image
import torch

model_id = "google/paligemma-3b-mix-224"
model = PaliGemmaForConditionalGeneration.from_pretrained(model_id).eval()
processor = AutoProcessor.from_pretrained(model_id)

def index(request):
    caption = None
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            image = Image.open(image_file)

            prompt = "caption es"
            model_inputs = processor(text=prompt, images=image, return_tensors="pt")
            input_len = model_inputs["input_ids"].shape[-1]

            with torch.inference_mode():
                generation = model.generate(**model_inputs, max_new_tokens=100, do_sample=False)
                generation = generation[0][input_len:]
                decoded = processor.decode(generation, skip_special_tokens=True)
                caption = decoded
    else:
        form = ImageUploadForm()

    return render(request, 'core/index.html', {'form': form, 'caption': caption})

