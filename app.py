import uvicorn
import os
import aiofiles
from typing import Optional
from core.summarization.snippet_service import SnippetGeneration

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


upload_folder = os.path.dirname(__file__) + '\\upload\\'


@app.post("/snippet/create")
async def create_snippet(file: UploadFile):
    snippet_service = SnippetGeneration()
    file_path = upload_folder + f'{file.filename}'
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()  
        await out_file.write(content)
    snippet = snippet_service.generate_snippet(file_path)
    return {'snippet': snippet}

if __name__ == '__main__':
    uvicorn.run(app=app)
