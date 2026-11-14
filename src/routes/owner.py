"""Pet Owner use case: browse and search the community feed."""
from flask import Blueprint, jsonify, request

from auth import PET_OWNER, require_roles
from db import query

bp = Blueprint("owner", __name__, url_prefix="/api/feed")


@bp.get("")
@require_roles(PET_OWNER)
def community_feed():
    q = request.args.get("q", "").strip()
    tag = request.args.get("tag", "").strip()

    sql = ("SELECT p.post_id, p.body, p.post_type, p.created_at, "
           "u.full_name AS author, pet.name AS pet_name, pet.species AS pet_species, "
           "(SELECT COUNT(*) FROM Post_Like pl WHERE pl.post_id = p.post_id) AS likes, "
           "(SELECT COUNT(*) FROM Comment c WHERE c.post_id = p.post_id) AS comments "
           "FROM Post p "
           "JOIN User u ON u.user_id = p.author_user_id "
           "LEFT JOIN Pet pet ON pet.pet_id = p.pet_id "
           "WHERE p.status = 'published'")
    params = []
    if q:
        sql += " AND (p.body LIKE %s OR u.full_name LIKE %s OR pet.name LIKE %s)"
        params += [f"%{q}%"] * 3
    if tag:
        sql += (" AND EXISTS (SELECT 1 FROM Post_Tag pt JOIN Tag t ON t.tag_id = pt.tag_id "
                "WHERE pt.post_id = p.post_id AND t.tag_name = %s)")
        params.append(tag)
    sql += " ORDER BY p.created_at DESC, p.post_id DESC"
    posts = query(sql, params)

    tags_by_post, comments_by_post = {}, {}
    for r in query("SELECT pt.post_id, t.tag_name FROM Post_Tag pt "
                   "JOIN Tag t ON t.tag_id = pt.tag_id ORDER BY t.tag_name"):
        tags_by_post.setdefault(r["post_id"], []).append(r["tag_name"])
    for r in query("SELECT c.post_id, c.body, c.created_at, u.full_name AS author "
                   "FROM Comment c JOIN User u ON u.user_id = c.author_user_id "
                   "ORDER BY c.created_at, c.comment_id"):
        comments_by_post.setdefault(r["post_id"], []).append(
            {"author": r["author"], "body": r["body"], "created_at": r["created_at"]})
    for p in posts:
        p["tags"] = tags_by_post.get(p["post_id"], [])
        p["comment_list"] = comments_by_post.get(p["post_id"], [])

    tags = [r["tag_name"] for r in query(
        "SELECT tag_name FROM Tag WHERE is_active = TRUE ORDER BY tag_name")]
    return jsonify(posts=posts, count=len(posts), tags=tags)
