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
 * @since 2023-10-26
 */
@lombok.Data
public class Apply implements Serializable {

    private static final long serialVersionUID = 1L;

      private Long id;

    private Long applyId;

    private LocalDateTime appliedTime;

    private String service;

    private String bizType;

    private Integer status;
    @TableField(typeHandler = JacksonTypeHandler.class)
    private String pipeline;

    private LocalDateTime finishedTime;
}
