from fastapi import APIRouter, Path, HTTPException, status
from ziweipan.model import StarGroup, Star, Palace, ZiweiPan, PalacePanMap
from ziweipan.store import save_star_group, find_all_star_groups, find_star_group, find_all_stars, find_star, save_ziwei_pan, get_all_ziwei_pans, find_ziwei_pan, find_palace


def retrieve_all_star_groups() -> list[StarGroup]:
    return find_all_star_groups()


def retrieve_star_group(star_group_id: int) -> StarGroup:
    return find_star_group(star_group_id)


def create_star_group(group: StarGroup):
    save_star_group(group)
    

def retrieve_all_stars() -> list[Star]:
    return find_all_stars()


def retrieve_star(star_id: int) -> Star:
    return find_star(star_id)


def retrieve_star_description(star_id: int) -> dict:
    star = find_star(star_id)
    start_group = find_star_group(star.star_group_id)
    return {
        "star": star.star,
        "type": star.type,
        "group": start_group.group,
        "feature": star.feature,
        "advantage": start_group.advantage,
        "disadvantage": start_group.disadvantage,
        "improvement": start_group.improvement,
    }


def create_ziwei_pan(pan: dict) -> dict:
    palace_maps = pan["palace_maps"]
    pan["palace_maps"] = None 
    pan_object = ZiweiPan(**pan)
    ret_pan = save_ziwei_pan(pan_object, palace_maps)
    pan_object.palace_maps = create_palace_maps(palace_maps)
    return ret_pan


def create_palace_maps(palace_maps: list) -> list[PalacePanMap]:
    new_palace_maps = []
    for palace_map_raw in palace_maps:
        palace_ids = palace_map_raw["stars"]
        palace_map_raw["stars"] = None
        palace_pan_map = PalacePanMap(**palace_map_raw)
        new_stars = []
        for id in palace_ids:
            star = find_star(id)
            new_stars.append(star)
        palace_pan_map.stars = new_stars
        new_palace_maps.append(palace_pan_map)
    return new_palace_maps

def retrieve_all_ziwei_pans():
    return get_all_ziwei_pans()
    

def retrieve_ziwei_pan(ziwei_pan_id: int) -> ZiweiPan:
    return find_ziwei_pan(ziwei_pan_id)


def retrieve_ziwei_pan_palace_stars(ziwei_pan_id: int, position_no: int) -> dict:
    pan = find_ziwei_pan(ziwei_pan_id)
    palace_list = []
    palace_map = pan.palace_maps[position_no]
    star_list = [star.star for star in palace_map.stars]
    return { "position_no": position_no, "palaces": star_list}

def explain_ziwei_pan_ming_palace(ziwei_pan_id: int) -> dict:
    pan = find_ziwei_pan(ziwei_pan_id)
    # palace_id = 0
    stars = get_main_stars_from_palace(pan, 0)
    if not stars:
        # palace_id = 6
        stars = get_main_stars_from_palace(pan, 6)
    # jie star (35) in ming palace (0)
    palace = find_palace(0)
    palace_map = get_palace_pan_map_with_palace_id(pan, 0)
    star = get_star_desc_with_star_id(palace_map, 35)
    if star:
        stars.append(star)
    return {"stars": stars, "Palace": palace.name, "JI desc": palace.ji_desc, "JI action": palace.ji_action}


def explain_ziwei_pan_money_palace(ziwei_pan_id: int) -> dict:
    # palace_id = 4 for money palace and 0 for ming palace
    total_score = calculate_ziwei_pan_money_score(ziwei_pan_id, 4, 0)

    action = ''
    if total_score < 1:
        action = '分数0分及以下，在赚钱上劳心费神，劳多获少，避免创业、高风险投资之外，重视储蓄，避免债务'
    elif total_score < 4:
        action = '分数在1-3分，财运中等，理财能力和赚钱机会也有，但是要伺机而动。可以分为以下两种情况： 如果命宫和财帛宫很干净，少部分一两颗星加分，这种情况可以适度投资，但是需要有自己的主业，还是要赚取所谓的正财。命宫和财帛宫中有财星和吉星，但是被煞星和破财星扣光了，这种情况，同时具备了财星和煞星，财运和理财能力都有，但是要注意守财，避免高风险投资'
    else:
        action = '分数高于4分，正财运比较好，理财能力高，遇到的赚钱机会也高，要多做善事，取财有道'

    # break money stas (31, 32) in ming palace (0) and money palace (4)
    ret_contents = populate_break_money_stars(ziwei_pan_id, 4, 0)
    
    palace = find_palace(4)
    return {"Palace": palace.name, "Desc": palace.ji_desc, "Action": action, "Break Money Stars": ret_contents}


