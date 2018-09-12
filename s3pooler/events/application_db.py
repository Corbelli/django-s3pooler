from s3pooler.utils.querytool import QueryTool

users = QueryTool('app_db','users')

def get_username(id):
    user = users.select('*').where('id={}'.format(id)).get()
    if (id == -1) or (len(user) == 0):
        return 'Undefined'
    return user[0]['name']
