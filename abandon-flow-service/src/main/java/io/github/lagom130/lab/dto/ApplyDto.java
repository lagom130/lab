package io.github.lagom130.lab.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonIgnoreType;
import io.github.lagom130.lab.entity.ApplySlot;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;

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
@JsonIgnoreProperties(ignoreUnknown = true)
public class ApplyDto {
    @NotNull(message = "申请人ID不允许为空")
    private Long applyUser;

    @NotNull(message = "申请人用户名不允许为空")
    private String applyUsername;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss",  timezone = "GMT+8")
    private LocalDateTime appliedTime;

    @NotBlank(message = "服务类型不允许为空")
    private String service;

    @NotBlank(message = "业务类型不允许为空")
    private String bizType;

    @Valid
    @NotEmpty(message = "审核流程不允许为空")
    private List<ApplySlot> slots;
}
