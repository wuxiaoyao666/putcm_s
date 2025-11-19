from sqlalchemy import func, Column

ListContentLen = 20


def sql_build_start(field, label: str):
    """生成基于html的查询，并得到前 20个有效字符"""
    return func.SUBSTRING(func.REGEXP_REPLACE(field, r'<.*?>', '', 1, "g"), 1, ListContentLen).label(label)
