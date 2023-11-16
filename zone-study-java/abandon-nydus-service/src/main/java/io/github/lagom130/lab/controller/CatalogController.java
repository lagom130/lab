package io.github.lagom130.lab.controller;

import io.github.lagom130.lab.dto.CatalogDTO;
import io.github.lagom130.lab.globalResponse.Result;
import io.github.lagom130.lab.service.ICatalogService;
import io.github.lagom130.lab.vo.CatalogVO;
import jakarta.annotation.Resource;
import org.springframework.web.bind.annotation.*;

/**
 * <p>
 *  前端控制器
 * </p>
 *
 * @author lagom
 * @since 2023-10-29
 */
@RestController
@RequestMapping("/api/catalog")
public class CatalogController {
    @Resource
    private ICatalogService service;

    @PostMapping("")
    public Result<Long> addOne(@RequestBody CatalogDTO dto) {
        return new Result<Long>().success(service.addOne(dto));
    }

    @GetMapping("/{id}")
    public Result<CatalogVO> getOne(@PathVariable("id") Long id) {
        return new Result<CatalogVO>().success(service.getOne(id));
    }

    @PutMapping("/{id}")
    public Result<Void> updateOne(@PathVariable("id") Long id, @RequestBody CatalogDTO dto) {
        service.updateOne(id, dto);
        return new Result<Void>().success();
    }

    @DeleteMapping("/{id}")
    public Result<Void> deleteOne(@PathVariable("id") Long id) {
        service.deleteOne(id);
        return new Result<Void>().success();
    }
}
