package io.github.lagom130.lab.client.dto;

/**
 * @author lujc
 * @date 2023/10/27.
 */
@lombok.Data
@lombok.Builder
public class UserInfo {
    private Long userId;
    private String username;
}
