# coding=utf-8

HOUSEHOLD_TYPE = (
    (1, '城镇户口'),
    (2, '农村户口'),
)

DUTY_TYPE = (
    (0, '无全责'),
    (1, '全责'),
    (2, '主要责任'),
    (3, '次要责任'),
    (4, '平等责任'),
)

DISABILITY_TYPE = (
    ('', '----'),
    (100, '一级'),
    (90, '二级'),
    (80, '三级'),
    (70, '四级'),
    (60, '五级'),
    (50, '六级'),
    (40, '七级'),
    (30, '八级'),
    (20, '九级'),
    (10, '十级'),
)

SEC_DISABILITY_TYPE = (
    ('', '----'),
    (10, '二级'),
    (9, '三级'),
    (8, '四级'),
    (7, '五级'),
    (6, '六级'),
    (5, '七级'),
    (4, '八级'),
    (3, '九级'),
    (2, '十级'),
)

SUPPORTED_TYPE = (
    ('', '----'),
    (1, '父亲'),
    (2, '母亲'),
    (3, '子女'),
    (5, '配偶'),
    (4, '其他'),
)

RELATION_TYPE = (
    ('', '----'),
    (5, '配偶'),
    (6, '兄弟姐妹'),
)
