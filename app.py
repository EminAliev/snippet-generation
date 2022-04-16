import uvicorn
import os
import aiofiles
from typing import Optional
from core.summarization.snippet_service import SnippetGeneration
from core.parsers.prepare_service import PrepareService

from fastapi import Form, FastAPI, File, UploadFile

app = FastAPI()


upload_folder = os.path.dirname(__file__) + '\\upload\\'


@app.post("/snippet/create")
async def create_snippet(file: Optional[UploadFile] = File(None), url: Optional[str] = Form(None)):
    result = {}
    prepare_service = PrepareService()
    snippet_service = SnippetGeneration()
    if file:
        file_path = upload_folder + f'{file.filename}'
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()  
            await out_file.write(content)
        rss_feed = prepare_service.parse_rss_feed(file_path)
        for i, entry in enumerate(rss_feed):    
            url_news = prepare_service.get_only_text(entry[i]['url'])
            title = entry[i]['title']
            snippet = snippet_service.generate_snippet(url_news)
            result[title] = snippet
    else:
        rss_feed = prepare_service.read_feed(url)
        rss_result = prepare_service.parse_rss_feed(rss_feed)
        for i, entry in enumerate(rss_feed):    
            url_news = prepare_service.get_only_text(entry[i]['url'])
            title = entry[i]['title']
            snippet = snippet_service.generate_snippet(url_news)
            result[title] = snippet
    return result

if __name__ == '__main__':
    uvicorn.run(app=app)
