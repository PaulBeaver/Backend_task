# import copy
# import pytest
# from app.db import async_session_maker
# from app.crud import your_crud
# from app.schemas import your_crud
#
#
# @pytest.mark.asyncio
# async def test_get_paginated():
#     objs = [your_crud(**data) for data in JSON_LIST]
#     async with async_session_maker() as db_session:
#         await your_crud.batch_create(db_session, obj)
#
#         page_1 = await your_crud.get_paginated(db_session, page=1, page_size=2)
#         assert len(page_1) == 2 and isinstance(page_1[0], your_crud)
#
#         page_2 = await your_crud.get_paginated(db_session, page=2, page_size=2)
#         assert len(page_2) == 2 and isinstance(page_1[0], your_crud)
