## 开发框架
接口开发主要使用了 Django 和 Django REST framework。

参考文档：
- Django: https://docs.djangoproject.com/zh-hans/4.2/
- Django REST framework: https://www.django-rest-framework.org/tutorial/1-serialization/

## 项目结构
本项目包含6个Django app，分别包含不同功能模块的接口：
- user：用户管理相关接口（注册、获取认证token、用户基本信息等）
- subscripton：会员相关接口（会员状态信息、会员支付等）
- verification：验证码相关接口（发送验证码、验证验证码等）
- payment：支付回调接口（用于接收来自于支付平台的异步通知等）
- material：直播素材材料相关接口（人设、文案、话术等）
- livestream：直播实时内容相关接口（直播音频推流等）

## 用户认证
接口的用户认证基于 request header 实现： `Authorization: Token <token-value>`（不使用 cookie 和 session）。具体流程参见下文章节“本地测试”

## 安装依赖包
```shell
pip install -r requirements.txt
```

**注意**: 因未知原因，部分依赖可能无法自动安装，需要手动安装
```shell
pip install djangorestframework==3.14.0
```

## 添加外部API授权配置
新建一个文件 `conf/auth.ini`，内容格式如下：
```ini
[alipay]
AppId = xxx
AppPublicKey = xxx
AppPrivateKey = xxx
AlipayPublicKey = xxx
AesEncryptionKey = xxx
SellerId = xxx

[alipay-sandbox]
AppId = xxx
AppPublicKey = xxx
AppPrivateKey = xxx
AlipayPublicKey = xxx
AesEncryptionKey = xxx
SellerId = xxx

[aliyun]
AccessKeyId = xxx
AccessKeySecret = xxx

[openai]
ApiKey = xxx

[serpapi]
ApiKey = xxx
```

**注意**: 支付宝官方开发工具生成的应用私钥 (AppPrivateKey) 为 PKCS8 格式，但该格式为支付宝 Java SDK 专用，Python SDK 只支持 PKCS1 格式私钥，因此需要使用开发工具对私钥进行转换后再使用

## 修改支付宝SDK代码
目前的支付宝SDK代码有bug，当加密 request 或解密 response 时会报错：
```python
TypeError: Object type <class 'str'> cannot be passed to C code
```

需要修改SDK内的下列文件：
- `alipay/aop/api/util/EncryptUtils.py`
    ```python
    def aes_encrypt_content(content, encrypt_key, charset):
        ...
        cryptor = AES.new(base64.b64decode(encrypt_key), AES.MODE_CBC, iv.encode('utf-8'))
        encrypted_content = cryptor.encrypt(padded_content.encode('utf-8'))
        ...
    

    def aes_decrypt_content(encrypted_content, encrypt_key, charset):
        ...
        cryptor = AES.new(base64.b64decode(encrypt_key), AES.MODE_CBC, iv.encode('utf-8'))
        ...
    ```

## 本地测试
通过以下命令在本地启动服务
```
# Debug（开发）模式
python manage.py runserver 8081

# Prod（生产）模式
DEBUG=0 python manage.py runserver 8081
```

如果使用 Postman 测试接口，可以直接导入本项目 `postman` 文件夹里的接口 collection 配置文件。Postman 中接口测试的基本流程如下：
1. 注册用户：调用 User/Register 接口
   - 注：注册需要填写验证码，可以通过调用 Verification/SendSms 接口发送到真实手机号
1. 获取用户认证token：调用 User/GetAuthToken 接口
1. 测试具体功能接口：调用时，request header 加上上一步获取的 token
    ```
    Authorization: Token <token-value>
    ```
    - 注：部分不需要用户认证的接口调用时无需包含 token（如发送验证码接口）