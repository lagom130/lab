package io.github.lagom130.lab.vo;

import java.util.List;

/**
 * @author lujc
 * @date 2023/10/31.
 */
@lombok.Data
public class CatalogGroupNodeVO {
    private Long i;
    private String n;
    private List<CatalogGroupNodeVO> c;
}
