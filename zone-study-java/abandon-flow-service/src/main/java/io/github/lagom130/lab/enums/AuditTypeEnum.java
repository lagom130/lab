package io.github.lagom130.lab.enums;

import com.baomidou.mybatisplus.annotation.EnumValue;

/**
 * @author lujc
 * @date 2023/10/27.
 */
public enum AuditTypeEnum implements IBaseEnum<Integer>{
    ANY(1, "任意"),
    HALF(2, "半数"),
    ALL(3, "全部");

    @EnumValue
    private Integer code;
    private String desc;

    AuditTypeEnum(Integer code, String desc) {
        this.init(code, desc);
    }
}
