# -*- coding:utf-8 -*-
"""
  Author  : 'longguangbin'
  Contact : lgb453476610@163.com
  Date    : 2018/10/4
  Usage   :
"""

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.clock import Clock
from kivy.event import EventDispatcher


class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)


# schedule 的基本介绍
def annotation_schedule():
    # ====================================
    # schedule interval 事件
    def my_callback(dt):
        print 'My callback is called', dt

    # 每隔一段时间调用一次该函数
    event = Clock.schedule_interval(my_callback, 1 / 30.)
    # 取消事件的方法
    event.cancel()
    Clock.unschedule(event)
    # 当函数返回 False 的时候，也会自动停止
    count = 0

    def my_callback(dt):
        global count
        count += 1
        if count == 10:
            print 'Last call of my callback, bye bye !'
            return False
        print 'My callback is called'

    Clock.schedule_interval(my_callback, 1 / 30.)

    # ====================================
    # schedule one-time 事件
    def my_callback(dt):
        print 'My callback is called !'

    Clock.schedule_once(my_callback, 1)  # 第2个参数是下次执行参数
    # >0，为等待执行时间(s)；=0，下次frame执行；-1，下次frame前执行（最常用）

    # ====================================
    # trigger 事件
    trigger = Clock.create_trigger(my_callback)
    # later
    trigger()

    # Page - 76


# widgets 的基本介绍
def annotation_widgets():
    # 默认有 2 种事件：1、属性事件：widget 改变位置、大小等，事件触发；2、组件定义事件：button 触发的事件
    # 这个例子不是很明白，跟直接调用 on_test 有什么区别
    class MyEventDispatcher(EventDispatcher):
        def __init__(self, **kwargs):
            self.register_event_type('on_test')
            super(MyEventDispatcher, self).__init__(**kwargs)

        def do_something(self, value):
            # when do_something is called, the 'on_test' event will be
            # dispatched with the value
            self.dispatch('on_test', value)

        def on_test(self, *args):
            print "I am dispatched", args

    # kivy.event.EventDispatcher.bind()
    # ====================================
    # 属性
    pass


class MyApp(App):
    def build(self):
        # return Label(text='Hello world!')
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()
