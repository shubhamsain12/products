# # import json
# # import os
# import html
# from io import BytesIO
# import os
# import subprocess
# import zipfile
# from fpdf import FPDF
# # from typing import Optional
# from reportlab.pdfgen import canvas
# from django.shortcuts import render
# from django.http import FileResponse, HttpResponse, JsonResponse
# from googletrans import Translator,LANGUAGES
# from xhtml2pdf import pisa
# from django.template.loader import get_template
# import pdfkit
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from django.views.decorators.csrf import csrf_exempt

# def get_all_indialanguages():
#     india_languages={}
#     india_keywords=['bengali', 'english', 'gujarati', 'hindi', 'kannada', 'malayalam', 'marathi', 'odia', 'punjabi', 'tamil', 'telugu', 'urdu']
#     for code, name in LANGUAGES.items():
#         #lowercase_name = name.lower()
#         if any(keyword in name for keyword in india_keywords):
#             india_languages[code] = name
#     return india_languages
  

# def getAllLanguages(request):
#     if request.method == 'GET':
#         try:
#             #here we are getting only india languages
#             indiaLang = get_all_indialanguages()
#             data = {'language_code': indiaLang}
#             return JsonResponse(data, safe=False)
#         except Exception as e:
#             print(f"Translation error: {e}")
#     return render(request, 'index.html')

# def Translate(request):                   #### this line is added
#     if request.method == 'POST':
#         input_text = request.POST.get('myText', '')
#         srcLang = request.POST.get('srcLang', '') 
#         destLang = request.POST.getlist('destLang[]')
#         getAlltranslate = {}          

#         input_text = html.unescape(input_text) # new one

#         try:   # Initialize the Translator with multiple service URLs
#             translator = Translator(service_urls=[
#                 'translate.google.com',  # Main Google Translate URL
#                 'translate.google.co.kr',  # South Korea Google Translate URL
#             ])
#             # print("translator", translator)

#             for value in destLang:
#                 translated = translator.translate(text=input_text, src=srcLang, dest=value)
#                 # print(translated)
#                 getAlltranslate[value] = translated.text
#             request.session['getAlltranslate'] = getAlltranslate    
#             return JsonResponse(getAlltranslate, safe=False)
#         except Exception as e:
#             print(f"Translation error: {e}")

#     return render(request, 'index.html')     ## this line is added

# def download_pdf(request,param1):
#     try:
#         getAlltranslate = request.session.get('getAlltranslate', 'default_value')
#         pdf_response = generate_pdf(getAlltranslate[param1])
#         return pdf_response
#     except Exception as e:
#         print("exception ",e)
#         return JsonResponse({'error': str(e)}, status=500)

# def generate_pdf(translatedText):
#     buffer = BytesIO()
#     pdf_path = os.path.join(os.path.dirname(__file__), "example.pdf")
#     font_path = r"F:\git_langtranslater\translator_web\language_converter\converter\langconvert\Sakalbharati.ttf"
#     # Create instance of FPDF class
#     pdf = FPDF() 
#     # Add content
#     pdf.add_page()
#     pdf.add_font("NotoSans", style="", fname=font_path, uni=True)
#     pdf.set_font("NotoSans", size=12)
#     # pdf.cell(0, 10, txt=translatedText, ln=True)
#     pdf.multi_cell(3500, 10, txt=translatedText, align='L')
#     # Save the pdf with name .pdf
#     pdf.output(pdf_path)
#     #return FileResponse(buffer, as_attachment=True, filename='example.pdf') 
#     response = FileResponse(open(pdf_path, "rb"), content_type="application/pdf")
#     response["Content-Disposition"] = 'attachment; filename="example.pdf"'
#     return response


# def generate_All_pdf(request):
#     font_path = r"F:\git_langtranslater\translator_web\language_converter\converter\langconvert\Sakalbharati.ttf"
#     pdfmetrics.registerFont(TTFont("Sakalbharati", font_path))
#     getAlltranslate = request.session.get('getAlltranslate', 'default_value')
#     # Create instance of FPDF class
#     zip_buffer = BytesIO()
#     i = 0
#     with zipfile.ZipFile(zip_buffer, 'a') as zip_file:
#     # Add content
#         for code in getAlltranslate:
#             i = i+1
#             buffer = BytesIO()
#             pdf = canvas.Canvas(buffer)
#             pdf.setFont("Sakalbharati", 12)
#             pdf.drawString(0,0,getAlltranslate[code])
#             pdf.showPage()
#             pdf.save()
#             zip_file.writestr(f'{code}.pdf', buffer.getvalue())
#     response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
#     response['Content-Disposition'] = 'attachment; filename=pdfs.zip'
#     return response


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import EmailSerializer
# from .models import Subscriber  # Import the model if used

