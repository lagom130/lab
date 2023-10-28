package io.github.lagom130.lab.vo;

import io.github.lagom130.lab.enums.AuditTypeEnum;

import java.time.LocalDateTime;

@lombok.Data
public class AuditDetailVo {
    private Long id;

    private Integer auditOrder;

    private AuditTypeEnum type;

    private Long operatorUser;

    private String operatorUsername;

    private Boolean pass;

    private String remark;

    private LocalDateTime operatedTime;

    private ApplyVo applyVo;
}
