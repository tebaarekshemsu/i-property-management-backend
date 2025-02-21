from fastapi import APIRouter

router = APIRouter(prefix='/admin', tags=['Admin'])

@router.get('/')
def index():
    #
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

@router.post('/house-post')
def post(request):
    return 'posting'