#問1. 名前を返す関数( return を含む)に、デコレータせよ。(デコレータの内容は自由に設定してよい)
#できてることも確認せよ
def deco(func):
    def inner_func(*args,**kwargs):
        result = []
        result.append("My name is")
        result.append(func(*args))
        result.append("Nice to meet you")
        return result
    return inner_func
@deco
def name(x):
    return str(x)
print(name("akkun"))