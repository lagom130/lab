package io.github.lagom130.lab.vo;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler;
import com.fasterxml.jackson.annotation.JsonFormat;
import io.github.lagom130.lab.entity.Apply;
import io.github.lagom130.lab.entity.ApplySlot;
import io.github.lagom130.lab.enums.ApplyStatusEnum;
import org.springframework.beans.BeanUtils;

import java.io.Serializable;
import java.time.LocalDateTime;
import java.util.List;

@lombok.Data
@lombok.Builder
@lombok.NoArgsConstructor
@lombok.AllArgsConstructor
public class ApplyVo {
    private Long id;
    private Long applyUser;
    private String applyUsername;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss",  timezone = "GMT+8")
    private LocalDateTime appliedTime;
    private String service;
    private String bizType;
    private List<ApplySlot> slots;
    private ApplyStatusEnum status;
    private LocalDateTime finishedTime;

    public ApplyVo(Apply apply) {
        BeanUtils.copyProperties(apply, this);
    }
}
