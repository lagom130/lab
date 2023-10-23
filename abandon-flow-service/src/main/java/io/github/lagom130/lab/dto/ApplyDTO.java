package io.github.lagom130.lab.dto;

import io.github.lagom130.lab.entity.FlowItem;

import java.time.LocalDateTime;
import java.util.List;

/**
 * @author lujc
 * @date 2023/10/23.
 */
@lombok.Data
public class ApplyDTO {
    private Integer id;
    private String code;
    private String service;
    private String type;
    private String applyId;
    private String condition;
    private List<FlowItem> flow;

    private LocalDateTime applyTime;

    private Integer status;
}
