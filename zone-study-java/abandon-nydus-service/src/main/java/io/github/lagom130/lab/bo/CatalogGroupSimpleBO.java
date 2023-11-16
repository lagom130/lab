package io.github.lagom130.lab.bo;

import io.github.lagom130.lab.entity.CatalogGroup;

/**
 * @author lujc
 * @date 2023/10/31.
 */
@lombok.Data
@lombok.NoArgsConstructor
@lombok.AllArgsConstructor
public class CatalogGroupSimpleBO {
    private Long id;
    private String name;
    private Long pid;

    public CatalogGroupSimpleBO(CatalogGroup catalogGroup) {
        this.id = catalogGroup.getId();
        this.name = catalogGroup.getName();
        this.pid = catalogGroup.getPid();
    }
}
