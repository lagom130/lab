package io.github.lagom130.lab.enums;

import com.baomidou.mybatisplus.annotation.EnumValue;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonValue;
import io.github.lagom130.lab.util.EnumUtils;

/**
 * @author lujc
 * @date 2023/10/27.
 */
@lombok.Getter
@lombok.AllArgsConstructor
public enum ResourceTypeEnum{
    TABLE(1, "库表"),
    FILE(2, "文件"),
    API(3, "接口");

    @EnumValue
    @JsonValue
    private Integer code;
    private String desc;
    @JsonCreator
    public static ResourceTypeEnum getByCode(Integer code) {
        return EnumUtils.parse(code, ResourceTypeEnum.class);
    }
}
