package io.github.lagom130.lab.enums;

import com.baomidou.mybatisplus.annotation.EnumValue;

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
}
