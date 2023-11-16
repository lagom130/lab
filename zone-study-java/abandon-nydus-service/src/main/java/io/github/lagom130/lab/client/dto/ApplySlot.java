package io.github.lagom130.lab.client.dto;

import com.baomidou.mybatisplus.annotation.EnumValue;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonValue;
import io.github.lagom130.lab.enums.ResourceTypeEnum;
import io.github.lagom130.lab.util.EnumUtils;

import java.util.List;

@lombok.Data
@lombok.Builder
public class ApplySlot {
    private int auditOrder;
    private AuditTypeEnum type;

    private List<UserInfo> auditors;
    @lombok.Getter
    @lombok.AllArgsConstructor
    public enum AuditTypeEnum {
        ANY(1, "任意"),
        HALF(2, "半数"),
        ALL(3, "全部");

        @EnumValue
        @JsonValue
        private Integer code;
        private String desc;
        @JsonCreator
        public static ResourceTypeEnum getByCode(Integer code) {
            return EnumUtils.parse(code, ResourceTypeEnum.class);
        }
    }
}
