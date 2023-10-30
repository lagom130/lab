package io.github.lagom130.lab.controller;

import io.github.lagom130.lab.dto.CatalogGroupDto;
import io.github.lagom130.lab.globalResponse.Result;
import io.github.lagom130.lab.service.ICatalogGroupService;
import jakarta.annotation.Resource;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.stereotype.Controller;

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
    public Result<String> addOne(@RequestBody CatalogGroupDto dto) {
        return null;
    }
}
