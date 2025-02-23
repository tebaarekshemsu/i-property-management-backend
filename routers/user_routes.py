from fastapi import APIRouter

router = APIRouter(prefix='/user', tags=['User'])

@router.get('/')
def index():
    # some statistics about the website like number of houses  number of users and so on just some generic statistic
    return 'hey'

@router.get('/house-list')
# we accept the parameter and pass it with the name in to the function
def house_list(min_price,max_price,location, type):
    #get the sorting and filter method as param and return based on the sorting and filtering method
    return 'house lists'

@router.get('/house-detail/{id}')
def house_detail(id:int):
    #return the detail of the house based on the id
    return f'detail of {id}'


@router.post('login')
def login(request):
    #we might use session
    return 'jwt'

@router.post('signup')
def signup(request):
    return 'jwt'

@router.post('/house-post')
# needs token protected route
def post(request):
    return 'posting'