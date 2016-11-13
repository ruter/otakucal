# otakucal
An otaku calendar RESTful API with management platform

Still developing...

---

# Usage

## Install managemant platform

Get extensions

```
pip install -r requirements.txt
```

Run the app to dev

```
python run.py
```

## API

```
http://api.sundaystart.net/otakucal/v1.0/entries
```

return

```
{"result": {"bad": ["游场", "暴饮暴食", "拉仇恨", "行走"], "good": ["睡觉", "面基", "看番", "吃饭", "购物", "看电影", "旅行", "保暖"]}}
```

```
http://api.sundaystart.net/otakucal/v1.0/hb_entries
```

return

```
{"result": {"hobby_entries": {"bad": ["看番", "看番", "游场", "露出"], "good": ["睡觉", "吃饭", "购物", "看电影", "运动", "旅行", "秀恩爱", "跑步"]}}}
```

```
http://api.sundaystart.net/otakucal/v1.0/hb_entries?hobby=%E6%90%9E%E5%9F%BA&hobby=COS&lucky=true
```

return

```
{"result": {"hobby_entries": {"bad": ["Coding", "看电影", "购物", "看电视"], "good": ["看番", "面基", "睡觉", "面基", "吃饭", "跑步"]}, "lucky_val": "100%"}}
```

```
http://api.sundaystart.net/otakucal/v1.0/hobbies
```

return

```
{"result": {"hobbies": ["搞基", "看番", "COS", "读书", "画画", "编程", "唱歌"]}}
```