class cache:
    def __init__(self, N):
        self.list_data = []     #cacheをアクセス順で記録する
        self.set_data = set()   #cacheを記録する（検索用）
        self.len = N            #cacheの長さの上限

    def access_page(self, element1):
        if element1 not in self.set_data:     #cacheにないページをアクセスする時  O(1)
            self.list_data.append(element1)   #一番後ろに追加する  O(1)
            self.set_data.add(element1)       #O(1)
            if len(self.list_data) > self.len:    #上限を超えるとき
                front = self.list_data.pop(0)     #一番前の元素を削除（一番古いのページを捨てる） O(n)
                self.set_data.remove(front)       #O(1)
        else:                                 #cacheにあるページをアクセスするとき
                                              #実質cacheの中でページの位置交換、cacheの長さは変わらないので長さをチェック必要がない
            self.list_data.remove(element1)   #cacheの中でこのページを削除する  O(n)
            self.list_data.append(element1)   #一番後ろに追加する  O(1)

        #print(self.list_data)     #cacheをチェックする

    def all_pages(self):
        return self.list_data





#初期化
cache = cache(3)


cache.access_page('a')   #['a']
cache.access_page('b')   #['a', 'b']
cache.access_page('a')   #['b', 'a']
cache.access_page('c')   #['b', 'a', 'c']
cache.access_page('d')   #['a', 'c', 'd']
cache.access_page('d')   #['a', 'c', 'd']
cache.access_page('b')   #['c', 'd', 'b']
cache.access_page('b')   #['c', 'd', 'b']
cache.access_page('d')   #['c', 'b', 'd']
cache.access_page('b')   #['c', 'd', 'b']
cache.access_page('e')   #['d', 'b', 'e']
cache.access_page('f')   #['b', 'e', 'f']
cache.access_page('b')   #['e', 'f', 'b']
cache.access_page('a')   #['f', 'b', 'a']

print(cache.all_pages())