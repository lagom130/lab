package io.github.lagom130.lab.controller;

import io.github.lagom130.lab.client.MetaClient;
import io.github.lagom130.lab.dto.CatalogGroupDto;
import io.github.lagom130.lab.entity.CatalogGroup;
import io.github.lagom130.lab.enums.CatalogTypeEnum;
import io.github.lagom130.lab.globalResponse.Result;
import io.github.lagom130.lab.service.ICatalogGroupService;
import io.github.lagom130.lab.util.SnowFlakeUtil;
import io.github.lagom130.lab.vo.CatalogGroupNodeVO;
import jakarta.annotation.Resource;
import org.apache.http.util.Asserts;
import org.springframework.boot.context.properties.bind.DefaultValue;
import org.springframework.util.NumberUtils;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.*;
import org.springframework.stereotype.Controller;

import java.util.ArrayList;
import java.util.List;

/**
 * <p>
 *  前端控制器
 * </p>
 *
 * @author lagom
 * @since 2023-10-29
 */
@Controller
@RequestMapping("/api/catalogGroup")
public class CatalogGroupController {
    @Resource
    private ICatalogGroupService catalogGroupService;
    @Resource
    private MetaClient metaClient;

    @PostMapping("")
    public Result<Long> addOne(@RequestBody CatalogGroupDto dto) {
        return new Result<Long>().success(catalogGroupService.addOne(dto));
    }

    @PutMapping("")
    public Result<Void> updateOne(@PathVariable("id") Long id, @RequestBody CatalogGroupDto dto) {
        catalogGroupService.updateOne(id, dto);
        return new Result<Void>().success();
    }

    @DeleteMapping("/{id}")
    public Result<Void> deleteOne(@PathVariable("id") Long id) {
        catalogGroupService.deleteOne(id);
        return new Result<Void>().success();
    }

    @GetMapping("/{id}")
    public Result<CatalogGroup> getOne(@PathVariable("id") String idStr) {
        Long id = NumberUtils.parseNumber(idStr, Long.class);
        if(id<0 || id> SnowFlakeUtil.getCurrentMax()) {
            return new Result<CatalogGroup>().success(null);
        }
        return new Result<CatalogGroup>().success(catalogGroupService.getOne(id));
    }

    @GetMapping("/tree")
    public Result<List<CatalogGroupNodeVO>> getTree(@RequestParam("noCaches") @DefaultValue("false") String noCaches) {
        return new Result<List<CatalogGroupNodeVO>>().success(catalogGroupService.getTree(Boolean.parseBoolean(noCaches)));
    }

    @GetMapping("/fake")
    public void fake() {
        String[] tianGan = {"甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"};
        String[] diZhi = {"子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"};
        for (int i = 0; i < 60; i++) {
            String provinceName = tianGan[i % 10] + diZhi[i / 10];
            CatalogGroupDto province = new CatalogGroupDto();
            province.setName(provinceName+"省");
            province.setCode(i<10?"0"+i:""+i);
            province.setPid(null);
            Long provinceId = catalogGroupService.addOne(province);
            List<CatalogGroup> batch = new ArrayList<>();
            for (int j = 0; j < 60; j++) {
                String cityName = tianGan[j % 10] + diZhi[j / 10];
                CatalogGroup city = new CatalogGroup();
                city.setId(metaClient.getSnowflakeId());
                city.setName(cityName+"市");
                city.setCode(province.getCode()+(j<10?"0"+j:""+j));
                city.setPid(provinceId);
                city.setPids(""+provinceId);
                batch.add(city);
                for (int a = 0; a < 60; a++) {
                    String areaName = tianGan[a % 10] + diZhi[a / 10];
                    CatalogGroup area = new CatalogGroup();
                    area.setId(metaClient.getSnowflakeId());
                    area.setName(areaName+"区");
                    area.setCode(city.getCode()+(a<10?"0"+a:""+a));
                    String areaCode = area.getCode();
                    area.setPid(city.getId());
                    area.setPids(city.getPids() + "," + city.getId());
                    area.setRegionCode(areaCode);
                    area.setCatalogType(CatalogTypeEnum.DEPT);
                    batch.add(area);
                    for (int b = 0; b < 60; b++) {
                        String screetName = tianGan[b % 10] + diZhi[b / 10];
                        CatalogGroup street = new CatalogGroup();
                        street.setId(metaClient.getSnowflakeId());
                        street.setName(screetName+"街道");
                        street.setCode(area.getCode()+(b<10?"0"+b:""+b));
                        street.setPid(area.getId());
                        street.setPids(area.getPids() + "," + area.getId());
                        street.setRegionCode(areaCode);
                        street.setCatalogType(CatalogTypeEnum.DEPT);
                        batch.add(street);
                    }
                }
            }
            catalogGroupService.saveBatch(batch);
        }
    }
}
