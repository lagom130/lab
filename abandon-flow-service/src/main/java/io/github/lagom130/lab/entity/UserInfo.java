package io.github.lagom130.lab.entity;

import jakarta.validation.constraints.NotNull;

/**
 * @author lujc
 * @date 2023/10/27.
 */
@lombok.Data
public class UserInfo {
    @NotNull(message = "审核人id不允许为空")
    private Long userId;
    @NotNull(message = "审核人用户名不允许为空")
    private String username;
}
