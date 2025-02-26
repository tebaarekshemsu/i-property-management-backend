from fastapi import APIRouter

router = APIRouter(prefix='/admin', tags=['Admin'])

# every route in admin part needs to be authenticated which means it needs token

@router.post('login')
def login(request):
    return 'login'

@router.get('/dashboard')
def dashboard():
    return 'dashboard'

@router.post('accept post request')
def accept_post_request(req):
    return 'post request accepted'

