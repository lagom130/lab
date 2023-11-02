package io.github.lagom130.lab.client.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

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
@lombok.Builder
@JsonIgnoreProperties(ignoreUnknown = true)
public class ApplyDto {
    private Long applyUser;

    private String applyUsername;

    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss",  timezone = "GMT+8")
    private LocalDateTime appliedTime;

    private String service;

    private String bizType;

    private List<ApplySlot> slots;

    private Map<String, Object> detail;
}
