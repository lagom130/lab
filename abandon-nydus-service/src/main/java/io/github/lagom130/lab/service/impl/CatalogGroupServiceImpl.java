package io.github.lagom130.lab.service.impl;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.github.lagom130.lab.bo.CatalogGroupSimpleBO;
import io.github.lagom130.lab.client.MetaClient;
import io.github.lagom130.lab.dto.CatalogGroupDto;
import io.github.lagom130.lab.entity.CatalogGroup;
import io.github.lagom130.lab.mapper.CatalogGroupMapper;
import io.github.lagom130.lab.service.ICatalogGroupService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import io.github.lagom130.lab.vo.CatalogGroupNodeVO;
import jakarta.annotation.Resource;
import org.springframework.beans.BeanUtils;
import org.springframework.cache.annotation.CacheConfig;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.CachePut;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.data.redis.cache.RedisCacheManager;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;
import org.springframework.util.StringUtils;

import java.sql.Wrapper;
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
@CacheConfig(cacheNames="catalog_group")
public class CatalogGroupServiceImpl extends ServiceImpl<CatalogGroupMapper, CatalogGroup> implements ICatalogGroupService {
    @Resource
    private MetaClient metaClient;
    @Resource
    private StringRedisTemplate stringRedisTemplate;
    @Resource
    private ObjectMapper objectMapper;

    @Override
    public Long addOne(CatalogGroupDto dto) {
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
        return catalogGroup.getId();
    }

    @Override
    @CacheEvict(key = "'catalog_group::'+ #id")
    public void updateOne(Long id, CatalogGroupDto dto) {
        CatalogGroup catalogGroup = this.getById(id);
        BeanUtils.copyProperties(dto, catalogGroup);
        catalogGroup.setId(metaClient.getSnowflakeId());
        CatalogGroup parent = this.getById(catalogGroup.getPid());
        List<String> pids = Arrays.stream(parent.getPids().split(",")).collect(Collectors.toList());
        pids.add(parent.getPid()+"");
        catalogGroup.setPids(pids.stream().collect(Collectors.joining(",")));
        this.updateById(catalogGroup);
    }

    @Override
    @CacheEvict(key = "'catalog_group::'+ #id")
    public void deleteOne(Long id) {
        this.removeById(id);
    }

    @Override
    @Cacheable(key = "'catalog_group::'+ #id", sync = true)
    public CatalogGroup getOne(Long id) {
        return this.getById(id);
    }

    @Override
    public List<CatalogGroupNodeVO> getTree(boolean noCaches) {
        String caches = stringRedisTemplate.opsForValue().get("catalog_group::tree");
        if(!noCaches && caches != null) {
            try {
                return objectMapper.readValue(caches, objectMapper.getTypeFactory().constructParametricType(List.class, CatalogGroupNodeVO.class));
            } catch (JsonProcessingException e) {
                throw new RuntimeException(e);
            }
        }
        List<CatalogGroupNodeVO> trees = null;
        synchronized(this) {
            if(!noCaches) {
                caches = stringRedisTemplate.opsForValue().get("catalog_group::tree");
                if(caches != null) {
                    try {
                        return objectMapper.readValue(caches, objectMapper.getTypeFactory().constructParametricType(List.class, CatalogGroupNodeVO.class));
                    } catch (JsonProcessingException e) {
                        throw new RuntimeException(e);
                    }
                }
            }
            trees = this.getTree();
            String treeStr = null;
            try {
                treeStr = objectMapper.writeValueAsString(trees);
            } catch (JsonProcessingException e) {
                throw new RuntimeException(e);
            }
            stringRedisTemplate.opsForValue().set("catalog_group::tree", treeStr);
            return trees;
        }

    }

    private List<CatalogGroupNodeVO> getTree() {
        Map<Long, List<CatalogGroupSimpleBO>> groupByPid = new HashMap<>();
        this.getBaseMapper().selectList(
                this.lambdaQuery()
                        .select(CatalogGroup::getId, CatalogGroup::getName, CatalogGroup::getPid),
                resultContext ->{
                    CatalogGroup catalogGroup = resultContext.getResultObject();
                    List<CatalogGroupSimpleBO> groupItem = groupByPid.getOrDefault(catalogGroup.getPid(), new ArrayList<>());
                    groupItem.add(new CatalogGroupSimpleBO(catalogGroup));
                    groupByPid.put(catalogGroup.getPid(), groupItem);
                });
        return this.getCatalogGroupChildrenNodes(groupByPid.get(null), groupByPid);
    }

    private List<CatalogGroupNodeVO> getCatalogGroupChildrenNodes(List<CatalogGroupSimpleBO> boList, Map<Long, List<CatalogGroupSimpleBO>> groupByPid) {
        if(CollectionUtils.isEmpty(boList)) {
            return new ArrayList<>();
        }
        return boList.stream().map(parent -> {
            CatalogGroupNodeVO vo = new CatalogGroupNodeVO();
            vo.setId(parent.getId());
            vo.setName(parent.getName());
            vo.setChildren(this.getCatalogGroupChildrenNodes(groupByPid.getOrDefault(parent.getId(), new ArrayList<>()), groupByPid));
            groupByPid.remove(parent.getId());
            return vo;
        }).collect(Collectors.toList());
    }
}
