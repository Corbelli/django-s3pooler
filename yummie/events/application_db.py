from s3pooler.querytool import QueryTool

users = QueryTool('app_db','users')

def get_user(id):
    # user = users.select('*').where('id={}'.format(id)).get()
    # if (id == -1) or (len(user) == 0):
    #     return {}
    # return user[0]
    return {'created_at': None, 'name': 'Undefined'}
