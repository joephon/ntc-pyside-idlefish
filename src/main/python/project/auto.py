import os
import time
import asyncio
import re
import cv2
import base64
import threading
import traceback
import uiautomator2 as u2
from adbutils import adb
from PySide2.QtGui import QPixmap, QImage, QFont
from PySide2.QtCore import Qt, Slot, Signal, QObject, QThread
from PySide2.QtWidgets import QMessageBox


class DeviceHub(QObject):
    seeked = Signal(list)
    called = Signal(dict)
    casted = Signal(dict)
    _instance_lock = threading.Lock()

    def __init__(self):
        super().__init__()
        self.adb = adb
        self.store = dict()
        self.hold = list()
        self.task_pool = dict()

    def __new__(cls, *args, **kwargs):
        if not hasattr(DeviceHub, "_instance"):
            with DeviceHub._instance_lock:
                if not hasattr(DeviceHub, "_instance"):
                    DeviceHub._instance = QObject.__new__(cls)
        return DeviceHub._instance

    def seek(self):
        try:
            self.hold = [i for i in adb.devices()]
            self.seeked.emit(self.hold)
            if not len(self.hold):
                return QMessageBox.information(self, '提示信息', '未发现设备',
                                               QMessageBox.Ok)
        except Exception as error:
            traceback.print_exc()
            print(error)

    def call(self, serial=None):
        try:
            self.store[serial] = u2.connect(serial)
            print(self.store[serial].wlan_ip + ':7912',
                  self.store[serial].address)
            self.called.emit({serial: self.store[serial]})
        except Exception as error:
            traceback.print_exc()
            print(error)

    def run(self, serial=None, form_data_dict=None):
        try:
            self.task_pool[serial] = TTask(d=self.store[serial],
                                           form_data_dict=form_data_dict)
            self.task_pool[serial].start()
            print(self.task_pool[serial])
            self.casted.emit({
                serial: self.store[serial],
                'task': self.task_pool[serial]
            })
        except Exception as error:
            traceback.print_exc()
            print('error', error)


class TTask(QThread):
    def __init__(self, form_data_dict=None, d=None):
        super().__init__()
        self.d = d
        self.form_data_dict = form_data_dict
        self.start_at = time.time()
        self.allow_failed_time = 5
        self.data_list = []
        self.data = dict()
        self.qty = 0

    def stop(self, reason=None):
        print('Mission Stopped as {}'.format(reason or 'Normal'))
        self.terminate()

    def run(self, steps=None):
        print('Invoke at {}'.format(self.start_at))
        steps = steps or [
            self.start_app, self.search_keyword, self.choose_ordered,
            self.loop_list, self.check_state
        ]

        for index, step in enumerate(steps):
            print('step for {}'.format(step.__name__))
            if not len(steps):
                self.stop('Finished')
                break
            else:
                try:
                    step()
                except Exception as error:
                    print('执行有误！', error, self.allow_failed_time)
                    traceback.print_exc()
                    if self.allow_failed_time > 0:
                        self.allow_failed_time -= 1
                        self.run(steps[index:])
                    else:
                        self.stop(error)
                        break

    def start_app(self):
        self.d.session('com.taobao.idlefish')
        self.d.xpath('@[text=^跳过广告$]').click_exists(5)
        self.d.xpath('@[text=^暂不升级$]').click_exists(5)
        self.d(resourceId='com.taobao.idlefish:id/left_btn').click_exists(5)

        self.d(resourceId='com.taobao.idlefish:id/search_bg_img_front'
               ).click_exists(3)
        self.d.xpath('//android.widget.EditText').click_exists(5)

    def search_keyword(self):
        # self.d(focused=True).set_text(self.form_data_dict['关键词'])
        self.d.send_keys(self.form_data_dict['关键词'])
        self.d.send_action('search')

    def choose_ordered(self):
        self.d(text='已折叠, 综合').click_exists(3)
        self.d(text='最新发布').click_exists(3)

    def loop_list(self):
        self.sleep(2)
        els = self.d(className='android.widget.ScrollView').child(
            className='android.view.View')

        for el in els:
            if not el or not el.get_text():
                continue
            text = el.get_text()
            text = text.replace('\n\r', '')
            if '发个求购' in text:
                print(1111, text)
                continue
            if '￥' not in text and '人想要' not in text or len(text) < 6:
                print(1111, text)
                continue
            self.el = el
            self.store_item_data()
            self.store_item_detail_data()
            self.d.press('back')
            self.sleep(0.3)
            print(self.data.get('detail'))
            if self.data not in self.data_list:
                self.data_list.append(self.data)
                self.qty += 1
                print('total:', len(self.data_list))

        self.d.swipe_ext('up', scale=0.6)
        if self.qty >= int(self.form_data_dict['休息数量']):
            self.qty = 0
            self.check_state()
        self.loop_list()

    def store_item_data(self):
        el = self.el
        text = el.get_text()

        line_text: [str] = text.split('\n')
        self.data = dict()
        self.data['text'] = text
        self.data['keyword'] = self.form_data_dict['关键词']
        self.data['location'] = line_text[-1:][0]
        self.data['price'] = line_text[len(line_text) -
                                       3] if len(line_text) >= 3 else '0'
        self.data['title'] = line_text[0]
        self.data['paid'] = line_text[len(line_text) - 2].replace(
            '人付款', '') if re.search('(人付款)$', line_text[len(line_text) -
                                                        2]) else '0'
        self.data['wanted'] = line_text[len(line_text) - 2].replace(
            '人想要', '') if re.search('(人想要)$', line_text[len(line_text) -
                                                        2]) else '0'

    def store_item_detail_data(self):
        self.el.click()
        self.sleep(2)
        wanted = self.d(text='我想要')
        if not wanted:
            self.d.press('back')

        save = self.d(text='收藏')
        if save:
            save.click()
            self.sleep(0.5)

        els = self.d(className='android.widget.ScrollView').child(
            className='android.view.View')
        detail = dict()

        for el in els:
            text = el.get_text()
            if '发布于' in text:
                detail['account'] = text.split('\n')[0]
                detail['recent'] = text
                detail['hold'] = text.split('\n')[1].split(' ')[0].replace(
                    ''.join(
                        re.compile('[^\d]').findall(
                            text.split('\n')[1].split(' ')[0])), '') or '1'
                detail['city'] = text.split('\n')[1].split(' ')[1].replace(
                    '发布于', '')

        self.data['detail'] = detail

    def check_state(self):
        if int(self.start_at) + int(self.form_data_dict['持续时间']) * 60 <= int(
                time.time()):
            print('finished work for {} minutes'.format(
                self.form_data_dict['持续时间']))
            self.d.toast.show(
                '按计划工作了{}分钟，准备结束'.format(self.form_data_dict['持续时间']), 5)
            self.stop()
        else:
            print('sleep for {} seconds'.format(self.form_data_dict['休息间隔']))
            self.count_down(int(self.form_data_dict['休息间隔']))
            # self.sleep(int(self.form_data_dict['休息间隔']) * 60)
            self.run()

    def count_down(self, s):
        self.d.toast.show('按计划休息{}秒'.format(str(s)))
        self.sleep(1)
        s -= 1
        if s > 0:
            self.count_down(s)