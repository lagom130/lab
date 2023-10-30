package io.github.lagom130.lab.entity;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler;

import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * <p>
 * 
 * </p>
 *
 * @author lagom
 * @since 2023-10-29
 */
@lombok.Data
public class Resource implements Serializable {

    private static final long serialVersionUID = 1L;

    private Long id;

    private String name;

    private Integer type;

    private Long catalogId;

    private Long orgId;

    private String orgName;

    private Long createUser;

    private String createUsername;

    private LocalDateTime createdTime;

    private LocalDateTime updatedTime;

    private Boolean released;

    private Boolean auditing;

    @TableField(typeHandler = JacksonTypeHandler.class)
    private ResourceDetail detail;

    private Long flowId;

    private LocalDateTime auditFinishedTime;

    private Integer auditWorkDays;
}
