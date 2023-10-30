package io.github.lagom130.lab.controller;

import io.github.lagom130.lab.service.ICatalogService;
import jakarta.annotation.Resource;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RestController;

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
    private ICatalogService catalogService;
}
