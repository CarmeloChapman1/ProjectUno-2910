from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import User, Post
from app.database import get_db
from pydantic import BaseModel


app = FastAPI()

class UserCreate(BaseModel):
  username: str
  image_url: str 
  is_admin: bool

class CreatePost(BaseModel):
  user_id: int
  title: str
  post_text: str
  likes: int

class UserUpdate(BaseModel):
  username: str
  image_url: str = None

class PostUpdate(BaseModel):
  title: str
  post_text: str

#Create User
@app.post("/users/",status_code=status.HTTP_201_CREATED,response_model=UserCreate )
async def create_user(user: UserCreate,db: Session = Depends(get_db)):
     print('here')
     db_user = User(username = user.username,image_url = user.image_url,is_admin = user.is_admin)
     db.add(db_user)
     db.commit()
     db.refresh(db_user)
     return db_user

#Return all Users
@app.get("/users/")
async def read_users(name: str = None, db: Session = Depends(get_db)):
    if name:
        users = db.query(User).filter(User.username == name).all()
    else:
        users = db.query(User).all()
    return users

#Return User by ID
@app.get("/users/{user_id}")
async def read_userid(user_id: int, db: Session = Depends(get_db)):
  user = db.query(User).filter(User.id == user_id).first()
  return user

#Update User
@app.put("/users/{user_id}")
async def update_user(new_user: UserCreate, user_id: int, db: Session = Depends(get_db)):
  db_user = db.query(User).filter(User.id == user_id).first()
  if not db_user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

  db_user.username = new_user.username
  db_user.image_url = new_user.image_url

  db.commit()
  db.refresh(db_user)

  return db_user

# Change Username
@app.patch("/users/{user_id}/username")
async def patch_username(user_id: int,username: str,db: Session = Depends(get_db)):
  user = db.query(User).filter(User.id == user_id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

  old_username = user.username

  user.username = username
  db.commit()

  return {"message": f'"{old_username}" updated to {username} successfully'}

# Change Admin Status
@app.patch("/users/{user_id}/isAdmin")
async def patch_admin_status(user_id: int,is_admin: bool,db: Session = Depends(get_db)):
  user = db.query(User).filter(User.id == user_id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

  old_admin_status = user.is_admin

  user.is_admin = is_admin
  db.commit()

  return {"message": f'"{old_admin_status}" updated to {is_admin} successfully'}

# Change Image URL
@app.patch("/users/{user_id}/Img")
async def patch_image_url(user_id: int,image_url: str,db: Session = Depends(get_db)):
  user = db.query(User).filter(User.id == user_id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

  old_img_url = user.image_url

  user.image_url = image_url
  db.commit()

  return {"message": f'"{old_img_url}" updated to {image_url} successfully'}


#Delete User by ID
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int,db: Session = Depends(get_db)):
  user = db.query(User).filter(User.id == user_id).first()
  if user is None:
    raise HTTPException(status_code=404, detail="User not found")
  db.delete(user)
  db.commit()
  return {"message": "That mf was deleted successfully"}


#Create Posts
@app.post("/posts/",status_code=status.HTTP_201_CREATED,response_model=CreatePost )
async def create_post(post: CreatePost,db: Session = Depends(get_db)):
     print('here')
     db_post = Post(user_id = post.user_id,title = post.title,post_text = post.post_text, likes = post.likes)
     db.add(db_post)
     db.commit()
     db.refresh(db_post)
     return db_post

#Return all Posts
@app.get("/posts/")
async def get_posts(title: str = None, db: Session = Depends(get_db)):
    if title:
        posts = db.query(Post).filter(Post.title == title).all()
    else:
        posts = db.query(Post).all()
    return posts

#return posts by user_id
@app.get("/posts/user/{user_id}")
async def get_posts_by_user(user_id: int,db: Session = Depends(get_db)):
  post_by_user = db.query(Post).filter(Post.user_id == user_id).all()
  return post_by_user

#return posts by post_id
@app.get("/posts/{postId}")
async def get_post(postID: int,db: Session = Depends(get_db)):
  if postID:
    posts = db.query(Post).filter(Post.id == postID).all()
  else:
    posts = db.query(Post).all()


#Change post title
@app.patch("/posts/{postID}/title")
async def patch_post_title(postID: int,title: str,db: Session = Depends(get_db)):
  post = db.query(Post).filter(Post.id == postID).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

  old_post_title = post.title

  db.query(Post).filter(Post.id == postID).update({"title":title})
  #post.title = title
  db.commit()

  return {"message": f'"{old_post_title}" updated to {title} successfully'}

#Change post text
@app.patch("/posts/{postID}/text")
async def patch_post_text(postID: int,postText: str,db: Session = Depends(get_db)):
  post = db.query(Post).filter(Post.id == postID).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

  old_post_text = post.post_text

  #db.query(Post).filter(Post.id == postID).update({"post_text":postText})
  post.post_text = postText
  db.commit()

  return {"message": f'"{old_post_text}" updated to {postText} successfully'}


#UpdatePost DOES NOT WORK
@app.put("/posts/{postID}/update")
async def update_post(new_post: PostUpdate, postID: int, db: Session = Depends(get_db)):

  db_post = db.query(Post).filter(Post.id == postID).first()

  if not db_post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")

  if new_post.title is not None:
        db_post.title = new_post.title
  if new_post.post_text is not None:
        db_post.post_text = new_post.post_text

  db.commit()
  db.refresh(db_post)

  return db_post


@app.patch("/posts/{post_id}/increment_likes")
async def like_post(post_id: int, db: Session = Depends(get_db)):

    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    post.likes = (post.likes + 1 )

    db.commit()
    db.refresh(post)

    return {"message": f"Post {post_id} liked successfully", "new_likes_count": post.likes}



@app.patch("/posts/{post_id}/decrement_likes")
async def like_post(post_id: int, db: Session = Depends(get_db)):

    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    post.likes = (post.likes - 1 )

    db.commit()
    db.refresh(post)

    return {"message": f"Post {post_id} unliked successfully", "new_likes_count": post.likes}




#Delete Post by Post ID
@app.delete("/posts/{postID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(postID: int,db: Session = Depends(get_db)):
  post = db.query(Post).filter(Post.id == postID).first()
  if post is None:
    raise HTTPException(status_code=404, detail="User not found")
  db.delete(post)
  db.commit()
  return {"message": "That mf was deleted successfully"}