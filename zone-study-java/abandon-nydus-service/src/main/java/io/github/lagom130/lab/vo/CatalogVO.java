package io.github.lagom130.lab.vo;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler;
import io.github.lagom130.lab.entity.CatalogDetail;
import io.github.lagom130.lab.enums.CatalogTypeEnum;

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
public class CatalogVO {

    private Long id;

    private String name;

    private String code;

    private Long groupId;

    private Long orgId;

    private String orgName;

    private Long createUser;

    private String createUsername;

    private LocalDateTime createdTime;

    private LocalDateTime updatedTime;

    private Boolean released;

    private Boolean auditing;

    private CatalogDetail detail;

    private LocalDateTime auditFinishedTime;

    private Integer auditWorkDays;

    private CatalogTypeEnum catalogType;
}
