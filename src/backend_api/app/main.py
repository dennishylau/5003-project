from fastapi_versioning import VersionedFastAPI
from fastapi import FastAPI
import env

# entry point

app = FastAPI(title='5003 Project')


@app.get('/', tags=['general'])
async def health_check():
    return {'status': 'ok'}


@app.get('/debug', tags=['debug'])
async def debug_info():
    return {
        'ROOT_DIR': env.ROOT_DIR,
        'PYTEST_MODE': env.PYTEST_MODE,
    }


# api versioning
app = VersionedFastAPI(
    app,
    default_version=(1, 0),
    enable_latest=True,
    version_format='{major}',
    prefix_format='/v{major}',
)
