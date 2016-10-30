from collections import namedtuple

Chapter = namedtuple('Chapter', ['title', 'text'])
Book = namedtuple('Book', ['title', 'id', 'language', 'meta', 'chapters', 'cover'])

# require the first five fields in Book, with the rest optional
Book.__new__.__defaults__ = (None,) * 5
