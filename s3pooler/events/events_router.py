# importa todas as callbacks definidas
from s3pooler.events.events import *
from s3pooler.register.router import Router
# local responsável por criar o dicionário de associação entre cada rota
# e a callback correspondente que deva tratá-la. Exemplo:
router = Router()
router.register('/api/user/login', login, 'Login')
router.register('/api/user/register', user_created, 'User_Created')
router.register('/api/posts/create', post_created, 'Post_Created')
router.register('/api/posts/like', post_reaction, 'Post_Reaction')
router.register('/api/comments/like', comment_reaction, 'Comment_Reaction')
router.register('/api/posts/comments/create', comment_created, 'Comment_Created')
router.register('/api/posts/feed', feed_scrolled, 'Feed_Scroled')
router.register('/api/user/accept_follow', accepted_follow , 'Accepted_Follow')
#router.register('/api/user/follow', follow_request , 'Follow_Requested')

router.register('/api/user/update/{user_id}')
router.register('/api/posts/update/{post_id}')
router.register('/api/posts/delete/{post_id}')
router.register('/api/posts/comments/update/{comment_id}')
router.register('/api/posts/comments/delete/{comment_id}')
