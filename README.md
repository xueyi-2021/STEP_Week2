# STEP Week2 Homework

### 宿題1

> 行列積を求めるプログラムを書いて、行列のサイズNと実行時間Nと関係を調べてみよう 

#### コード

```python
for i in range(n): 
   for j in range(n):
       for k in range(n):
               c[i, j] += a[i, k] * b[k, j]
```

#### 結果

N=1~1500の実行時間とNの関係：

![](https://github.com/xueyi-2021/STEP_Week2/blob/master/homework1.png)

誤差はあるが、フィッティングの結果かなり微妙......（計算量はO(N^3)だけど…なぜだろう…)

<br>

<br>

### 宿題2

> 木構造を使えばO(log N)、ハッシュテーブルを使えばほぼO(1)で検索・追加・削除を実現することができて、これだけ見ればハッシュテーブルのほうがはるかに優れているように見える。ところが、現実の大規模なデータベースでは、ハッシュテーブルではなく木構造が使われることが多い。その理由を考えよ。

- ハッシュテーブルの計算量O(log N)はそんなに大きくないから実際に高速で検索、削除や追加などもできる
  - 例えば、10億のデータ量に対してlog Nは30くらいだけ、O(1)と比べてそんなに大きくなっていない

- ハッシュテーブルの空間計算量が大きい
- ハッシュテーブルの中でデータがバラバラので、管理しにくい。一方で、木構造の中でデータが整列されて一定の順序が保たれているので、例えばアルファベット順で前半の要素を取り出したいとき、木構造がかなり便利。

<br>

<br>

### 宿題3 & 宿題4

> キャッシュの管理をほぼO(1)で実現できるデータ構造を考えよ

~~（宿題3を「コードを書け」と勘違いして普通にコードを書いちゃった…書き終わった後宿題4にサンプルコードがあることに気づいた…）~~

#### 方針1

- 最初思い浮かべるのがキューみないに、新しい要素を一番後ろに追加して、長さが上限(N)を超えるとき一番前の要素を取り出すという構造。
  - 一番前の要素つまりアクセス順で一番古いウェブページで、取り出すという操作はキャッシュの中から捨てるという意味。
  - キューでは検索という機能が実装されていないので、要素を検索する機能を追加して、検索できるキューという構造を作りたい。
- 計算量について：listのin操作の計算量がO(n)だが、dictとsetのin操作の計算量はO(1)。1つのlistでアクセス順でウェブページを記録して、もう1つのdict(or set)でキャッシュに入れたページを記録する。これによって、O(1)で検索することができる。
  - もし新しくアクセスしたページが出現してない場合、一番前(古い)のページを捨ててこのページを一番後ろに追加する。
  - もしある場合、このページを一番後ろに移動すると思ってるけど、移動という操作ができないようで、この要素を取り出して一番後ろに追加するという2つの操作に分かれる。
  - listの中で指定位置の要素を取り出すの計算量はO(n)で、目標はほぼO(1)なので、この方法がちょっと間違ってると思う。けど、これをとりあえず実装してみた。
- ここでの実装はWebpageの名前だけ記録されるが\<Webpageの名前>と\<URL>でハッシュテーブルでO(1)で見つけるので実装したいなら普通にできると思う。

#### データ構造（擬似コード(ほぼコード)）-> queue_modified.py

```python
class cache:
   def __init__(self, N):    #Nはキャッシュの容量
      self.list_data = []          #アクセス順でキャッシュを記録
      self.set_data = set()     #O(1)で検索できるためにキャッシュを記録
      self.len = N
   def access_page(self, page):     #新しいページをアクセスする時
      if キャッシュにこのpageがない:
         キャッシュの一番後ろに追加(list.append, set.add)   #O(1)
         if キャッシュ内のページ数が上限を超える:
            一番前のpageを削除(list.pop(0), set.remove())  #O(n)
      else キャッシュにこのpageがある:
         このpageを削除(list.remove(page))    #O(n)
         一番後ろに追加(list.append)           #O(1)
   def all_pages(self):     #キャッシュをチェック
      return self.list_data
```

感想：こんな感じで実装したけど、得られたキャッシュの順序は古い→新しいで、たぶん求められるのは新しい→古いっていう順序だと思う。list.reverse()(O(n))でできるけど、たぶんこのデータ構造は違ってる.......

<br>

#### 方針2

- 連結リストのように前と後ろのページを記録すれば、順序が変換するたび前と後ろの値を更新すればいいと思うので、listの指定位置の要素を取り出す計算量O(n)と比べてO(1)でできるかもしれない。
- 初めてアクセスするページはheadとする。

- 新しいページをアクセスするとき、
  - もしcache内にないなら、headを削除してhead.nextは新しいheadになる（cacheが満ちてる時だけ）。新しいページは新しいtailになる。
  - もしcache内にあるなら、辞書でこのページを取り出して、新しいtailになる。

- cacheの中身を確認する時、
  - 新しい → 古い順で出力したいので、tailを始点としてheadまで探索。
- 今回は\<Webpageの名前>と\<URL>両方とも記録できるようにした。

#### データ構造（擬似コード） -> linkedlist_modified.py

```python
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
        if self.head is None:   #最初のページをアクセスする時 -> cacheは空の場合
            headとtail = new_page
        else:    #cacheは空ではない場合
            if new_pageはcacheに保存されていない場合  #辞書でO(1)
                if cache is full:
                    一番前のページを削除
                    tail = new_page
                    いろいろ連結する
                else cache is not full:
                    tail = new_page
                    いろいろ連結する
                    長さ += 1

            else new_pageはcacheに保存されている場合:
                saved_page = self.dict_data[url]   #O(1)で参照
                if new_pageは直前アクセスしたページ:
                    pass #交換する必要がない
                elif new_pageはhead:
                    交換と連結
                else new_pageは中間のページ:
                    交換と連結

    def all_pages(self):
        page = self.tail    
        list_data = []
        while文でheadまで探す
        return list_data
```

感想：連結するのがちょっと大変……連結リストのデバッグもちょっと大変……