package io.github.lagom130.lab.dto;

import io.github.lagom130.lab.enums.AuditTypeEnum;
import jakarta.validation.constraints.NotNull;

import java.time.LocalDateTime;

@lombok.Data
public class AuditDto {
    private Long operatorUser;

    private String operatorUsername;

    @NotNull(message = "操作不允许为空")
    private Boolean pass;

    private String remark;

    private LocalDateTime operatedTime;
}
