package io.github.lagom130.lab.controller;

import io.github.lagom130.lab.dto.AuditDto;
import io.github.lagom130.lab.globalResponse.Result;
import io.github.lagom130.lab.service.IAuditService;
import io.github.lagom130.lab.vo.ApplyVo;
import io.github.lagom130.lab.vo.AuditDetailVo;
import jakarta.annotation.Resource;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import org.springframework.web.bind.annotation.*;
import org.springframework.stereotype.Controller;

/**
 * <p>
 *  前端控制器
 * </p>
 *
 * @author lagom
 * @since 2023-10-26
 */
@RestController
@RequestMapping("/audits")
public class AuditController {
    @Resource
    private IAuditService auditService;

    @GetMapping("/{id}")
    public Result<AuditDetailVo> auditDetail(@NotBlank @PathVariable("id") Long id) {
        return new Result<AuditDetailVo>().success(auditService.getDetail(id));
    }

    @PostMapping("/{id}")
    public Result<AuditDetailVo> auditDetail(@NotBlank @PathVariable("id") Long id, @Valid @RequestBody AuditDto auditDto) {
        auditService.operate(id, auditDto);
        return new Result<AuditDetailVo>().success();
    }

}
