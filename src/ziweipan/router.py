from fastapi import APIRouter, Path, HTTPException, status
from ziweipan.model import StarGroup, Star, Palace, ZiweiPan
from ziweipan.service import create_star_group, retrieve_all_star_groups, retrieve_star_group, retrieve_all_stars, retrieve_star, retrieve_star, retrieve_star_description, create_ziwei_pan, retrieve_all_ziwei_pans, retrieve_ziwei_pan, retrieve_ziwei_pan_palace_stars, explain_ziwei_pan_ming_palace

router = APIRouter()


@router.get("/star-group", response_model=list[StarGroup])
async def retrieve_groups() -> list[StarGroup]:
    return retrieve_all_star_groups()


@router.get("/star-group/{star_group_id}/_object", response_model=StarGroup)
async def get_single_group(
    star_group_id: int = Path(..., title="The ID of the StarGroup to retrieve.")
) -> StarGroup:
    return retrieve_star_group(star_group_id)


@router.get("/star", response_model=list[Star])
async def retrieve_stars() -> list[Star]:
    return retrieve_all_stars()


@router.get("/star/{star_id}/_object", response_model=Star)
async def get_star(
    star_id: int = Path(..., title="The ID of the Star to retrieve.")
) -> Star:
    return retrieve_star(star_id)


@router.get("/star/{star_id}", response_model=dict)
async def get_star_description(
    star_id: int = Path(..., title="The ID of the Star to retrieve.")
) -> dict:
    return retrieve_star_description(star_id)


@router.post("/ziwei-pan", status_code=201)
async def add_ziwei_pan(pan: dict) -> dict:
    ret_pan = create_ziwei_pan(pan)
    ret_pan["message"] = "ZiweiPan added successfully."
    return ret_pan


@router.get("/ziwei-pan", response_model=list[ZiweiPan])
async def retrieve_ziwei_pans() -> list[ZiweiPan]:
    return retrieve_all_ziwei_pans()

@router.get("/ziwei-pan/{ziwei_pan_id}/_object", response_model=ZiweiPan)
async def get_single_ziweipan(
    ziwei_pan_id: int = Path(..., title="The ID of the Star to retrieve.")
) -> dict:
    return retrieve_ziwei_pan(ziwei_pan_id)


@router.get("/ziwei-pan/{ziwei_pan_id}/position/{position_no}/", response_model=dict)
async def get_ziweipan_palace_stars(
    ziwei_pan_id: int = Path(..., title="The ID of the Star to retrieve."),
    position_no: int = Path(..., title="The position number of the Palace in ziwei_pan.")
) -> dict:
    return retrieve_ziwei_pan_position_palace(ziwei_pan_id, position_no)


@router.get("/ziwei-pan/{ziwei_pan_id}/explain0", response_model=dict)
async def explain_ziweipan_ming_palace(
    ziwei_pan_id: int = Path(..., title="The ID of the Star to retrieve."),
) -> dict:
    return explain_ziwei_pan_ming_palace(ziwei_pan_id)
