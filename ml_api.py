from fastapi.openapi.utils import get_openapi
import io
# from core.v1_parser import *

app = FastAPI()



@app.post("/process_file", response_model=ResponseDoc)
async def process_file(pcd_file: bytes = File(...)):
    temp = io.BytesIO()
    temp.write(pdf_file)

    # with pdfplumber.open(temp) as pdf:

    # Do processing

    return output
