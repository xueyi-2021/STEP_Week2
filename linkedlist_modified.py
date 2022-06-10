class linkedlist_node:
    def __init__(self, url, contents):
        self.url = url
        self.contents = contents
        self.prev = None   #一個前のページ
        self.next = None   #一個後ろのページ


class cache_linkedlist:
    def __init__(self, n):
        self.head = None
        self.tail = None
        self.n = n
        self.len = 0
        self.dict_data = {}            #O(1)で検索用

    def access_page(self, url, contents):
        new_page = linkedlist_node(url, contents)
        if self.head is None:           #最初のページをアクセスする
            self.head = new_page
            self.tail = self.head
            self.len += 1
            self.dict_data[url] = new_page
        else:
            if url not in self.dict_data:         #cacheに保存されていない場合  O(1)
                if self.len >= self.n:                 #when cache is full
                    del self.dict_data[self.head.url]  #辞書の中で一番前のページを削除
                    self.head = self.head.next         #連結リストの中で一番前のページを削除
                    self.head.prev = None
                    self.tail.next = new_page
                    new_page.prev = self.tail
                    self.tail = new_page
                    self.dict_data[url] = new_page

                else:        #when cache is not full
                    self.tail.next = new_page
                    new_page.prev = self.tail
                    self.tail = new_page
                    self.dict_data[url] = new_page
                    self.len += 1

            else:            #cacheに保存されている場合
                saved_page = self.dict_data[url]
                if saved_page == self.tail:        #このページは直前アクセスしたページの時
                    pass                           #交換する必要がない
                elif saved_page == self.head:
                    self.head = self.head.next
                    self.head.prev = None
                    self.tail.next = saved_page
                    saved_page.prev = self.tail
                    saved_page.next = None
                    self.tail = saved_page
                else:

                    saved_page.prev.next = saved_page.next
                    saved_page.next.prev = saved_page.prev
                    self.tail.next = saved_page
                    saved_page.prev = self.tail
                    saved_page.next = None
                    self.tail = saved_page

    def all_pages(self):
        page = self.tail
        list_data = []
        while page is not None:
            list_data.append(page.url)
            page = page.prev
        print(list_data)
        return list_data


#初期化
cache = cache_linkedlist(4)
cache.all_pages()

cache.access_page("a.com", "AAA")
cache.all_pages() #['a.com']
cache.access_page("b.com", "BBB")
cache.all_pages() #['b.com', 'a.com']
cache.access_page("c.com", "CCC")
cache.all_pages() #["c.com", "b.com", "a.com"]
cache.access_page("d.com", "DDD")
cache.all_pages() #["d.com", "c.com", "b.com", "a.com"]
cache.access_page("d.com", "DDD")
cache.all_pages() #["d.com", "c.com", "b.com", "a.com"]
cache.access_page("a.com", "AAA")
cache.all_pages() #["a.com", "d.com", "c.com", "b.com"]
cache.access_page("c.com", "CCC")
cache.all_pages() #["c.com", "a.com", "d.com", "b.com"]
cache.access_page("a.com", "AAA")
cache.all_pages() #["a.com", "c.com", "d.com", "b.com"]
cache.access_page("a.com", "AAA")
cache.all_pages() #["a.com", "c.com", "d.com", "b.com"]
cache.access_page("e.com", "EEE")
cache.all_pages() #["e.com", "a.com", "c.com", "d.com"]
cache.access_page("f.com", "FFF")
cache.all_pages() #["f.com", "e.com", "a.com", "c.com"]
cache.access_page("e.com", "EEE")
cache.all_pages() #["e.com", "f.com", "a.com", "c.com"]
cache.access_page("a.com", "AAA")
cache.all_pages() #["a.com", "e.com", "f.com", "c.com"]

