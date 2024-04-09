from fastapi import Depends, FastAPI, HTTPException, status, Response
from schemas import Blog
import models   
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List


app = FastAPI()


# creating all the models in the database
models.Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.post('/', response_model=Blog, status_code=201)
@app.post('/', response_model=Blog, status_code=status.HTTP_201_CREATED)
def create(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title,body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blogs',response_model=List[Blog])
def getAll(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    print("blogs :", blogs)
    return blogs


@app.get('/blogs/{id}',response_model=Blog, status_code=status.HTTP_200_OK)
def get(id: int,response: Response, db: Session = Depends(get_db)):
    # blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    # # blog = db.query(models.Blog).get(id)
    # print("blog :", blog)
    # if not blog:
    #     print("blog :", blog)
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {'detail': f'blog with blog {id} not found !'}
    # return blog
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        print('blog not found!')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with ID {id} not found')
    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        print('blog not found!')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with ID {id} not found')
    db.delete(blog)
    db.commit()
    return {'detail': f'blog {id} deleted successfully !'}



@app.put('/blogs/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: Blog ,db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with ID {id} not found')
    # blog.update({'title': 'updated title'})

    # Update individual fields
    for field, value in request.dict().items():
        setattr(blog, field, value)

    db.commit()
    return {'message': 'Updated sucessfully !'}