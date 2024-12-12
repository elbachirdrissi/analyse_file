import os
import xlrd
import docx2pdf
from django.shortcuts import render, redirect
from django.contrib.staticfiles import finders
import google.generativeai as genai
import nltk
import pandas as pd

from pages.models import UploadedFile

file_path = finders.find('data/data.txt')
if file_path:
    with open(file_path, 'r', encoding='utf-8') as file:
        text_content = file.read()
else:
    raise FileNotFoundError("File not found in static files.")

genai.configure(api_key="AIzaSyBy9czHsgzweMg3Q_Hy1N9w5EzoxYprytQ")

def query_gpt(prompt,file=None):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    if file:
        file_extension = os.path.splitext(file)[1].lower()



        myfile = genai.upload_file(file)
        response = model.generate_content(
            [myfile, "\n\n", prompt]
        )
    else:
        response = model.generate_content(prompt)
    return response.text

def clear_chat(request):
    if request.method == 'GET':
        # Clear the session data for the conversation
        request.session['conversation'] = []
    return redirect('index')


def index(request):
    conversation = request.session.get('conversation', [])
    if request.method == 'POST':
        user_query = request.POST.get('user_message')
        print("00000000000000000")
        print(user_query)
        file = request.FILES.get('file')
        print(file)
        if file:
            print("111111111111111111111111111111")
            print(file)
            uploaded_file = UploadedFile.objects.create(file=file)
            filePath = uploaded_file.file.path
            print(filePath)
            if user_query:
                prompt = f"""
                User: {user_query}
                the user attache a file 
                (response as HTML Format in a div without entire html structure) if the text in arabic add the attribut dir="rtl" to the div
                BOT: 
                """
                bot_response = query_gpt(prompt,filePath)
                print(bot_response)
            else:
                bot_response = "لم تكتب شيئا، تفضل بالسؤال"
        else:
            print("222222222222222222222222222222222")
            if user_query:
                prompt = f"""
                {text_content}
                User: {user_query}
                BOT:
                """
                bot_response = query_gpt(prompt)
                print(bot_response)
            else:
                bot_response = "لم تكتب شيئا، تفضل بالسؤال"

        conversation.append( {'sender': 'user', 'text': user_query} )
        conversation.append( {'sender': 'bot', 'text': bot_response} )
        request.session['conversation'] = conversation

    return render(request, 'chatBoot_CBAHI.html', {'conversation': conversation})
