# import copy
# import pytest
# from app.db import async_session_maker
# from app.crud import TVOY_CRUD
# from app.schemas import TBOI_SCHEMAS
#
#
# @pytest.mark.asyncio
# async def test_get_paginated():
#     objs = [TBOI_SCHEMAS(**data) for data in JSON_LIST]
#     async with async_session_maker() as db_session:
#         await TVOY_CRUD.batch_create(db_session, obj)
#
#         page_1 = await TVOY_CRUD.get_paginated(db_session, page=1, page_size=2)
#         assert len(page_1) == 2 and isinstance(page_1[0], TBOI_SCHEMAS)
#
#         page_2 = await TVOY_CRUD.get_paginated(db_session, page=2, page_size=2)
#         assert len(page_2) == 2 and isinstance(page_1[0], TBOI_SCHEMAS)
