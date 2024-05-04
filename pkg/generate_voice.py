import requests
import json
import os
import yaml

from plugins.miHoYoVoice.pkg.audio_converter import convert_to_silk

# 设置基础路径为当前文件夹的上一级
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 读取yaml文件
with open(os.path.join(base_path, 'config/config.yml'), 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# token = config['token'][0]

if len(config['token']) == 0:
    print("请填写token")
    exit(1)
else:
    token_list = config['token']

print(token_list)

def get_character_list():
    global base_path

    url = "https://api.ttson.cn:50602/flashsummary/voices?language=zh-CN&tag_id=1"

    payload = ""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_json = response.json()

    # 清空角色列表
    with open(os.path.join(base_path, 'config/角色列表.yaml'), 'w', encoding='UTF-8') as file:
        file.write('')

    # 遍历所有角色
    for character in response_json['data']:
        if character['tags'][0]['tag_name'] == '新原神星铁' or character['tags'][1]['tag_name'] == '新原神星铁' or \
                character['tags'][2]['tag_name'] == '新原神星铁':
            content = f"- id: {character['id']}\n  name: {character['voice_name']}\n  tags: {character['tags'][0]['tag_name']}"

            with open(os.path.join(base_path, 'config/角色列表.yaml'), 'a', encoding='UTF-8') as file:
                file.write(content + '\n')


def get_audio_url(text: str, voice_id: str):
    global token_list

    # 如果有多个token，轮询使用
    if len(token_list) > 1:
        token = token_list.pop(0)
        token_list.append(token)
    else:
        token = token_list[0]

    url = "https://u95167-bd74-2aef8085.westx.seetacloud.com:8443/flashsummary/tts?token=" + token

    language = "ZH"
    auto_translate = 0

    # 检测text是否包含英文
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            language = "auto"
            break

    payload = json.dumps({
        "voice_id": voice_id,
        "text": text,
        "format": "mp3",
        "to_lang": language,
        "auto_translate": auto_translate,
        "voice_speed": "0%",
        "speed_factor": 1,
        "rate": "1.0",
        "client_ip": "ACGN",
        "emotion": 1
    })

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = response.json()

    # print(response_json)

    return 'https://api.ttson.cn:50602/flashsummary/retrieveFileData?stream=True&token=' + token + '&voice_audio_path=' + \
        response_json['voice_path']


def download_audio(url, save_path):
    if url == "":
        print("Empty url")
        return False
    try:
        audio_content = requests.get(url)
        if audio_content.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(audio_content.content)
            return True
    except Exception as e:
        print(f"Error downloading audio: {str(e)}")
    return False


def generate_audio(text, character_id):
    global base_path

    audio_url = get_audio_url(text, character_id)
    # print(audio_url)

    if audio_url:
        # 设置基础路径为当前文件夹的上一级
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        # 在基础路径下创建audio_temp文件夹
        base_path = os.path.join(base_path, "audio_temp")
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        # 提取文件名，.wav字符前的八个字符为文件名
        file_name = audio_url.split('/')[-1].split('.')[0][:8]
        # 拼接文件路径
        save_path = os.path.join(base_path, file_name + '.mp3')

        if download_audio(audio_url, save_path):
            # 转换为silk格式
            silk_path = convert_to_silk(save_path, base_path)

            # 删除wav文件
            # os.remove(save_path)
            return silk_path
    return None


if __name__ == "__main__":
    # get_character_list()

    # 测试生成语音
    text = "你好"
    character = "430"
    generate_audio(text, character)
