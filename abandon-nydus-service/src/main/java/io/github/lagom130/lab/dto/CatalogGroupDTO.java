package io.github.lagom130.lab.dto;

import io.github.lagom130.lab.enums.CatalogTypeEnum;

/**
 * <p>
 * 
 * </p>
 *
 * @author lagom
 * @since 2023-10-29
 */
@lombok.Data
public class CatalogGroupDTO {

    private String name;

    private String code;

    private Long pid;

    private CatalogTypeEnum catalogType;

}
