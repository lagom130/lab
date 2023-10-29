package io.github.lagom130.lab.service.impl;

import io.github.lagom130.lab.entity.Resource;
import io.github.lagom130.lab.mapper.ResourceMapper;
import io.github.lagom130.lab.service.IResourceService;
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
public class ResourceServiceImpl extends ServiceImpl<ResourceMapper, Resource> implements IResourceService {

}