def explain_ziwei_pan_dayun_palace(ziwei_pan_id: int, palace_id: int) -> dict:
    # palace_id is the Palace which digit bucket belong to current age and
    # the associated palace_id is (palace_id + 5) mod 12
    second_palace_id = (palace_id + 5) % 12
    total_score = calculate_ziwei_pan_money_score(ziwei_pan_id, second_palace_id, palace_id)

    action = ''
    if total_score < 1:
        action = '分数0分及以下，在赚钱上劳心费神，劳多获少，避免创业、高风险投资之外，重视储蓄，避免债务'
    elif total_score < 4:
        action = '分数在1-3分，财运中等，理财能力和赚钱机会也有，但是要伺机而动。可以分为以下两种情况： 如果命宫和财帛宫很干净，少部分一两颗星加分，这种情况可以适度投资，但是需要有自己的主业，还是要赚取所谓的正财。命宫和财帛宫中有财星和吉星，但是被煞星和破财星扣光了，这种情况，同时具备了财星和煞星，财运和理财能力都有，但是要注意守财，避免高风险投资'
    else:
        action = '分数高于4分，正财运比较好，理财能力高，遇到的赚钱机会也高，要多做善事，取财有道'

    # break money stas (31, 32) in ming palace (0) and money palace (4)
    ret_contents = populate_break_money_stars(ziwei_pan_id, second_palace_id, palace_id)
    
    palace = find_palace(palace_id)
    return {"Palace": palace.name + "(大运)", "Desc": palace.ji_desc, "Action": action, "Break Money Stars": ret_contents}


def populate_break_money_stars(ziwei_pan_id: ZiweiPan, first_palace_id: int, second_palace_id: int) -> list:
    pan = find_ziwei_pan(ziwei_pan_id)
    ret_contents = []
    palace_map0 = get_palace_pan_map_with_palace_id(pan, second_palace_id)
    palace_map4 = get_palace_pan_map_with_palace_id(pan, first_palace_id)
    prepare_star_feature(ret_contents, palace_map0, 31)
    prepare_star_feature(ret_contents, palace_map0, 32)
    prepare_star_feature(ret_contents, palace_map4, 31)
    prepare_star_feature(ret_contents, palace_map4, 32)
    return ret_contents
    

def calculate_ziwei_pan_money_score(ziwei_pan_id: int, first_palace_id: int, second_palace_id: int) -> dict:
    # first_palace_id should be the Money Palace or Da Yun Palace
    pan = find_ziwei_pan(ziwei_pan_id)
    total_score = 0
    palace_map4 = get_palace_pan_map_with_palace_id(pan, first_palace_id)
    stars = palace_map4.stars
    total_score += calculate_stars_scrores(stars)
    palace_map0 = get_palace_pan_map_with_palace_id(pan, second_palace_id)
    stars = palace_map0.stars
    total_score += calculate_stars_scrores(stars)
    return total_score



def prepare_star_feature(ret_contents: dict, palace_map: PalacePanMap, star_id: int) -> dict:
    ret_record = {}
    if star := get_star_with_star_id(palace_map, star_id):
        ret_record["star"] = star.star
        ret_record["feature"] = star.feature
    if ret_record:
        ret_contents.append(ret_record)
    return ret_record


def calculate_stars_scrores(stars: list) -> int:
    return sum(star.money_score for star in stars)


def get_main_stars_from_palace(pan: ZiweiPan, palace_id: int) -> list:
    for palace_map in pan.palace_maps:
        if palace_map.palace_id == palace_id:
            return get_stars_with_type(palace_map.stars, "main")
    

def get_stars_with_type(stars: list, type: str) -> list:
    return [retrieve_star_description(star.star_id) for star in stars if star.type == type]


def get_palace_pan_map_with_palace_id(pan: ZiweiPan, palace_id: int) -> PalacePanMap:
    for palace_map in pan.palace_maps:
        if palace_map.palace_id == palace_id:
            return palace_map


def get_star_with_star_id(palace_map: PalacePanMap, star_id: int) -> Star:
    for star in palace_map.stars:
        if star.star_id == star_id:
            return star


def get_star_desc_with_star_id(palace_map: PalacePanMap, star_id: int) -> dict:
    return [retrieve_star_description(star.star_id) for star in palace_map.stars if star.star_id == star_id]

