package io.github.lagom130.lab.service.impl;

import io.github.lagom130.lab.entity.Catalog;
import io.github.lagom130.lab.mapper.CatalogMapper;
import io.github.lagom130.lab.service.ICatalogService;
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
public class CatalogServiceImpl extends ServiceImpl<CatalogMapper, Catalog> implements ICatalogService {

}
