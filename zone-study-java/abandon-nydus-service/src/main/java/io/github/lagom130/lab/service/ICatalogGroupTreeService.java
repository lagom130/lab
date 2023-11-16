package io.github.lagom130.lab.service;

import com.baomidou.mybatisplus.extension.service.IService;
import io.github.lagom130.lab.dto.CatalogGroupDTO;
import io.github.lagom130.lab.entity.CatalogGroup;
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
public interface ICatalogGroupTreeService extends IService<CatalogGroup> {
    List<CatalogGroupNodeVO> getTree();

    void refreshTree();
}
