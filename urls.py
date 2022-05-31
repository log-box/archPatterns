from views import Index, About, Boards, CreateBoard, CreateCategory, CategoryList

# route list
routes = {
    '/': Index(),
    '/about/': About(),
    '/boards/': Boards(),
    '/create-board/': CreateBoard(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList(),
}
