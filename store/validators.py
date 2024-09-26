from rest_framework.exceptions import ValidationError


def validate_file_size(file):
    max_size_kb = 2000

    if file.size > max_size_kb * 1024:  # convert kb to bytes
        raise ValidationError(f'File size cannot be greater than {max_size_kb} KB')
