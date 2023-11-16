package io.github.lagom130.lab.dto;

import io.github.lagom130.lab.entity.CatalogDetail;

/**
 * @author lujc
 * @date 2023/11/1.
 */
@lombok.Data
public class CatalogDTO {
    private String name;

    private String code;

    private Long groupId;

    private CatalogDetail detail;
}
