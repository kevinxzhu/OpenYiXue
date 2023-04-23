from fastapi import APIRouter, Path, HTTPException, status
from ziweipan.model import StarGroup, Star, Palace, ZiweiPan

star_groups = [
    StarGroup(star_group_id=0, group='开创型性格', advantage='价值观是行动，非常重视机会、效率，比较喜欢挑战，擅长辩论，小时候会比较叛逆，长大后通常是领导人物', disadvantage='1、因为太有自信，导致骄傲自满而失败; 2、因为太过冒险，而导致准备不足，评估不周而失败; 3、因为太过压迫，导致人际关系失败; 4、因为太有冲劲，导致别人跟不上你而失败', improvement='要修炼定力，多忍耐，多控制自己的情绪，确认时机成熟再出击'),
    StarGroup(star_group_id=1, group='领导型性格', advantage='理性，喜欢被看成客观而合理的人，做事有条理，擅长建立组织和程序，做事踏实', disadvantage='1、太过固执，刚愎自用而导致失败; 2、太过保守，常常因为保守错过大好的机会; 3、太爱听人阿谀奉承，没有兼听则明，而导致失败; 4、吝啬，不愿意授权而导致自己特别辛苦', improvement='性格上保持弹性，兼听则明'),
    StarGroup(star_group_id=2, group='前瞻型性格', advantage='先知卓越，希望被大家重视，被大家需要，喜欢运筹帷幄，帮人出谋划策，适合从事自媒体，或者新闻媒体的工作', disadvantage='1、太过热情，太过爱管闲事，介入太深而被人讨厌; 2、太容易发现事情的关键，就会导致太多话，容易言多必失得罪人; 3、行动力不足，很难坚持，是思想上的巨人，行动上的矮子', improvement='加强落地执行的能力，避免自己刷存在感，避免多管闲事'),
    StarGroup(star_group_id=3, group='幕僚型性格', advantage='观念和谐，喜欢被看成是一个被人欣赏，被人欢迎的人，非常重视别人对自己的看法，做事漫无目标，前后不一致，擅长变通，实验精神很好，没有主见，事事迁就，个性软弱，容易妥协', disadvantage='1、因为没有原则，事事妥协，导致失败; 2、过于软弱，没有主见，无法坚持，缺乏了韧性和耐力，导致失败; 3、容易讨好他人，被当做阿谀奉承的人，导致不被人信任，而失败; 4、擅长维护调节，控制各种状态，而导致机关算尽而失败', improvement='培养责任心，勇于承担责任，适度的去面对必要的冲突，讲求原则，实话实说，就事论事'),
    StarGroup(star_group_id=4, group='', advantage='', disadvantage='', improvement=''),
]

stars = [
    Star(star_id=0, star='贪狼', type='main', star_group_id=0, feature='1、桃花特别旺; 2、擅长交际，人缘好; 3、娱乐嗜好多'),
    Star(star_id=1, star='七杀', type='main', star_group_id=0, feature='1、毅力强; 2、眼神有力; 3、目标感极重，不择手段，重视结果'), 
    Star(star_id=2, star='廉贞', type='main', star_group_id=0, feature='1、体面，重视自己在别人眼里的样子; 2、敢爱敢恨; 3、对自己要求比较高，高傲'), 
    Star(star_id=3, star='破军', type='main', star_group_id=0, feature='1、创意性，一般从事艺术、设计等工作会如鱼得水; 2、性格比较叛逆，是打破规则的人、自我主义; 3、喜新厌旧'), 
    Star(star_id=4, star='紫微', type='main', star_group_id=1, feature='1、领导欲望强; 2、喜怒无常、多疑; 3、爱面子'),
    Star(star_id=5, star='天府', type='main', star_group_id=1, feature='1、管理能力强; 2、财星，擅长理财，会回避风险; 3、谨慎保守'),
    Star(star_id=6, star='武曲', type='main', star_group_id=1, feature='1、事业心重，执行力强; 2、性格刚硬，会给人一种不近人情的感觉; 3、财星，开创生财'),
    Star(star_id=7, star='天相', type='main', star_group_id=1, feature='1、善沟通; 2、二把手，辅助; 3、人缘好'),
    Star(star_id=8, star='太阳', type='main', star_group_id=2, feature='1、追求成就感; 2、阳光热情，会照顾别人; 3、无私'),
    Star(star_id=9, star='巨门', type='main', star_group_id=2, feature='1、心思深沉，擅长隐藏，不太会表达自己; 2、观察力，洞察力强; 3、口舌善辩'),
    Star(star_id=10, star='天机', type='main', star_group_id=2, feature='1、有谋略、会思考，擅长出谋划策，点子多，逻辑思维也高; 2、适应能力太快，容易善变; 3、专业能力强'),
    Star(star_id=11, star='天梁', type='main', star_group_id=3, feature='1、保守老成，照顾他人，口碑好; 2、重视名声，顾忌他人对自己的感受，老好人; 3、谨慎多虑'),
    Star(star_id=12, star='天同', type='main', star_group_id=3, feature='1、心胸宽大、忘性大; 2、容易被感动，易落泪; 3、懂享受'),
    Star(star_id=13, star='太阴', type='main', star_group_id=3, feature='1、爱美，重视外表; 2、比较被动; 3、财星，善经营、对钱财敏感，对数字敏锐'),
    Star(star_id=14, star='文昌', type='luck', star_group_id=4, feature=''),
    Star(star_id=15, star='文曲', type='luck', star_group_id=4, feature=''),
    Star(star_id=16, star='天魁', type='luck', star_group_id=4, feature=''),
    Star(star_id=17, star='天钺', type='luck', star_group_id=4, feature=''),
    Star(star_id=18, star='左辅', type='luck', star_group_id=4, feature=''),
    Star(star_id=19, star='右弼', type='luck', star_group_id=4, feature=''),
    Star(star_id=20, star='红鸾', type='luck', star_group_id=4, feature=''),
    Star(star_id=21, star='天喜', type='luck', star_group_id=4, feature=''),
    Star(star_id=22, star='禄', type='luck', star_group_id=4, feature=''),
    Star(star_id=23, star='天马', type='luck', star_group_id=4, feature=''),
    Star(star_id=24, star='禄存', type='luck', star_group_id=4, feature=''),
    Star(star_id=25, star='权', type='luck', star_group_id=4, feature=''),
    Star(star_id=26, star='科', type='luck', star_group_id=4, feature=''),
    Star(star_id=27, star='火星', type='bad', star_group_id=4, feature=''),
    Star(star_id=28, star='铃星', type='bad', star_group_id=4, feature=''),
    Star(star_id=29, star='擎羊', type='bad', star_group_id=4, feature=''),
    Star(star_id=30, star='陀罗', type='bad', star_group_id=4, feature=''),
    Star(star_id=31, star='地空', type='bad', star_group_id=4, feature=''),
    Star(star_id=32, star='地劫', type='bad', star_group_id=4, feature=''),
    Star(star_id=33, star='天姚', type='bad', star_group_id=4, feature=''),
    Star(star_id=34, star='天刑', type='bad', star_group_id=4, feature=''),
    Star(star_id=35, star='忌', type='bad', star_group_id=4, feature='忌是代表失去、空缺、固执、亏欠。忌在哪个宫，就代表和这个宫位无缘。'),
]

