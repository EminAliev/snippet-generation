import uvicorn
import os
import aiofiles
from typing import Optional
from core.summarization.snippet_service import SnippetGeneration
from core.parsers.prepare_service import PrepareService
from core.dto.db_service import DbService

from fastapi import Form, FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

upload_folder = os.path.dirname(__file__) + '\\upload\\'


@app.post("/snippet/create")
async def create_snippet(file: Optional[UploadFile] = File(None), url: Optional[str] = Form(None)):
    result = {}
    prepare_service = PrepareService()
    snippet_service = SnippetGeneration()
    db_service = DbService()
    if file:
        file_path = upload_folder + f'{file.filename}'
        db_service.insert_to_feeds(file_name=file.filename)
        feed_id = db_service.get_id_feed()
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        rss_feed = prepare_service.parse_rss_feed(file_path)
        for i, entry in enumerate(rss_feed):
            url_news = prepare_service.get_only_text(entry['url'])
            title = entry['title']
            snippet = snippet_service.generate_snippet(file_name=url_news)
            result[title] = snippet
            db_service.insert_snippets(title=title, snippet=snippet, feed_id=feed_id)
    else:
        db_service.insert_to_feeds(url=url)
        feed_id = db_service.get_id_feed()
        rss_feed = prepare_service.read_feed(url)
        rss_result = prepare_service.parse_rss_feed(rss_feed)
        for i, entry in enumerate(rss_result):
            url_news = prepare_service.get_only_text(entry['url'])
            url_news = ''.join(url_news)
            title = entry['title']
            snippet = snippet_service.generate_snippet(text=url_news)
            result[title] = snippet
            db_service.insert_snippets(title=title, snippet=snippet, feed_id=feed_id)

    return result


@app.get('/feeds')
async def list_feeds(request: Request):
    result = {}
    db_service = DbService()
    feeds = db_service.get_all_feeds()
    for feed in feeds:
        result[feed[1]] = feed[0], feed[2]
    return result


@app.get('/feed/{feed_id}')
async def feed_view(request: Request, feed_id):
    result = {}
    db_service = DbService()
    snippets = db_service.get_snippets_from_feed(feed_id=feed_id)
    for snippet in snippets:
        result[snippet[0]] = snippet[1]
    return result



if __name__ == '__main__':
    uvicorn.run(app=app)