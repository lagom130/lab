package io.github.lagom130.lab.entity;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler;
import io.github.lagom130.lab.enums.ApplyStatusEnum;

import java.io.Serializable;
import java.time.LocalDateTime;
import java.util.List;

/**
 * <p>
 * 
 * </p>
 *
 * @author lagom
 * @since 2023-10-26
 */
@lombok.Data
public class Apply implements Serializable {

    private static final long serialVersionUID = 1L;

    private Long id;

    private Long applyUser;

    private Long applyUsername;

    private LocalDateTime appliedTime;

    private String service;

    private String bizType;

    @TableField(typeHandler = JacksonTypeHandler.class)
    private List<ApplySlot> slots;

    private Integer nowPointer;
    private ApplyStatusEnum status;

    private LocalDateTime finishedTime;
}
