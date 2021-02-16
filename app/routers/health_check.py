from fastapi import APIRouter, Response

router = APIRouter()


# Health Check
@router.get('/healthcheck')
async def get_health_check():
    Response(status_code=200)
