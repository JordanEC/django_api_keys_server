from api_keys_server.models import APIKey


def valid_key(api_key):
    return APIKey.objects.filter(api_key=api_key).exists()


def get_duplicates(data_list):
    duplicates = []
    words = set()

    for row_index, row_word in enumerate(data_list):
        positions = []
        for col_index, col_word in enumerate(data_list):
            if not row_index == col_index and row_word == col_word:
                positions.append(col_index)
        if positions:
            if not row_word in words:
                positions.append(row_index)
                positions.sort()
                duplicate = {'word': row_word, 'positions': positions}
                words.add(row_word)
                duplicates.append(duplicate)
    return duplicates
