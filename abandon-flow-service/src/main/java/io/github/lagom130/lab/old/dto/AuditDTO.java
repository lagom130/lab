package io.github.lagom130.lab.old.dto;

import java.time.LocalDateTime;

/**
 * @author lujc
 * @date 2023/10/23.
 */
@lombok.Data
public class AuditDTO {
    private Integer id;
    private String applyId;

    private Boolean pass;

}
