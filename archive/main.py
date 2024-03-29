from fastapi import FastAPI, HTTPException, Depends
import aioredis
from models import Like, Comment, UserRegister, UserLogin

app = FastAPI()
redis = aioredis.from_url("redis://192.168.2.1:6379", encoding="utf-8", decode_responses=True)

# Dependency for getting the Redis connection
async def get_redis():
    async with redis.client() as conn:
        yield conn

@app.post("/register/")
async def register_user(user: UserRegister, redis=Depends(get_redis)):
    # Check if user already exists
    exists = await redis.exists(f"user:{user.username}")
    if exists:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Store user credentials in Redis
    await redis.set(f"user:{user.username}", user.password)
    return {"message": "User registered successfully"}

@app.post("/login/")
async def login_user(user: UserLogin, redis=Depends(get_redis)):
    # Retrieve user password from Redis
    stored_password = await redis.get(f"user:{user.username}")

    # Validate password
    if stored_password is None or stored_password != user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}

@app.post("/like/")
async def like_page(like: Like, redis=Depends(get_redis)):
    # Use a set for likes to avoid duplicates
    await redis.sadd(f"page:{like.page_id}:likes", like.username)
    return {"message": "Page liked successfully"}

@app.post("/comment/")
async def comment_on_page(comment: Comment, redis=Depends(get_redis)):
    # Store comments in a list
    comment_data = f"{comment.timestamp} - {comment.username}: {comment.content}"
    await redis.rpush(f"page:{comment.page_id}:comments", comment_data)
    return {"message": "Comment added successfully"}

@app.get("/page/{page_id}/")
async def get_page_info(page_id: str, redis=Depends(get_redis)):
    # Get all likes and comments for a page
    likes = await redis.smembers(f"page:{page_id}:likes")
    comments = await redis.lrange(f"page:{page_id}:comments", 0, -1)
    return {
        "likes": list(likes),
        "comments": comments
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
