from django.http import UnreadablePostError

def SpecialFilter(record,foo):
    print (record)

    return True