package io.github.lagom130.lab.controller;

import io.github.lagom130.lab.dto.ApplyDto;
import io.github.lagom130.lab.entity.Apply;
import io.github.lagom130.lab.globalResponse.Result;
import io.github.lagom130.lab.service.IApplyService;
import io.github.lagom130.lab.vo.ApplyListVo;
import io.github.lagom130.lab.vo.ApplyVo;
import jakarta.annotation.Resource;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import org.springframework.web.bind.annotation.*;

import java.util.List;

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
    public Result<Long> apply(@RequestBody @Valid ApplyDto applyDto) {
        return new Result<Long>().success(applyService.apply(applyDto));
    }

    @GetMapping("/{id}")
    public Result<ApplyVo> apply(@NotBlank @PathVariable("id") Long id) {
        return new Result<ApplyVo>().success(applyService.getOneById(id));
    }

    @GetMapping("")
    public Result<List<ApplyListVo>> apply(@RequestParam("page")Integer page, @RequestParam("size")Integer size) {
        return new Result<List<ApplyListVo>>().success(applyService.getPage(page, size));
    }
}
