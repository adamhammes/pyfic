from collections import namedtuple

Chapter = namedtuple('Chapter', ['title', 'text'])
Book = namedtuple('Book', ['title', 'id', 'language', 'meta', 'chapters'])
