import os
import json
from pathlib import Path
from aiohttp import web
import pypdf

# Shared memory file
CONTEXT_FILE = Path("latest_candidate.json")

async def upload_handler(request: web.Request) -> web.Response:
    reader = await request.multipart()
    field = await reader.next()
    
    role = "Software Engineer"
    resume_text = "No resume provided."
    
    while field:
        if field.name == 'role':
            val = await field.read_chunk()
            role = val.decode('utf-8')
        
        if field.name == 'resume':
            filename = "temp_resume.pdf"
            with open(filename, 'wb') as f:
                while True:
                    chunk = await field.read_chunk()
                    if not chunk: break
                    f.write(chunk)
            
            try:
                # Extract text from PDF
                reader_pdf = pypdf.PdfReader(filename)
                resume_text = ""
                for page in reader_pdf.pages:
                    resume_text += page.extract_text() + "\n"
            except Exception as e:
                print(f"PDF Error: {e}")
        
        field = await reader.next()

    # Save to JSON for the Agent
    data = {"role": role, "resume_text": resume_text[:5000]}
    with open(CONTEXT_FILE, "w") as f:
        json.dump(data, f)

    return web.json_response({"status": "ok"})

async def index_handler(request):
    # Serve the HTML file
    return web.FileResponse('index.html')

app = web.Application()
app.router.add_get('/', index_handler)
app.router.add_post('/upload', upload_handler)

if __name__ == "__main__":
    print("UI Server running at: http://localhost:8080")
    web.run_app(app, host="127.0.0.1", port=8080)