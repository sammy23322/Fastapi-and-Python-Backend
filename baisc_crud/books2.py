from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field 
from typing import Optional
from starlette import status


app = FastAPI()



class Book:
    id: int
    title : str
    author: str
    description: str
    rating: int
    published_date :int

    def __init__(self,id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description 
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description= "ID  is not needd on create", default=None)
    title : str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date : int = Field(gt = 1999, lt = 2031)

    class Config:
        json_schema_extra = {
            "example"   :{
                "title" : "A new book",
                "author" : "codeingwuthroby",
                "description" : "A new dscription of a book",
                "rating" : 5 
            }
        }

BOOKS = [
    Book(1, 'computersciencepro', 'codingwithroby' , 'a very good book', 5 ,2020),
    Book(2, 'madewith python', 'codingwithroby' , 'a verynice book', 2, 2024),
    Book(3, 'docker for beginner', 'sunil singh' , 'detailed book', 1, 2020),
    Book(4, 'backend with projects', 'sharard and rahul' , 'unique projects', 4, 2020),
    Book(5, 'python for backend', 'savroop singh sethi' , 'mind opening', 3, 2026),

]



@app.get("/books", status_code=status.HTTP_200_OK)
async def get_books():
    return BOOKS




@app.get("/books/published_date", status_code=status.HTTP_200_OK)
async def get_books_by_publishing_date(date : int):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == date:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def fetch_book_by_id(book_id : int = Path(gt = 0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404 ,detail='item not found because id does not exist')



@app.get("/books/", status_code=status.HTTP_200_OK)
async def fetch_book_by_rating(book_rating : int  = Query(gt = 0, lt = 6)):
    books_by_rating =[]
    for book in BOOKS:
        if book.rating == book_rating:
            books_by_rating.append(book)
    return books_by_rating





@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request : BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book) )




@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book : BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed= True
    if not book_changed:
        raise HTTPException(status_code=404 ,detail="nothing chnaged , bacsue book was not found ")




@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt = 0)):
    book_changed =False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail="item not found")




def find_book_id(book:Book):
    if len(BOOKS) == 0 :
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book