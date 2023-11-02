package io.github.lagom130.lab.controller;

import io.github.lagom130.lab.globalResponse.Result;
import io.github.lagom130.lab.service.ICatalogGroupTreeService;
import io.github.lagom130.lab.vo.CatalogGroupNodeVO;
import jakarta.annotation.Resource;
import org.springframework.boot.context.properties.bind.DefaultValue;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * @author lujc
 * @date 2023/11/2.
 */
@RestController
@RequestMapping("/api/catalogGroupTree")
public class CatalogGroupTreeController {
    @Resource
    private ICatalogGroupTreeService service;

    @GetMapping("")
    public Result<List<CatalogGroupNodeVO>> getTree() {
        return new Result<List<CatalogGroupNodeVO>>().success(service.getTree());
    }
}
