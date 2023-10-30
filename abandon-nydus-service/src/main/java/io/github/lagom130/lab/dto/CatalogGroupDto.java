package io.github.lagom130.lab.dto;

import com.baomidou.mybatisplus.annotation.TableName;
import io.github.lagom130.lab.enums.CatalogTypeEnum;

import java.io.Serializable;

/**
 * <p>
 * 
 * </p>
 *
 * @author lagom
 * @since 2023-10-29
 */
@lombok.Data
public class CatalogGroupDto {

    private Integer name;

    private String code;

    private Long pid;

    private CatalogTypeEnum catalogType;

}
