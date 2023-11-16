package io.github.lagom130.lab.service.impl;

import com.baomidou.mybatisplus.core.conditions.AbstractWrapper;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.toolkit.support.SFunction;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.github.lagom130.lab.bo.CatalogGroupSimpleBO;
import io.github.lagom130.lab.entity.CatalogGroup;
import io.github.lagom130.lab.mapper.CatalogGroupMapper;
import io.github.lagom130.lab.service.ICatalogGroupTreeService;
import io.github.lagom130.lab.util.GzipUtils;
import io.github.lagom130.lab.vo.CatalogGroupNodeVO;
import jakarta.annotation.Resource;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.scheduling.annotation.Async;
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
public class CatalogGroupTreeServiceImpl extends ServiceImpl<CatalogGroupMapper, CatalogGroup> implements ICatalogGroupTreeService {
    @Resource
    private StringRedisTemplate stringRedisTemplate;
    @Resource
    private ObjectMapper objectMapper;

    @Override
    public List<CatalogGroupNodeVO> getTree() {
        String caches = stringRedisTemplate.opsForValue().get("catalog_group:tree");
        if(caches != null) {
            try {
                return objectMapper.readValue(GzipUtils.uncompress(caches), objectMapper.getTypeFactory().constructParametricType(List.class, CatalogGroupNodeVO.class));
            } catch (JsonProcessingException e) {
                throw new RuntimeException(e);
            }
        }
        List<CatalogGroupNodeVO> trees = null;
        synchronized(this) {
            trees = this.getTreeFromDB();
            String treeStr = null;
            try {
                treeStr = objectMapper.writeValueAsString(trees);
            } catch (JsonProcessingException e) {
                throw new RuntimeException(e);
            }
            stringRedisTemplate.opsForValue().set("catalog_group:tree", GzipUtils.compress(treeStr));
            return trees;
        }

    }

    @Override
    @Async
    public void refreshTree() {
        synchronized(this) {
            List<CatalogGroupNodeVO> trees = this.getTreeFromDB();
            String treeStr = null;
            try {
                treeStr = objectMapper.writeValueAsString(trees);
            } catch (JsonProcessingException e) {
                throw new RuntimeException(e);
            }
            stringRedisTemplate.opsForValue().set("catalog_group:tree", GzipUtils.compress(treeStr));
        }
    }

    private List<CatalogGroupNodeVO> getTreeFromDB() {
        Map<Long, List<CatalogGroupSimpleBO>> groupByPid = new HashMap<>();
        AbstractWrapper<CatalogGroup, SFunction<CatalogGroup, ?>, LambdaQueryWrapper<CatalogGroup>> wrapper = this.lambdaQuery()
                .select(CatalogGroup::getId, CatalogGroup::getName, CatalogGroup::getPid).getWrapper();
        this.getBaseMapper().selectList(
                wrapper,
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
            vo.setI(parent.getId());
            vo.setN(parent.getName());
            vo.setC(this.getCatalogGroupChildrenNodes(groupByPid.getOrDefault(parent.getId(), new ArrayList<>()), groupByPid));
            groupByPid.remove(parent.getId());
            return vo;
        }).collect(Collectors.toList());
    }
}
