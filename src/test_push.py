__author__ = 'wyunchi'

#-*-coding:utf-8-*-

import instapush
app = instapush.App(appid='54d1aeb8a4c48ad275ff7ea5', secret='c3562dd35abc8083a92dfbb31048665c')
result = app.notify(event_name='First Blood!', trackers={ 'message': '430 kill minimi get first blood!'})
print result