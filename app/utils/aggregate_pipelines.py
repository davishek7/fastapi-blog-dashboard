from fastapi import Query


def posts_with_author(
    blog_id: str = None,
    slug: str = None,
    include_inactive: bool = False,
    skip: int | None = Query(None, ge=0),
    limit: int | None = Query(None, ge=1, le=100),
):
    pipeline = []

    # Match stage
    match_stage = {}
    if blog_id:
        match_stage["_id"] = blog_id
    if slug:
        match_stage["slug"] = slug
    if not include_inactive:
        match_stage["is_active"] = True
    if match_stage:
        pipeline.append({"$match": match_stage})

    # Lookup stage
    pipeline.append(
        {
            "$lookup": {
                "from": "auth",
                "localField": "author_id",
                "foreignField": "_id",
                "as": "author",
            }
        }
    )

    # Unwind stage
    pipeline.append({"$unwind": "$author"})

    # Projection stage
    pipeline.append(
        {
            "$project": {
                "_id": 1,
                "title": 1,
                "subtitle": 1,
                "slug": 1,
                "content": 1,
                "is_active": 1,
                "created_at": 1,
                "author._id": 1,
                "author.username": 1,
                "author.email": 1,
                "author.role": 1,
                "author.is_active": 1,
                "author.created_at": 1,
            }
        }
    )

    # Sort newest first
    if blog_id is None and slug is None:
        pipeline.append({"$sort": {"created_at": -1}})

    # Pagination
    if skip is not None:
        pipeline.append({"$skip": skip})

    if limit is not None:
        pipeline.append({"$limit": limit})

    return pipeline
