package io.github.lagom130.lab.entity;

import io.github.lagom130.lab.enums.AuditTypeEnum;

import java.util.List;

@lombok.Data
public class ApplySlot {
    private int auditOrder;
    private AuditTypeEnum type;

    private List<UserInfo> auditors;
}
