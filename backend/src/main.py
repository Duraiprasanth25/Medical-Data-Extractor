import uvicorn
from fastapi import FastAPI, Form, UploadFile, File
from extractor import extract
import uuid
import os


app = FastAPI()

@app.post("/extract_from_doc")
def extract_from_doc(
        file_format: str = Form(...),
        file: UploadFile = File(...),
):
    contents = file.file.read()

    #file_path = "../uploads/test.pdf" #Since there are multiple users an multiple call to single server we shouldn't save hardcoded file name(Use - uuid model)

    file_path = "../uploads" + str(uuid.uuid4()) + ".pdf"
    with open(file_path, "wb") as f:
        f.write(contents)

    try:
        data = extract(file_path, file_format)
    except Exception as e:
        data = {
            'error': str(e)
        }


    if os.path.exists(file_path):
        os.remove(file_path)
    return data

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
