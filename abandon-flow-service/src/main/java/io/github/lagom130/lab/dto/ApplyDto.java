package io.github.lagom130.lab.dto;

import io.github.lagom130.lab.entity.ApplySlot;

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
public class ApplyDto {
    private Long applyUser;

    private String applyUsername;

    private LocalDateTime appliedTime;

    private String service;

    private String bizType;

    private List<ApplySlot> slots;
}
