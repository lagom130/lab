package io.github.lagom130.lab.entity;

import io.github.lagom130.lab.enums.AuditTypeEnum;

import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * <p>
 * 
 * </p>
 *
 * @author lagom
 * @since 2023-10-26
 */
@lombok.Data
public class OrgAudit implements Serializable {

    private static final long serialVersionUID = 1L;

    private Long id;

    private String bizType;

    private Long applyId;

    private Integer auditOrder;

    private AuditTypeEnum type;

    private Long auditOrgId;

    private String auditOrgName;

    private Long operatorUser;

    private String operatorUsername;

    private Boolean pass;

    private String remark;

    private LocalDateTime operatedTime;
}
