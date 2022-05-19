# 关于attr库的学习

## 一、为什么要学习attr库？

`attr`库是为了提高python的OOP开发效率而开发的！为程序员编写大型项目极大的提高开发效率！

## 二、与传统创建类对比

> 安装: pip install attrs

- 传统

  - ```python
    # -*- coding: utf-8 -*-
    class Person(object):
        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age
    
        def __repr__(self) -> str:
            '''打印美化'''
            return self.__str__()
    
        def __str__(self) -> str:
            return f"<Object Person => {self.name}, {self.age}>"
    ```

- `attr`方式

  - ```python
    # -*- coding: utf-8 -*-
    from attr import attrs
    from attr import attrib
    
    @attrs
    class Person(object):
        name = attrib(type=str)
        age = attrib(type=int)
    
    if __name__ == "__main__":
        # result => Person(name='珂珂', age=18)
        print(Person("珂珂", 18))
    ```

- 一对比是不是感觉比传统更加简化，这样我们在开发过程中就可以极大提高效率！

## 三、方法介绍

> 参考链接：[提升类编写效率的库——attr - 简书 (jianshu.com)](https://www.jianshu.com/p/2140b519028d)

#### 3.1 `attrs`类装饰器介绍

- ```python
  ''' 只解释部分属性
  attrs(maybe_cls=None, these=None, repr_ns=None, 
        repr=None, cmp=None, hash=None, init=None, 
        slots=False, frozen=False, weakref_slot=True, 
        str=False, auto_attribs=False, kw_only=False, 
        cache_hash=False, auto_exc=False, eq=None, 
        order=None, auto_detect=False, collect_by_mro=False, 
        getstate_setstate=None, on_setattr=None, 
        field_transformer=None, match_args=True
  )
  '''
  # ---
  ''' these
  这个属性是用来定义类属性的，如果*these*不是`None'，`attrs'将*不*搜索类体中的的属性，也不会从其中删除任何属性。这个属性用的较少; type these: `dict` of `str` to `attr.i。
  '''
  # ---
  ''' auto_detect
  不设置*init*, *repr*, *eq*, *order*, 和 *hash* 参数. 假定值为*True*, 当你自己在类中实现init或其他，那么attrs就会推断出init=False其他对应值,而不会自己进行创建其相关方法。向*init*、*repr*、*eq*、*order*、*cmp*或*hash*传递`True'或`False'，将覆盖*auto_detect*的决定。
  '''
  # ---
  ''' init
  此属性表示帮你自动创建构造函数，且关于继承方面，也会自动调用`super().__init__()'；默认启动。关于形参设置如下：
  案例:
      @attrs
      class Person(object):
          name = attrib(type=str)
          age = attrib(type=int)
  '''
  # ---
  ''' slots
  相当于帮你实现__slots__属性，好处就是节约你的内存空间，参考链接：https://zhuanlan.zhihu.com/p/101109893
  '''
  # ---
  ''' weakref_slot
  让对象支持弱引用；弱引用参考链接：https://blog.csdn.net/qq_39173907/article/details/79921590
  '''
  # ---
  ''' frozen
  让修饰类的实例化对象其中属性不可修改。原理就是attr帮你实现了一个__setattr__方法，所以不可自己再进行实现。
  '''、
  # ---
  ''' cache_hash
  确保对象的哈希代码只被计算一次，并存储在对象上。
  '''
  # ---
  ''' auto_attrlib
  使用注释属性，这个比较有意思，和typing集合最佳！
  '''
  ```

#### 3.2 `attrib`方法介绍

- ```python
  #　Create a new attribute on a class.
  '''
  attrib(default=NOTHING, validator=None, repr=True, 
  	   cmp=None, hash=None, init=True, metadata=None, 
  	   type=None, converter=None, factory=None, 
  	   kw_only=False, eq=None, order=None, on_setattr=None)
  '''
  # ---
  ''' default 
  创建属性的提供默认值，可以是任何类型。
  '''
  # ---
  ''' validator
  在实例被初始化后，由 `attrs`生成的 `__init__` 方法调用的 `callable`。 他们接收初始化的实例，:func:`~attrs.Attribute`，和传递的值。
  (<class>, Attribute(...), value)
  '''
  # ---
  ''' type
  该属性的类型，注释作用。参考链接：https://peps.python.org/pep-0526/
  '''
  ```

   

