# importa todas as callbacks definidas
from s3pooler.events.events import *

# local responsável por criar o dicionário de associação entre cada rota
# e a callback correspondente que deva tratá-la. Exemplo :

router = {
    #'/api/user/login': login,
    #'/api/user/register': user_created,
    #'api/posts/create' : post_created,
    #'api/posts/like' : reaction,
    #'api/posts/comments/create' : comment
}
