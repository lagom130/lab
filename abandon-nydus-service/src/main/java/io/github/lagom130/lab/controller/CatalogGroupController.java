package io.github.lagom130.lab.controller;

import io.github.lagom130.lab.dto.CatalogGroupDto;
import io.github.lagom130.lab.entity.CatalogGroup;
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
}
