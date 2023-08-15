import openai
from django.shortcuts import render, redirect
from django.http import HttpResponse
import time

openai.api_key = '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'

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

def generate_with_retry(prompt, max_tokens=500):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=0.8
            )
            return response.choices[0].text.strip(), None  # Return generated text and no error
        except openai.error.OpenAIError as e:
            print(f"Error: {e}")
            retries += 1
            time.sleep(RETRY_DELAY)
            if retries == MAX_RETRIES:
                return None, e  # Return no text and the last OpenAI error

def generate_story(topic, style):
    if style == "null":
        prompt = f'Write a very short story about {topic} in under 500 words.'
    else:
        prompt = f'Write a very short {style} story about {topic} in under 500 words.'
    
    return generate_with_retry(prompt)

def generate_funny_story(story):
    prompt = f'You are a hilarious comedian-writer, rewrite this story in a hilarious and creative way:\n"{story}"'
    return generate_with_retry(prompt)

def home(request):
    if request.method == 'POST':
        topic = request.POST.get('topic')
        style = request.POST.get('style')
        try:
            story, story_error = generate_story(topic, style)
            if story is None:
                error_message = f"Failed to generate story. {str(story_error)}"
                return render(request, 'chatgptApp/error.html', {'error_message': error_message})
            
            funny_story, funny_error = generate_funny_story(story)
            if funny_story is None:
                error_message = f"Failed to generate story. {str(funny_error)}"
                return render(request, 'chatgptApp/error.html', {'error_message': error_message})
            
            return render(request, 'chatgptApp/result.html', {
                'topic': topic,
                'style': style,
                'story': story,
                'funny_story': funny_story
            })
        except openai.error.OpenAIError as e:
            error_message = f"Failed to generate story. {str(e)}"
            return render(request, 'chatgptApp/error.html', {'error_message': error_message})
    return render(request, 'chatgptApp/index.html')





