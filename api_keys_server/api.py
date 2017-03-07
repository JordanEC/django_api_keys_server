from api_keys_server.models import APIKey


def valid_key(api_key):
    return APIKey.objects.filter(api_key=api_key).exists()


def find_duplicates(string_list):
    duplicates = {}
    l = string_list.split(',')
    for row_index, row_word in enumerate(l):
        positions = []
        for col_index, col_word in enumerate(l):
            if not row_index == col_index and row_word == col_word:
                positions.append(col_index)
        if positions:
            d = ""
            for p in positions:
                d += "%s, " % p
            d += "%d" % row_index
            duplicates[row_word] = d
    return duplicates


def format_response(duplicates):
    if duplicates:
        duplicates_formatted = ""
        for d in duplicates:
            duplicates_formatted += "{\"word\":\"%s\", <br>\"positions\":{%s}<br>},<br>" % (d, duplicates[d])
        return "{<br>%s<br>}" % duplicates_formatted[:-5]
    else:
        return "{}"


