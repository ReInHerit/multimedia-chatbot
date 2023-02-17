from transformers import AutoProcessor, AutoModelForCausalLM
import torch
from PIL import Image
import urllib.request
from io import BytesIO

# torch.hub.download_url_to_file('http://images.cocodataset.org/val2017/000000039769.jpg', 'cats.jpg')
# torch.hub.download_url_to_file('https://huggingface.co/datasets/nielsr/textcaps-sample/resolve/main/stop_sign.png',
#                                'stop_sign.png')
# torch.hub.download_url_to_file('https://cdn.openai.com/dall-e-2/demos/text2im/astronaut/horse/photo/0.jpg',
#                                'astronaut.jpg')

git_processor_base = AutoProcessor.from_pretrained("microsoft/git-base-vqav2")
git_model_base = AutoModelForCausalLM.from_pretrained("microsoft/git-base-vqav2")

git_processor_large = AutoProcessor.from_pretrained("microsoft/git-large-vqav2")
git_model_large = AutoModelForCausalLM.from_pretrained("microsoft/git-large-vqav2")

device = "cuda" if torch.cuda.is_available() else "cpu"

git_model_base.to(device)
git_model_large.to(device)


def generate_answer_git(processor, model, image, question):
    # prepare image
    pixel_values = processor(images=image, return_tensors="pt").pixel_values

    # prepare question
    input_ids = processor(text=question, add_special_tokens=False).input_ids
    input_ids = [processor.tokenizer.cls_token_id] + input_ids
    input_ids = torch.tensor(input_ids).unsqueeze(0)

    generated_ids = model.generate(pixel_values=pixel_values, input_ids=input_ids, max_length=50)
    generated_answer = processor.batch_decode(generated_ids, skip_special_tokens=True)

    return generated_answer


def generate_answers(image_path, question):
    urllib.request.urlretrieve(image_path, "file_name")
    image = Image.open("file_name")
    if max(image.size[0], image.size[1]) > 1600:
        scale_rate = 1600 / max(image.size[0], image.size[1])
        x = int(image.size[1] * scale_rate)
        y = int(image.size[0] * scale_rate)
        image = image.resize((x, y))
    answer_git_base = generate_answer_git(git_processor_base, git_model_base, image, question)
    answer_git_large = generate_answer_git(git_processor_large, git_model_large, image, question)

    return answer_git_base, answer_git_large
