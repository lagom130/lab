package io.github.lagom130.lab.service.impl;

import io.github.lagom130.lab.entity.CatalogGroup;
import io.github.lagom130.lab.mapper.CatalogGroupMapper;
import io.github.lagom130.lab.service.ICatalogGroupService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;

/**
 * <p>
 *  服务实现类
 * </p>
 *
 * @author lagom
 * @since 2023-10-29
 */
@Service
public class CatalogGroupServiceImpl extends ServiceImpl<CatalogGroupMapper, CatalogGroup> implements ICatalogGroupService {

}
