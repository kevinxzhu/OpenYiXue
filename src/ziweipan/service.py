from fastapi import APIRouter, Path, HTTPException, status
from ziweipan.model import StarGroup, Star, Palace, ZiweiPan, PalacePanMap
from ziweipan.store import save_star_group, get_all_star_groups, find_star_group, get_all_stars, find_star, save_ziwei_pan, get_all_ziwei_pans, find_ziwei_pan


def retrieve_all_star_groups() -> list[StarGroup]:
    return get_all_star_groups()


def retrieve_star_group(star_group_id: int) -> StarGroup:
    return find_star_group(star_group_id)


def create_star_group(group: StarGroup):
    save_star_group(group)
    

def retrieve_all_stars() -> list[Star]:
    return get_all_stars()


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
    pan_object.palace_maps = create_palace_maps(palace_maps, ret_pan["ziwei_pan_id"])
    return ret_pan


def create_palace_maps(palace_maps: list, ziwei_pan_id: int) -> list[PalacePanMap]:
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
        palace_pan_map.ziwei_pan_id = ziwei_pan_id
        new_palace_maps.append(palace_pan_map)
    return new_palace_maps

def retrieve_all_ziwei_pans():
    return get_all_ziwei_pans()
    

def retrieve_ziwei_pan(ziwei_pan_id: int) -> ZiweiPan:
    return find_ziwei_pan(ziwei_pan_id)


def retrieve_ziwei_pan_position_palace(ziwei_pan_id: int, position_no: int) -> dict:
    pan = find_ziwei_pan(ziwei_pan_id)
    palace_list = []
    palace_map = pan.palace_maps[position_no]
    star_list = [star.star for star in palace_map.stars]
    return { "position_no": position_no, "palaces": star_list}

def explain_ziwei_pan_ming_palace(ziwei_pan_id: int) -> dict:
    pan = find_ziwei_pan(ziwei_pan_id)
    # palace_id = 0
    stars = find_main_stars_from_palace(pan, 0)
    if not stars:
        # palace_id = 6
        stars = find_main_stars_from_palace(pan, 6)
    return {"stars": stars}


def find_main_stars_from_palace(pan: ZiweiPan, palace_id: int) -> dict:
    for palace_map in pan.palace_maps:
        if palace_map.palace_id == palace_id:
            return find_stars_with_type(palace_map.stars, "main")
    

def find_stars_with_type(stars: list, type: str) -> list:
    return [retrieve_star_description(star.star_id) for star in stars if star.type == type]