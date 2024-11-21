from .user_route import register_user
from .admin_route import register_admin
from .public_route import register_public

def register_routes(app,db,bcrypt):
    register_user(app,db,bcrypt)
    register_admin(app,db)
    register_public(app,db,bcrypt)


    return app,db