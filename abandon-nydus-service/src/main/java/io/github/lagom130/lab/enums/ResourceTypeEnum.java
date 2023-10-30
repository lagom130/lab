package io.github.lagom130.lab.enums;

import com.baomidou.mybatisplus.annotation.EnumValue;

/**
 * @author lujc
 * @date 2023/10/27.
 */
public enum ResourceTypeEnum implements IBaseEnum<Integer>{
    TABLE(1, "库表"),
    FILE(2, "文件"),
    API(3, "接口");

    @EnumValue
    private Integer code;
    private String desc;

    ResourceTypeEnum(Integer code, String desc) {
        this.init(code, desc);
    }
}
