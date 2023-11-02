package io.github.lagom130.lab.service.impl;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.github.lagom130.lab.client.FlowClient;
import io.github.lagom130.lab.client.MetaClient;
import io.github.lagom130.lab.client.dto.ApplyDto;
import io.github.lagom130.lab.client.dto.ApplySlot;
import io.github.lagom130.lab.client.dto.UserInfo;
import io.github.lagom130.lab.config.LoginUser;
import io.github.lagom130.lab.config.LoginUserUtils;
import io.github.lagom130.lab.dto.CatalogDTO;
import io.github.lagom130.lab.entity.Catalog;
import io.github.lagom130.lab.entity.CatalogGroup;
import io.github.lagom130.lab.globalResponse.BizException;
import io.github.lagom130.lab.mapper.CatalogGroupMapper;
import io.github.lagom130.lab.mapper.CatalogMapper;
import io.github.lagom130.lab.service.ICatalogService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import io.github.lagom130.lab.util.AssertUtils;
import io.github.lagom130.lab.vo.CatalogVO;
import jakarta.annotation.Resource;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

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
    @Resource
    private CatalogGroupMapper catalogGroupMapper;
    @Resource
    private MetaClient metaClient;
    @Resource
    private FlowClient flowClient;
    @Value("${spring.application.name}")
    private String appName;
    @Resource
    private ObjectMapper objectMapper;

    @Override
    public Long addOne(CatalogDTO dto) {
        LoginUser loginUser = LoginUserUtils.getLoginUser();
        Catalog catalog = new Catalog();
        BeanUtils.copyProperties(dto, catalog);
        catalog.setOrgId(loginUser.getOrgId());
        catalog.setOrgName(loginUser.getOrgName());
        catalog.setCreateUser(loginUser.getId());
        catalog.setCreateUsername(loginUser.getUsername());
        catalog.setCreatedTime(LocalDateTime.now());
        catalog.setUpdatedTime(catalog.getCreatedTime());
        catalog.setReleased(false);
        catalog.setAuditing(false);
        CatalogGroup catalogGroup = catalogGroupMapper.selectById(catalog.getGroupId());
        AssertUtils.isTrue(catalogGroup, AssertUtils::isNotNull, () -> new BizException(400, "catalog group not found"));
        catalog.setGroupIds(catalogGroup.getPids()+","+catalogGroup.getId());
        catalog.setRegionCode(catalogGroup.getRegionCode());
        catalog.setId(metaClient.getSnowflakeId());
        this.save(catalog);
        return catalog.getId();
    }

    @Override
    @CacheEvict(key = "'catalog:'+ #id")
    public void updateOne(Long id, CatalogDTO dto) {
        Catalog catalog = this.getById(id);
        AssertUtils.isTrue(catalog, AssertUtils::isNotNull, () -> new BizException(400, "catalog not found"));
        BeanUtils.copyProperties(dto, catalog);
        catalog.setUpdatedTime(LocalDateTime.now());
        this.updateById(catalog);
    }

    @Override
    @CacheEvict(key = "'catalog:'+ #id")
    public void deleteOne(Long id) {
        Catalog catalog = this.getById(id);
        AssertUtils.isTrue(catalog, AssertUtils::isNotNull, () -> new BizException(400, "catalog not found"));
        this.removeById(catalog);
    }

    @Override
    @Cacheable(key = "'catalog:'+ #id", sync = true)
    public CatalogVO getOne(Long id) {
        Catalog catalog = this.getById(id);
        AssertUtils.isTrue(catalog, AssertUtils::isNotNull, () -> new BizException(400, "catalog not found"));
        CatalogVO catalogVO = new CatalogVO();
        BeanUtils.copyProperties(catalog, catalogVO);
        return catalogVO;
    }

    @Override
    @Transactional // 修改为seata at事务
    public void release(Long id) {
        LoginUser loginUser = LoginUserUtils.getLoginUser();
        Catalog catalog = this.getById(id);
        AssertUtils.isTrue(catalog, AssertUtils::isNotNull, () -> new BizException(400, "catalog not found"));
        List<ApplySlot> slots = new ArrayList<>();
        slots.add(ApplySlot.builder()
                .auditOrder(0)
                .type(ApplySlot.AuditTypeEnum.ALL)
                .auditors(List.of(UserInfo.builder().userId(-1L).username("admin").build()))
                .build());
        try {
            ApplyDto applyDto = ApplyDto.builder()
                    .applyUser(loginUser.getId())
                    .applyUsername(loginUser.getUsername())
                    .appliedTime(LocalDateTime.now())
                    .service(appName)
                    .bizType("catalog_release")
                    .slots(slots)
                    .detail(objectMapper.readValue(objectMapper.writeValueAsString(catalog.getDetail()), Map.class))
                    .build();
            flowClient.apply(applyDto);
            catalog.setAuditing(true);
            this.updateById(catalog);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }

    }
}
