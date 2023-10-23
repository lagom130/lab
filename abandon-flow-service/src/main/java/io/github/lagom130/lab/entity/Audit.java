package io.github.lagom130.lab.entity;

import java.time.LocalDateTime;

/**
 * @author lujc
 * @date 2023/10/23.
 */
public class Audit {
    private Integer id;
    private String applyId;

    private Integer order;

    /**
     * ALL|ANY|MUST
     */
    private String condition;
    private String operatorId;

    private String operateType;

    private LocalDateTime operateTime;
}
