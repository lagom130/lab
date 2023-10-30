package io.github.lagom130.lab.entity;

import com.baomidou.mybatisplus.annotation.TableName;
import io.github.lagom130.lab.enums.CatalogTypeEnum;

import java.io.Serializable;
import java.util.List;

/**
 * <p>
 * 
 * </p>
 *
 * @author lagom
 * @since 2023-10-29
 */
@lombok.Data
@TableName("catalog_group")
public class CatalogGroup implements Serializable {

    private static final long serialVersionUID = 1L;

    private Long id;

    private Integer name;

    private String code;

    private Long pid;

    private String pids;

    /** dept catalog group need this value */
    private Long deptId;

    private CatalogTypeEnum catalogType;

    private String regionCode;

}
