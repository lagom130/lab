package io.github.lagom130.lab.entity;

import io.github.lagom130.lab.enums.AuditTypeEnum;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;

import java.util.List;

@lombok.Data
public class ApplySlot {
    private int auditOrder;
    @NotNull(message = "审核类型不允许为空")
    private AuditTypeEnum type;

    @Valid
    @NotEmpty(message = "审核人不允许为空")
    private List<UserInfo> auditors;
}
