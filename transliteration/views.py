import os
import io
import csv
import json
import pandas as pd
from bs4 import BeautifulSoup
from docx import Document
from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from .utils import cyrillic_to_latin


def upload_file_view(request):
    form = UploadFileForm()

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            filename = f.name
            file_type = os.path.splitext(filename)[1].lower()

            # extract content
            raw_text = ""

            if file_type == ".txt":
                raw_text = f.read().decode('utf-8')
            elif file_type == ".docx":
                doc = Document(f)
                raw_text = '\n'.join([p.text for p in doc.paragraphs])
            elif file_type in [".csv", ".xlsx"]:
                df = pd.read_csv(f) if file_type == ".csv" else pd.read_excel(f)
                raw_text = df.to_csv(index=False)
            elif file_type == ".html":
                soup = BeautifulSoup(f.read(), 'html_parser')
                raw_text = soup.get_text()
            elif file_type == ".json":
                data = json.load(f)
                raw_text = json.dumps(data, ensure_ascii=False, indent=2)
            else:
                return HttpResponse("Unsupported file type!", status=400)

            # transliterate
            converted = cyrillic_to_latin(raw_text)

            # return same type of file
            buffer = io.BytesIO()
            response = HttpResponse(content_type="application/octet-stream")
            response["Content-Disposition"] = f"attachment; filename=File{file_type}"

            if file_type == ".txt" or file_type == ".html":
                response.write(converted)
            elif file_type == ".docx":
                doc = Document()
                for line in converted.splitlines():
                    doc.add_paragraph(line)
                doc.save(buffer)
                buffer.seek(0)
                response = HttpResponse(buffer.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                response["Content-Disposition"] = "attachment; filename=File.docx"
            elif file_type in [".csv", ".xlsx"]:
                df = pd.read_csv(io.StringIO(converted)) if file_type == ".csv" else pd.DataFrame(converted)
                output = io.StringIO() if file_type == ".csv" else io.BytesIO()
                if file_type == ".csv":
                    df.to_csv(output, index=False)
                    response.write(output.getvalue())
                else:
                    df.to_excel(output, index=False)
                    response = HttpResponse(output.getvalue(),
                                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    response["Content-Disposition"] = "attachment; filename=File.xlsx"
            elif file_type == ".json":
                response.write(converted)

            return response
        else:
            form = UploadFileForm()

    return render(request, "transliteration/file_upload.html", {"form": form})