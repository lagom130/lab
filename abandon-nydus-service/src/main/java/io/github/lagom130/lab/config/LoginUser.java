package io.github.lagom130.lab.config;

/**
 * @author lujc
 * @date 2023/10/30.
 */
@lombok.Data
public class LoginUser {
    private Long id;
    private String username;
    private Long orgId;
    private String orgName;
}
