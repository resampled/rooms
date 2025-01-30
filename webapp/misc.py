# https://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# hack to store lists as strings in DB (seperated by \x06)
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

def elist_append(elist,new):
    if '\x06' in new:
        raise Exception('Found invalid joining character x06')
    return f"{elist}\x06{new}"

print(elist_append('abc#123','g\x06hi#789'))