# class SubscribeView(APIView):
#     def post(self, request, *args, **kwargs):
#         print('dataaaaaaaaaa',request.data['mailid'])
#         email=request.data['mailid']
#         # serializer = EmailSerializer(data=request.data)
#         serializer = EmailSerializer(data={'email': email})
#         if (email==""):
#            return Response({'detail': 'Please Enter Email Id'}, status=status.HTTP_201_CREATED) 

#         if serializer.is_valid():
#             email = serializer.validated_data['email']

           
#             if Subscriber.objects.filter(email=email).exists():
#                 return Response({'detail': 'Email already exists'}, status=status.HTTP_201_CREATED)

#             subscriber = Subscriber.objects.create(email=email)

#             return Response({'detail': 'Successfully subscribed'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({'detail': 'Please Enter Valid Email Id'}, status=status.HTTP_201_CREATED)
   

# def generate_pdf_Canvas(getAlltranslate):
#     # buffer = BytesIO()
#     pdf_path = os.path.join(os.path.dirname(__file__), "example.pdf")
#     for text in getAlltranslate:
#         pdf_canvas = canvas.Canvas('example.pdf', pagesize=letter)
#         pdf_canvas.drawString(100, 700, text)
#         pdf_canvas.save()
#     response = FileResponse(open(pdf_path, "rb"), content_type="application/pdf")
#     response["Content-Disposition"] = 'attachment; filename="example.pdf"'
#     return response  end


# import json
# import os
import html
from io import BytesIO
import os
import subprocess
import zipfile
from fpdf import FPDF
# from typing import Optional
from reportlab.pdfgen import canvas
from django.shortcuts import render
from django.http import FileResponse, HttpResponse, JsonResponse
from googletrans import Translator,LANGUAGES
from xhtml2pdf import pisa
from django.template.loader import get_template
import pdfkit
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from . models import  Contact
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmailSerializer
from .models import Subscriber  # Import the model if used
from reportlab.lib import colors
from bs4 import BeautifulSoup
from ckeditor.fields import RichTextField 
from django.template.loader import render_to_string 
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context
from weasyprint import HTML
import html

import json

def get_all_indialanguages():
    india_languages={}
    india_keywords=['bengali', 'english', 'gujarati', 'hindi', 'kannada', 'malayalam', 'marathi', 'odia', 'punjabi', 'tamil', 'telugu', 'urdu']
    for code, name in LANGUAGES.items():
        #lowercase_name = name.lower()
        if any(keyword in name for keyword in india_keywords):
            india_languages[code] = name
    return india_languages
  

def getAllLanguages(request):
    if request.method == 'GET':
        try:
            #here we are getting only india languages
            indiaLang = get_all_indialanguages()
            data = {'language_code': indiaLang}
            return JsonResponse(data, safe=False)
        except Exception as e:
            print(f"Translation error: {e}")
    return render(request, 'index.html')

def Translate(request):                   #### this line is added
    if request.method == 'POST':
        input_text = request.POST.get('myText', '')
        srcLang = request.POST.get('srcLang', '') 
        destLang = request.POST.getlist('destLang[]')
        getAlltranslate = {}          

        input_text = html.unescape(input_text) # new one

        try:   # Initialize the Translator with multiple service URLs
            translator = Translator(service_urls=[
                'translate.google.com',  # Main Google Translate URL
                'translate.google.co.kr',  # South Korea Google Translate URL
            ])
            # print("translator", translator)

            for value in destLang:
                translated = translator.translate(text=input_text, src=srcLang, dest=value)
                # print(translated)
                getAlltranslate[value] = translated.text
            request.session['getAlltranslate'] = getAlltranslate    
            return JsonResponse(getAlltranslate, safe=False)
        except Exception as e:
            print(f"Translation error: {e}")

    return render(request, 'index.html')     ## this line is added

def about(request):
    return render(request,'about.html')

def home(request):
    return render(request,'index.html')

def contact(request):
    success = False
    if request.method == 'POST':
        name = request.POST.get("name")
        company = request.POST.get("company")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        category = request.POST.get("category")
        description = request.POST.get("description")

        contact = Contact(name=name, company=company, phone=phone, email=email, category=category, description=description)
        contact.save()
        
       
        return render(request, 'contact.html', {'success': True})

    return render(request, 'contact.html')

def html_to_plain_text(soup):
    plain_text = ""
    for element in soup.descendants:
        if element.name == 'strong':
            plain_text += f"{colored(element.get_text(), 'white', attrs=['bold'])}"
        elif element.name is None:  # If it's just a NavigableString (text node)
            plain_text += element
    return plain_text




