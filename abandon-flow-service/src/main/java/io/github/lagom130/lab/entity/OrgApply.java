package io.github.lagom130.lab.entity;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableName;
import com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler;
import io.github.lagom130.lab.enums.ApplyStatusEnum;

import java.io.Serializable;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

/**
 * <p>
 *
 * </p>
 *
 * @author lagom
 * @since 2023-10-26
 */
@lombok.Data
@TableName(value = "org_apply", autoResultMap = true)
public class OrgApply implements Serializable {

    private static final long serialVersionUID = 1L;

    private Long id;

    private Long applyUser;

    private String applyUsername;

    private Long applyOrg;

    private String applyOrgName;

    private LocalDateTime appliedTime;

    private String service;

    private String bizType;

    @TableField(typeHandler = JacksonTypeHandler.class)
    private List<OrgApplySlot> slots;
    @TableField(typeHandler = JacksonTypeHandler.class)
    private Map<String, Object> detail;
    
    private Integer nowPointer;
    private ApplyStatusEnum status;

    private LocalDateTime finishedTime;
}
