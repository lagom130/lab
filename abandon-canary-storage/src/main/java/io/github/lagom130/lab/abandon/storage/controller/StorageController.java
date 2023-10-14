package io.github.lagom130.lab.abandon.storage.controller;

import io.github.lagom130.lab.abandon.storage.globalResponse.Result;
import io.github.lagom130.lab.abandon.storage.service.IStorageService;
import jakarta.annotation.Resource;
import org.springframework.web.bind.annotation.*;
import org.springframework.stereotype.Controller;

/**
 * <p>
 *  前端控制器
 * </p>
 *
 * @author lagom
 * @since 2023-10-14
 */
@RestController
@RequestMapping("/storage")
public class StorageController {
    @Resource
    IStorageService service;

    @PostMapping("/{commodityCode}")
    public Result deduct(@PathVariable("commodityCode") String commodityCode,@RequestParam int count) {
        service.deduct(commodityCode, count);
        return new Result<>().success();
    }
}
