package io.github.lagom130.lab.controller;

import io.github.lagom130.lab.globalResponse.Result;
import io.github.lagom130.lab.service.IAuditService;
import io.github.lagom130.lab.vo.ApplyVo;
import io.github.lagom130.lab.vo.AuditDetailVo;
import jakarta.annotation.Resource;
import jakarta.validation.constraints.NotBlank;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.stereotype.Controller;
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
@RequestMapping("/audits")
public class AuditController {
    @Resource
    private IAuditService auditService;

    @GetMapping("/{id}")
    public Result<AuditDetailVo> auditDetail(@NotBlank @PathVariable("id") Long id) {
        return new Result<AuditDetailVo>().success(auditService.getDetail(id));
    }

}
