package io.github.lagom130.lab.vo;

import com.fasterxml.jackson.annotation.JsonFormat;
import io.github.lagom130.lab.entity.Apply;
import io.github.lagom130.lab.enums.ApplyStatusEnum;
import org.springframework.beans.BeanUtils;

import java.time.LocalDateTime;

@lombok.Data
@lombok.Builder
@lombok.NoArgsConstructor
@lombok.AllArgsConstructor
public class AuditListVo {
    private Long id;
    private String applyUsername;
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss",  timezone = "GMT+8")
    private LocalDateTime appliedTime;
    private ApplyStatusEnum status;

    public AuditListVo(Apply apply) {
        BeanUtils.copyProperties(apply, this);
    }
}
