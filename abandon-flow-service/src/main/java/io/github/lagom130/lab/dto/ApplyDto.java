package io.github.lagom130.lab.dto;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler;
import io.github.lagom130.lab.entity.ApplyItem;

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
public class ApplyDto implements Serializable {

    private static final long serialVersionUID = 1L;

    private Long id;

    private Long applyId;

    private LocalDateTime appliedTime;

    private String service;

    private String bizType;

    private Integer status;
    private List<ApplyItem> pipeline;

    private LocalDateTime finishedTime;
}
