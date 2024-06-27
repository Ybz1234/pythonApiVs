from fastapi import APIRouter, HTTPException
from models.user import User
from config.db import db
from schemas.user import serializeDict, serializeList
from bson import ObjectId
import logging

user = APIRouter()


@user.post('/')
async def create_user(user: User):
    try:
        result = db.user.insert_one(dict(user))
        inserted_id = str(result.inserted_id)
        return {"message": "User created successfully", "id": inserted_id}
    except Exception as e:
        logging.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not create user")


@user.get('/')
async def find_all_users():
    try:
        return serializeList(db.user.find())
    except Exception as e:
        logging.error(f"Error fetching users: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not fetch users")


@user.put('/{id}')
async def update_user(id, user: User):
    try:
        db.user.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})
        return serializeDict(db.user.find_one({"_id": ObjectId(id)}))
    except Exception as e:
        logging.error(f"Error updating user {id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not update user")


@user.delete('/{id}')
async def delete_user(id):
    try:
        return serializeDict(db.user.find_one_and_delete({"_id": ObjectId(id)}))
    except Exception as e:
        logging.error(f"Error deleting user {id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not delete user")
