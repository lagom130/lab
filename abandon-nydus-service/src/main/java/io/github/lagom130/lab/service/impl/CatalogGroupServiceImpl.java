package io.github.lagom130.lab.service.impl;

import com.baomidou.mybatisplus.core.conditions.AbstractWrapper;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.toolkit.support.SFunction;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.github.lagom130.lab.bo.CatalogGroupSimpleBO;
import io.github.lagom130.lab.client.MetaClient;
import io.github.lagom130.lab.dto.CatalogGroupDTO;
import io.github.lagom130.lab.entity.CatalogGroup;
import io.github.lagom130.lab.mapper.CatalogGroupMapper;
import io.github.lagom130.lab.service.ICatalogGroupService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import io.github.lagom130.lab.service.ICatalogGroupTreeService;
import io.github.lagom130.lab.util.GzipUtils;
import io.github.lagom130.lab.vo.CatalogGroupNodeVO;
import jakarta.annotation.Resource;
import org.springframework.beans.BeanUtils;
import org.springframework.cache.annotation.CacheConfig;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

import java.util.*;
import java.util.stream.Collectors;

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
    @Resource
    private MetaClient metaClient;
    @Resource
    private ObjectMapper objectMapper;
    @Resource
    private ICatalogGroupTreeService treeService;

    @Override
    public Long addOne(CatalogGroupDTO dto) {
        CatalogGroup catalogGroup = new CatalogGroup();
        BeanUtils.copyProperties(dto, catalogGroup);
        catalogGroup.setId(metaClient.getSnowflakeId());
        CatalogGroup parent = this.getById(catalogGroup.getPid());
        if(parent != null) {
            String parentId = parent.getId()+"";
            String parentPids = parent.getPids();
            if(parentPids != null) {
                catalogGroup.setPids(parentPids+","+parentId);
            } else {
                catalogGroup.setPids(parentId);
            }

        }
        this.save(catalogGroup);
        treeService.refreshTree();
        return catalogGroup.getId();
    }

    @Override
    @CacheEvict(key = "'catalog_group:'+ #id")
    public void updateOne(Long id, CatalogGroupDTO dto) {
        CatalogGroup catalogGroup = this.getById(id);
        BeanUtils.copyProperties(dto, catalogGroup);
        catalogGroup.setId(metaClient.getSnowflakeId());
        CatalogGroup parent = this.getById(catalogGroup.getPid());
        List<String> pids = Arrays.stream(parent.getPids().split(",")).collect(Collectors.toList());
        pids.add(parent.getPid()+"");
        catalogGroup.setPids(pids.stream().collect(Collectors.joining(",")));
        this.updateById(catalogGroup);
        treeService.refreshTree();
    }

    @Override
    @CacheEvict(key = "'catalog_group:'+ #id")
    public void deleteOne(Long id) {
        this.removeById(id);
        treeService.refreshTree();
    }

    @Override
    @Cacheable(key = "'catalog_group:'+ #id", sync = true)
    public CatalogGroup getOne(Long id) {
        return this.getById(id);
    }
}
