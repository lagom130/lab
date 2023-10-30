package io.github.lagom130.lab.entity;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler;
import io.github.lagom130.lab.enums.ResourceTypeEnum;

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
public class ResourceApply implements Serializable {

    private static final long serialVersionUID = 1L;

    private Long id;

    private String code;

    private Long resourceId;

    private Long orgId;

    private String orgName;

    private Long createUser;

    private String createUsername;

    private LocalDateTime createdTime;

    private LocalDateTime updatedTime;

    private Boolean status;

    private Boolean auditing;

    @TableField(typeHandler = JacksonTypeHandler.class)
    private ApplyDetail detail;

    private Long flowId;

    private LocalDateTime auditFinishedTime;

    private Integer auditWorkDays;

    private String resourceName;

    private ResourceTypeEnum resourceType;
}
