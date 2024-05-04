import os
import yaml
from mirai import *

from pkg.plugin.context import register, handler, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
from pkg.command import entities
from pkg.command.operator import CommandOperator, operator_class
import typing

from plugins.miHoYoVoice.pkg.generate_voice import generate_audio

# 读取yaml配置文件
with open(os.path.join(os.path.dirname(__file__), 'config/config.yml'), 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

ifVoice = config['voice_switch']
character = config['character']


# 增加指令
@operator_class(name="语音合成", help="原神/星铁语音合成开关 开启/关闭/状态/角色列表/角色切换", privilege=1)
class SwitchVoicePlugin(CommandOperator):

    # 控制语音合成的开关
    async def execute(self, context: entities.ExecuteContext) -> typing.AsyncGenerator[entities.CommandReturn, None]:
        global ifVoice
        global character

        if context.crt_params[0] == "开启":
            self.ap.logger.info("启动语音合成")
            ifVoice = True
            yield entities.CommandReturn(text="启动语音合成")

        elif context.crt_params[0] == "关闭":
            self.ap.logger.info("关闭语音合成")
            ifVoice = False
            yield entities.CommandReturn(text="关闭语音合成")

        elif context.crt_params[0] == "状态":
            if ifVoice:
                yield entities.CommandReturn(text="语音合成状态:已开启"+f"，当前角色为{character}")
            else:
                yield entities.CommandReturn(text="语音合成状态:已关闭")

        elif context.crt_params[0] == "角色列表":
            # 读取角色列表.yaml
            with open(os.path.join(os.path.dirname(__file__), 'config/角色列表.yaml'), 'r', encoding='UTF-8') as file:
                character_list = yaml.load(file, Loader=yaml.FullLoader)
            reply = "角色列表：\n"
            for ch in character_list:
                reply += ch['name'] + "\n"
            yield entities.CommandReturn(text=reply.strip())

        elif context.crt_params[0] == "角色切换":
            # 读取角色列表.yaml
            with open(os.path.join(os.path.dirname(__file__), 'config/角色列表.yaml'), 'r', encoding='UTF-8') as file:
                character_list = yaml.load(file, Loader=yaml.FullLoader)
            for ch in character_list:
                if ch['name'] == context.crt_params[1]:
                    character = ch['name']
                    self.ap.logger.info(f"切换语音合成角色为{character}")
                    yield entities.CommandReturn(text=f"切换语音合成角色为{character}")
                    break
            else:
                yield entities.CommandReturn(text="未找到该角色")
        elif context.crt_params[0] == "帮助":
            yield entities.CommandReturn(text="语音合成插件支持的指令有：\n"
                                              "!语音合成 开启\n"
                                              "!语音合成 关闭\n"
                                              "!语音合成 状态\n"
                                              "!语音合成 角色列表\n"
                                              "!语音合成 角色切换 <角色名>\n"
                                              "!语音合成 帮助\n")

        else:
            yield entities.CommandReturn(error="无效指令，请输入\"!语音合成 帮助\"查看帮助")


# 注册插件
@register(name="miHoYoVoice", description="一个生成原神/星铁语音的插件", version="1.0", author="the-lazy-me")
class miHoYoVoicePlugin(BasePlugin):
    # 插件加载时触发
    def __init__(self, host: APIHost):
        pass

    # 当消息回复时触发
    @handler(NormalMessageResponded)
    async def text_to_voice(self, ctx: EventContext):
        global ifVoice
        global character
        # 如果语音开关开启
        if ifVoice:
            # 获取回复内容
            res_text = ctx.event.response_text
            # 读取角色列表.yaml
            with open(os.path.join(os.path.dirname(__file__), 'config/角色列表.yaml'), 'r', encoding='UTF-8') as file:
                character_list = yaml.load(file, Loader=yaml.FullLoader)
            # 获取角色id
            character_id = None
            for character_item in character_list:
                if character_item['name'] == character:
                    character_id = character_item['id']
                    break

            self.ap.logger.info(f"使用角色“{character}”生成回复语音，内容为：{res_text}")
            # 生成语音
            result = generate_audio(res_text, character_id)

            if result:
                # 回复语音消息
                ctx.add_return("reply", [Voice(path=str(result))])

                # 删除生成的silk语音文件
                os.remove(result)

        # 插件加载时触发

    def __init__(self, host: APIHost):
        pass
