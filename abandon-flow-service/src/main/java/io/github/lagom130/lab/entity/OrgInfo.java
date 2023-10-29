package io.github.lagom130.lab.entity;

import jakarta.validation.constraints.NotNull;

@lombok.Data
public class OrgInfo {
    @NotNull(message = "审核部门id不允许为空")
    private Long orgId;
    @NotNull(message = "审核部门用户名不允许为空")
    private String orgName;
}
