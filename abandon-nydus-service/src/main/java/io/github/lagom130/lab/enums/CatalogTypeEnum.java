package io.github.lagom130.lab.enums;

import com.baomidou.mybatisplus.annotation.EnumValue;
import com.fasterxml.jackson.annotation.JsonCreator;

/**
 * @author lujc
 * @date 2023/10/27.
 */
public enum CatalogTypeEnum implements IBaseEnum<Integer>{
    DEPT(1, "部门"),
    THEME(2, "主题"),
    BASIC(3, "基础");

    @EnumValue
    private Integer code;
    private String desc;

    CatalogTypeEnum(Integer code, String desc) {
        this.init(code, desc);
    }

    @JsonCreator
    public static CatalogTypeEnum getByCode(Integer code) {
        return IBaseEnum.getByCode(CatalogTypeEnum.class, code);
    }
}
