from fastapi import FastAPI, Response, HTTPException, status, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import session

router = APIRouter(
    prefix="/vote",
    tags=["vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.vote, db: session=Depends(database.get_db), 
         current_user:  schemas.userout=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post2).filter(vote.post_ID == models.Post2.ID).first()
    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post {vote.post_ID} does not exit")
    vote_query = db.query(models.vote).filter(vote.post_ID == models.vote.ID_post, 
                                              current_user.ID_user == models.vote.ID_user)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"you've already liked this post {vote.post_ID}")
        new_vote = models.vote(ID_user=current_user.ID_user, ID_post=vote.post_ID)
        db.add(new_vote)
        db.commit()
        return {"message":" you like this post succesfully"}
    else: 
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"you've not liked this post")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "you just unlike this post  successfully"}
        

