package io.github.lagom130.lab.vo;

import com.fasterxml.jackson.annotation.JsonFormat;
import io.github.lagom130.lab.entity.ApplySlot;
import io.github.lagom130.lab.enums.ApplyStatusEnum;
import io.github.lagom130.lab.enums.AuditTypeEnum;

import java.time.LocalDateTime;
import java.util.List;

@lombok.Data
public class AuditDetailVo {
    private Long id;

    private Long applyId;
    private Integer auditOrder;

    private AuditTypeEnum type;

    private Long operatorUser;

    private String operatorUsername;

    private Boolean pass;

    private String remark;

    private LocalDateTime operatedTime;

    private Long applyUser;
    private String applyUsername;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss",  timezone = "GMT+8")
    private LocalDateTime appliedTime;
    private String service;
    private String bizType;
    private List<ApplySlot> slots;
    private ApplyStatusEnum status;
    private LocalDateTime finishedTime;
}
