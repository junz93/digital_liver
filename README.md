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
