import weakref


class A:

  def __del__(self):
    print('(Deleting)')


d = weakref.WeakValueDictionary()
d['a'] = A()
print(list(d.keys()))
