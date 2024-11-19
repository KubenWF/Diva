from .album_route import register_albums
from .user_route import register_users
from .list_route import register_lists

def register_routes(app,db,bcrypt):
    register_albums(app,db)
    register_users(app,db,bcrypt)
    register_lists(app,db)


    return app,db