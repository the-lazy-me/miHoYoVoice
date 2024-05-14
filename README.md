# miHoYoVoice插件使用教程

> 很高兴，[QChatGPT](https://github.com/RockChinQ/QChatGPT)开始了全新的3.x版本，带给开发和用户更好的体验，这应该是[QChatGPT](https://github.com/RockChinQ/QChatGPT) 3.x版本的第一个语音插件，由于原神和星铁的受众广泛，所以我开发了这个插件
>
> 但是我没学过python，代码大量依赖于AI生成，难免有不合理不正确之处，反正代码和人有一个能跑就行😋



## 介绍

本插件调用了[TTS-Online原神免费文本转语音](https://www.ttson.cn/?source=thelazy)的接口，用于将QChatGPT返回的内容转换为原神/星铁角色语音

特点：速度快，低价，效果好

## 使用

### 下载

克隆此项目，放到plugins的文件夹下

```bash
git clone https://github.com/the-lazy-me/miHoYoVoice.git
```

或下载源码压缩包，解压后放到plugins的文件夹下

打开GenshinVoice文件夹，命令行执行

```bash
pip install -r requirements.txt
```

速度太慢可以执行

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
```

### token获取

打开此页面[https://www.ttson.cn/](https://www.ttson.cn/?source=thelazy)

点击升级专业版

付款后，会给出一个链接（**只展示一次，相当重要，记清楚，不然钱就白花了！！！**）

这个链接形如`https://acgn.ttson.cn/?token=一串英文数字字符`

这个`token=`后面的英文数字字符就是获取到的token，复制备用
**是等于号后面的！！！不是那一串网址！！！长眼睛看清楚！！！**

### 配置

打开[miHoYoVoice](https://github.com/the-lazy-me/miHoYoVoice)的config文件夹下的`config.yaml`，内容如下所示

```yaml
# 默认角色，可在对话中指定角色，不指定则使用默认角色
character: "派蒙"
# 是否默认开启语音功能，默认为False，即不开启，True为默认开启，看你喜好
voice_switch: True

# token，这个是必须的，不然无法使用，可以配置多个token，获取方式请看文档
token:
  - "填入你的token 1"
```

重点关注第三个，token，在汉字提示处填入刚刚复制的token，保存即可

### 指令

对话中，发送

- `!语音合成 开启`
- `!语音合成 关闭`
- `!语音合成 状态`
- `!语音合成 角色列表`
- `!语音合成 角色切换 <角色名>`  举个例子：!语音合成 角色切换 纳西妲
- `!语音合成 帮助`
