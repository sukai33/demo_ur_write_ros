#!/usr/bin/env python
# coding:utf-8
import socket
import threading
import json
import queue
import time


class UR:
    def __init__(self, ip="127.0.0.1", port=13557):
        self._ip = ip
        self._port = port

        # 连接状态
        self._connected = False
        # 连接状态回调
        self._connected_callback = None
        # socket client
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._queue = queue.Queue()

    def _set_connected(self, connected):
        self._connected = connected
        if self._connected_callback is not None:
            self._connected_callback(self._connected)

    def _do_connect(self, callback=None):
        try:
            # socket client
            self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._client.connect((self._ip, self._port))
            self._set_connected(True)
            if callback is not None:
                callback()

            recv_thread = threading.Thread(target=lambda: self._do_recv())
            recv_thread.start()

            send_thread = threading.Thread(target=lambda: self._do_send())
            send_thread.start()
        except Exception as e:
            print(e)

    def _do_recv(self):
        try:
            while self._connected:
                recv = self._client.recv(1024)
                if len(recv) == 0:
                    # 断开链接了
                    self.disconnect()
                    break
                print(recv.decode("utf-8"))
        except Exception as e:
            # 断开链接了
            self.disconnect()

    def _do_send(self):
        while self._connected:
            try:
                data = self._queue.get()
                if data is None:
                    self._do_disconnect()
                    continue
                self._client.send("{}{}".format("#", data).encode("utf-8"))
            except Exception as e:
                print(e)
                pass

    def _do_disconnect(self):
        if self._connected:
            threading.Thread(target=lambda: self._do_stop()).start()
            self._client.close()
            self._set_connected(False)

    def _do_stop(self):
        time.sleep(3)
        self._queue.put(None)

    def connect(self, callback=None):
        if self._connected:
            return
        thread = threading.Thread(target=lambda: self._do_connect(callback))
        thread.start()

    def disconnect(self):
        time.sleep(0.2)
        self._queue.put(None)

    def is_connected(self):
        return self._connected

    def on_connected_change(self, callback):
        """
        连接状态监听
        :param callback: 回调，包含一个参数，当前连接状态
        :return:
        """
        self._connected_callback = callback

    def move_j(self, joints, a=1.4, v=1.05, t=0, r=0, degrees=True):
        if not isinstance(joints, list) and not isinstance(joints, tuple):
            raise Exception("传入的数据类型不是列表或元组")
        data = {}
        data["type"] = 1
        data["data"] = {
            'acc': a,
            'vel': v,
            'time': t,
            'radius': r,
            'degrees': degrees,
            'joints': []
        }
        for joint in joints:
            data["data"]["joints"].append(joint)
        self._queue.put(json.dumps(data))

    def move_l(self, pose, a=1.2, v=0.25, r=0, degrees=True):
        if not isinstance(pose, list) and not isinstance(pose, tuple):
            raise Exception("传入的数据类型不是列表或元组")
        data = {}
        data["type"] = 2
        data["data"] = {
            "acc": a,
            "vel": v,
            "radius": r,
            "degrees": degrees,
            "pose": []
        }
        for p in pose:
            data["data"]["pose"].append(p)
        self._queue.put(json.dumps(data))

    def move_c(self, via_pose, to_pose, a=1.2, v=0.25, r=0, degrees=True):
        if not isinstance(via_pose, list) and not isinstance(via_pose, tuple):
            raise Exception("传入的数据类型不是列表或元组")
        if not isinstance(to_pose, list) and not isinstance(to_pose, tuple):
            raise Exception("传入的数据类型不是列表或元组")
        data = {}
        data["type"] = 3
        data["data"] = {
            "acc": a,
            "vel": v,
            "radius": r,
            "degrees": degrees,
            "via": [],
            "to": []
        }
        for p in via_pose:
            data["data"]["via"].append(p)
        for p in to_pose:
            data["data"]["to"].append(p)
        self._queue.put(json.dumps(data))

    def move_p(self, pose, a=1.2, v=0.25, r=0, degrees=True):
        if not isinstance(pose, list) and not isinstance(pose, tuple):
            raise Exception("传入的数据类型不是列表或元组")
        data = {}
        data["type"] = 4
        data["data"] = {
            "acc": a,
            "vel": v,
            "radius": r,
            "degrees": degrees,
            "pose": []
        }
        for p in pose:
            data["data"]["pose"].append(p)
        self._queue.put(json.dumps(data).encode("utf-8"))

    def move_t(self, pose, a=1.4, v=1.05, t=0, r=0, degrees=True):
        if not isinstance(pose, list) and not isinstance(pose, tuple):
            raise Exception("传入的数据类型不是列表或元组")
        data = {}
        data["type"] = 6
        data["data"] = {
            "acc": a,
            "vel": v,
            "radius": r,
            "degrees": degrees,
            "pose": pose
        }
        self._queue.put(json.dumps(data))

    def show_point(self, point, size=0.05, color=(0, 0, 255, 255)):
        if not isinstance(point, list) and not isinstance(point, tuple):
            raise Exception("传入的数据类型不是列表或元组")
        data = {
            "type": 5,
            "data": {
                "size": size,
                "point": point,
                "color": color
            }
        }
        self._queue.put(json.dumps(data))

    def clear_points(self):
        data = {
            "type": 7
        }
        self._queue.put(json.dumps(data))

    def enable_trail(self):
        data = {
            "type": 8,
            "enable": True
        }
        self._queue.put(json.dumps(data))

    def disable_trail(self):
        data = {
            "type": 8,
            "enable": False
        }
        self._queue.put(json.dumps(data))