palaces = [
    Palace(palace_id=0, name='命宫', ji_desc='1、一生坎坷不顺，尤其是少年的时候过不顺利; 2、个性固执己见，不听人劝; 3、易犯小人，灾厄多，容易破财。忌通常和无缘有关，容易有不顺，有遗憾。但是上面所有忌引发的是是非非，完全都是由自己的心境、念头所造成的，物有阴阳，事有好坏，所有事情的吉凶祸福往往在于一个人的一念之间。', ji_action='化解方法（关键在于转念）： 1、避免由于过度的关注自己，而导致自己固执己见; 2、不宜出风头，低调做人做事; 3、不宜冲动创业，只宜受雇于人'),
    Palace(palace_id=1, name='兄弟', ji_desc='', ji_action=''),
    Palace(palace_id=2, name='夫妻', ji_desc='', ji_action=''),
    Palace(palace_id=3, name='子女', ji_desc='', ji_action=''),
    Palace(palace_id=4, name='财帛', ji_desc='', ji_action=''),
    Palace(palace_id=5, name='疾厄', ji_desc='', ji_action=''),
    Palace(palace_id=6, name='迁移', ji_desc='', ji_action=''),
    Palace(palace_id=7, name='仆役', ji_desc='', ji_action=''),
    Palace(palace_id=8, name='官禄', ji_desc='', ji_action=''),
    Palace(palace_id=9, name='田宅', ji_desc='', ji_action=''),
    Palace(palace_id=10, name='福德', ji_desc='', ji_action=''),
    Palace(palace_id=11, name='父母', ji_desc='', ji_action=''),
]

ziwei_pans = [
]

star_groups_count = 0
star_ = 0
ziwei_pan_count = 0

def find_all_star_groups() -> list[StarGroup]:
    return star_groups


def find_star_group(star_group_id: int) -> StarGroup:
    for group in star_groups:
        print(group.star_group_id)
        if group.star_group_id == star_group_id:
            return group
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="StarGroup with supplied ID doesn't exist",
    )


def save_star_group(group: StarGroup):
    global star_groups_count
    star_groups_count = star_groups_count + 1
    group.star_group_id = star_groups_count
    star_groups.append(group)
    

def find_all_stars() -> list[Star]:
    return stars


def find_star(star_id: int) -> Star:
    for star in stars:
        if star.star_id == star_id:
            return star
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Star with supplied ID doesn't exist",
    )


def save_ziwei_pan(pan: ZiweiPan, palace_map: dict) -> dict:
    global ziwei_pan_count 
    ziwei_pan_count = ziwei_pan_count + 1
    pan.ziwei_pan_id = ziwei_pan_count

    ziwei_pans.append(pan)
    return {'ziwei_pan_id': ziwei_pan_count }


def get_all_ziwei_pans() -> list[ZiweiPan]:
    return ziwei_pans


def find_ziwei_pan(ziwei_pan_id: int) -> ZiweiPan:
    for pan in ziwei_pans:
        if pan.ziwei_pan_id == ziwei_pan_id:
            return pan
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Star with supplied ID doesn't exist",
    )

def find_palace(palace_id: int) -> Palace:
    for palace in palaces:
        if palace.palace_id == palace_id:
            return palace
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Palace with supplied ID doesn't exist",
    )