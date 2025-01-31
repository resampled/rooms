# https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# elist:
# hack to store lists as strings in DB (seperated by \x06)

# convert elist to regular python list
def elist_to_list(elist):
    outlist = []
    builder = '' # assembles string from chars
    for char in range(len(elist)):
        if elist[char] == '\x06': 
            outlist.append(builder)
            builder = ''
        else:
            builder += elist[char]
    outlist.append(builder) # join last
    return outlist

# append string to elist (raises exception if \x06 found)
def elist_append(elist,new):
    if '\x06' in new:
        raise Exception('Found invalid joining character x06')
    if elist == '' or elist == None:
        return "{new}"
    return f"{elist}\x06{new}"

# find string in elist
def elist_find(elist,query):
    list_ = elist_to_list(elist)
    for item in list_:
        if item == query:
            return True
    return False
