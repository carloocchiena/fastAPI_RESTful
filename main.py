from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

import uvicorn

# instantiate our FastApi application
app = FastAPI()

# initiate our test dataset
videogames = [
  {'title': 'Doom Eternal', 'rating': 4, 'cost': 45},
  {'title': 'Days Gone', 'rating': 1, 'cost': 25},
  {'title': 'The Last Of Us', 'rating': 3, 'cost': 75},
  {'title': 'Detroit:Become Human', 'rating': 5, 'cost': 30},
  {'title': 'Cyberpunk 2077', 'rating': 2, 'cost': 5},
]


# define the types of our dataset objects
class Videogame(BaseModel):
  title: str
  rating: int
  cost: int

  
# FUNCTIONS

# check existance of the videogame
def videogame_check(videogame_id):
  if not videogames[videogame_id]:
    raise HTTPException(status_code=404, detail='Game Not Found')


# create our home page route
@app.get('/')
async def root():
  return {'message': 'Hello world'}


# check if a videogames is within the list
@app.get('/videogames/{videogame_id}')
def videogame_detail(videogame_id: int):
  videogame_check(videogame_id)
  return {'videogames': videogames[videogame_id]}

  
# API METHODS

# GET
@app.get('/videogames')
def videogame_list(min_rate:Optional[int]=None, max_rate:Optional[int]=None):
  
  if min_rate and max_rate:
    
    filtered_videogames = list(
      filter(lambda rating: (min_rate <= rating['rating'] <= max_rate), videogames)
    )

    return {'videogames': filtered_videogames}
    
  return {'videogames': videogames}

  
# POST
@app.post('/videogames')
def videogame_add(videogame: Videogame):
  videogames.append(videogame)

  return {'videogames': videogames[-1]}

  
# PUT
@app.put('/videogames')
def videogame_update(videogame: Videogame, videogame_id: int):
  videogame_check(videogame_id)
  videogames[videogame_id].update(videogame)

  return {'videogames': videogames[videogame_id]}

  
# DELETE
@app.delete('/videogames')
def videogame_delete(videogame_id: int):
  videogame_check(videogame_id)
  del videogames[videogame_id]

  return {'videogames': videogames}

  
# launch our application with uvicorn
if __name__ == '__main__':
  uvicorn.run(app,host="0.0.0.0",port="8080")
