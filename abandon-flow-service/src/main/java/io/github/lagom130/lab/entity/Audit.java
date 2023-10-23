package io.github.lagom130.lab.entity;

import java.time.LocalDateTime;

/**
 * @author lujc
 * @date 2023/10/23.
 */
@lombok.Data
public class Audit {
    private Integer id;
    private Integer applyId;

    private Integer order;

    /**
     * ALL|ANY|HALF
     */
    private String condition;
    private String operatorId;

    private Boolean pass;

    private LocalDateTime operateTime;
}