def generate_pdf(translatedText):
    data = translatedText

    # Create a PDF response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="dictionary.pdf"'

    # Create PDF
    pdf = canvas.Canvas(response, pagesize=A4)
    font_path = r"D:\products\translator_web\language_converter\converter\langconvert\Sakalbharati.ttf"
    pdfmetrics.registerFont(TTFont('Sakalbharati', font_path))
    

    pdf.setFont('Sakalbharati', 12)

    width, height = A4
    y = height - 50
    line_height = 20  # Line height for text
    margin = 20           #15
    max_width = width - 2 * margin  # Maximum width for the text

    for key, value in data.items():
        pdf.drawString(margin, y, f'{key}:')
        y -= line_height

        # Remove HTML tags from the value
        soup = BeautifulSoup(value, 'html.parser')
        plain_text = soup.get_text(separator='|')

        for val in plain_text.split('|'):
            lines = []
            words = val.strip().split(' ')
            line = ''
            for word in words:
                if pdf.stringWidth(line + word + ' ', 'Sakalbharati', 12) <= max_width:
                    line += word + ' '
                else:
                    lines.append(line)
                    line = word + ' '


            lines.append(line)

            for line in lines:
                if y < 40:
                    pdf.showPage()  # Create a new page if the next line will go out of bounds
                    pdf.setFont('Sakalbharati', 12)
                    y = height - 50  # Reset y position to the top of the new page
                print("rrrrrrrrrrrrrrrrr rrrrrrrrrrrrrrrrrr", line)
                
                pdf.drawString(margin + 15, y, line.strip())
                y -= line_height

        if y < 40:   
            pdf.showPage()  # Create a new page
            pdf.setFont('Sakalbharati', 12)
            y = height - 50  # Reset y position to the top of the new page

    pdf.save()

    return response
	





def download_pdf(request, param1):
    try:
        getAlltranslate = request.session.get('getAlltranslate', 'default_value')
        if not getAlltranslate or getAlltranslate == 'default_value':
            raise ValueError("Translation data is not available or is invalid.")
        valid_translations = {k: v for k, v in getAlltranslate.items() if v is not None}
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>My Template</title>
        </head>
        <body>
            <h1>{{ name }}</h1>
            {% for key, value in translations.items %}
                <h2>{{ key }}:</h2>
                <p>{{ value|safe }}</p>
            {% endfor %}
        </body>
        </html>
        """

        template = Template(html_template)
        context = Context({
           
            'translations': valid_translations     
        })
        html_string = template.render(context)

        pdf_file = HTML(string=html_string).write_pdf()

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="translated_text.pdf"'
        return response
    except Exception as e:
        print("Exception: ", e)
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)





def generate_All_pdf(request):
    font_path = r"D:\products\translator_web\language_converter\converter\langconvert\Sakalbharati.ttf"
    pdfmetrics.registerFont(TTFont("Sakalbharati", font_path))
    getAlltranslate = request.session.get('getAlltranslate', 'default_value')
    # Create instance of FPDF class
    zip_buffer = BytesIO()
    # i = 0
    with zipfile.ZipFile(zip_buffer, 'a') as zip_file:
    # Add content
        for code in getAlltranslate:
            # i = i+1
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=letter)
            pdf.setFont("Sakalbharati", 12)
            pdf.drawString(72, 750, getAlltranslate[code])
            pdf.showPage()
            pdf.save()
            zip_file.writestr(f'{code}.pdf', buffer.getvalue())
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=translations.zip'
    return response




class SubscribeView(APIView):
    def post(self, request, *args, **kwargs):
        print('dataaaaaaaaaa',request.data['mailid'])
        email=request.data['mailid']
        # serializer = EmailSerializer(data=request.data)
        serializer = EmailSerializer(data={'email': email})
        if (email==""):
           return Response({'detail': 'Please Enter Email Id'}, status=status.HTTP_201_CREATED) 

        if serializer.is_valid():
            email = serializer.validated_data['email']

           
            if Subscriber.objects.filter(email=email).exists():
                return Response({'detail': 'Email already exists'}, status=status.HTTP_201_CREATED)

            subscriber = Subscriber.objects.create(email=email)

            return Response({'detail': 'Successfully subscribed'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Please Enter Valid Email Id'}, status=status.HTTP_201_CREATED)
   



def generate_pdf_Canvas(getAlltranslate):
    # buffer = BytesIO()
    pdf_path = os.path.join(os.path.dirname('C:/Users/asus/Downloads'), "example.pdf")
    for text in getAlltranslate:
        pdf_canvas = canvas.Canvas('example.pdf', pagesize=letter)
        pdf_canvas.drawString(100, 700, text)
        pdf_canvas.save()
    response = FileResponse(open(pdf_path, "rb"), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="example.pdf"'
    return response

