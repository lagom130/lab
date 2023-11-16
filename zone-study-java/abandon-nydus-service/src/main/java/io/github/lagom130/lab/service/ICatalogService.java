package io.github.lagom130.lab.service;

import io.github.lagom130.lab.dto.CatalogDTO;
import io.github.lagom130.lab.entity.Catalog;
import com.baomidou.mybatisplus.extension.service.IService;
import io.github.lagom130.lab.vo.CatalogVO;

/**
 * <p>
 *  服务类
 * </p>
 *
 * @author lagom
 * @since 2023-10-29
 */
public interface ICatalogService extends IService<Catalog> {
    Long addOne(CatalogDTO dto);
    void updateOne(Long id, CatalogDTO dto);
    void deleteOne(Long id);

    CatalogVO getOne(Long id);

    void release(Long id);
}
