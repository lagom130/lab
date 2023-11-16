package io.github.lagom130.lab.enums;

import com.baomidou.mybatisplus.annotation.EnumValue;

/**
 * @author lujc
 * @date 2023/10/27.
 */
public enum ApplyStatusEnum implements IBaseEnum<Integer>{
    AUDITING(1, "审核中"),
    PASSED(2, "已通过"),
    REFUSED(99, "已拒绝");

    @EnumValue
    private Integer code;
    private String desc;

    ApplyStatusEnum(Integer code, String desc) {
        this.init(code, desc);
    }
}
