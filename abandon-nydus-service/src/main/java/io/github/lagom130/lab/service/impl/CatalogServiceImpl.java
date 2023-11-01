package io.github.lagom130.lab.service.impl;

import io.github.lagom130.lab.client.MetaClient;
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
import io.github.lagom130.lab.util.Assert;
import io.github.lagom130.lab.vo.CatalogVO;
import jakarta.annotation.Resource;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

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
        Assert.isTrue(catalogGroup, Assert::isNotNull, () -> new BizException(400, "catalog group not found"));
        catalog.setGroupIds(catalogGroup.getPids()+","+catalogGroup.getId());
        catalog.setRegionCode(catalogGroup.getRegionCode());
        catalog.setId(metaClient.getSnowflakeId());
        this.save(catalog);
        return catalog.getId();
    }

    @Override
    public void updateOne(Long id, CatalogDTO dto) {
        Catalog catalog = this.getById(id);
        Assert.isTrue(catalog, Assert::isNotNull, () -> new BizException(400, "catalog not found"));
        BeanUtils.copyProperties(dto, catalog);
        catalog.setUpdatedTime(LocalDateTime.now());
        this.updateById(catalog);
    }

    @Override
    public void deleteOne(Long id) {
        Catalog catalog = this.getById(id);
        Assert.isTrue(catalog, Assert::isNotNull, () -> new BizException(400, "catalog not found"));
        this.removeById(catalog);
    }

    @Override
    public CatalogVO getOne(Long id) {
        Catalog catalog = this.getById(id);
        Assert.isTrue(catalog, Assert::isNotNull, () -> new BizException(400, "catalog not found"));
        CatalogVO catalogVO = new CatalogVO();
        BeanUtils.copyProperties(catalog, catalogVO);
        return catalogVO;
    }
}
