package io.github.lagom130.lab.dto;

import io.github.lagom130.lab.enums.AuditTypeEnum;

import java.time.LocalDateTime;

@lombok.Data
public class AuditDto {
    private Long operatorUser;

    private String operatorUsername;

    private Boolean pass;

    private String remark;

    private LocalDateTime operatedTime;
}
