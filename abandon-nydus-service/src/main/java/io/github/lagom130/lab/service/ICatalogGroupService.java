package io.github.lagom130.lab.service;

import io.github.lagom130.lab.dto.CatalogGroupDTO;
import io.github.lagom130.lab.entity.CatalogGroup;
import com.baomidou.mybatisplus.extension.service.IService;
import io.github.lagom130.lab.vo.CatalogGroupNodeVO;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * <p>
 *  服务类
 * </p>
 *
 * @author lagom
 * @since 2023-10-29
 */
@Service
public interface ICatalogGroupService extends IService<CatalogGroup> {
    Long addOne(CatalogGroupDTO dto);

    void updateOne(Long id, CatalogGroupDTO dto);

    void deleteOne(Long id);

    CatalogGroup getOne(Long id);
    List<CatalogGroupNodeVO> getTree(boolean noCaches);
}
