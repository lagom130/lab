package io.github.lagom130.lab.enums;

import com.baomidou.mybatisplus.annotation.EnumValue;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonValue;
import io.github.lagom130.lab.util.EnumUtils;

import java.util.Arrays;

/**
 * @author lujc
 * @date 2023/10/27.
 */
@lombok.Getter
@lombok.AllArgsConstructor
public enum CatalogTypeEnum{
    DEPT(1, "部门"),
    THEME(2, "主题"),
    BASIC(3, "基础");

    @EnumValue
    @JsonValue
    private Integer code;
    private String desc;
    @JsonCreator
    public static CatalogTypeEnum getByCode(Integer code) {
        return EnumUtils.parse(code, CatalogTypeEnum.class);
    }
}
