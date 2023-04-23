from typing import List

from pydantic import BaseModel


class StarGroup(BaseModel):
    star_group_id: int
    group: str 
    advantage: str
    disadvantage: str 
    improvement: str

    class Config:
        schema_extra = {"example": {"star_group_id": 0, "group": "john", "advantage": "adv", "disadvantage": "disadv", "improvement": "imp"}}


class Star(BaseModel):
    star_id: int
    star: str 
    type: str
    star_group_id: int 
    feature: str

    class Config:
        schema_extra = {"example": {"star_id": 0, "star": "贪狼", "type": "main", "star_group_id": 0, "feature": "john"}}


class Palace(BaseModel):
    palace_id: int
    name: str 
    ji_desc: str
    ji_action: str

    class Config:
        schema_extra = {"example": {"palace_id": 0, "name": "命宫", "ji_desc": "", "ji_action": ""}}


class PalacePanMap(BaseModel):
    palace_id: int
    stars: List[Star] = None

    class Config:
        schema_extra = {"example": {"palace_id": 0, "star": []}}


class ZiweiPan(BaseModel):
    ziwei_pan_id: int 
    name: str
    lunar_birth_day: str
    current_year: str
    palace_maps: List[PalacePanMap] = None

    class Config:
        schema_extra = {"example": {"ziwei_pan_id": 0, "name": "小明1", "lunar_birth_day": "1980-06-08", "current_year": "2020", "palace_maps": [{"palace_id": 0, "name": "命宫"}]}}

