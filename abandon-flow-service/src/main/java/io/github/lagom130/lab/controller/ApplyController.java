package io.github.lagom130.lab.controller;

import io.github.lagom130.lab.dto.ApplyDto;
import io.github.lagom130.lab.globalResponse.Result;
import io.github.lagom130.lab.service.IApplyService;
import jakarta.annotation.Resource;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * <p>
 *  前端控制器
 * </p>
 *
 * @author lagom
 * @since 2023-10-26
 */
@RestController
@RequestMapping("/apply")
public class ApplyController {
    @Resource
    private IApplyService applyService;

    @PostMapping("")
    public Result<Long> apply(@RequestBody ApplyDto applyDto) {
        return new Result<Long>().success(applyService.apply(applyDto));
    }

}
