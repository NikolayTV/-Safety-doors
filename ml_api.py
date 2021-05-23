from fastapi import FastAPI
import io

app = FastAPI()


@app.post("/process_file", response_model=ResponseDoc)
async def process_file(pcd_file: bytes = File(...)):
    temp = io.BytesIO()
    temp.write(pcd_file)

    # with pdfplumber.open(temp) as pdf:

    # Do processing

    return output
