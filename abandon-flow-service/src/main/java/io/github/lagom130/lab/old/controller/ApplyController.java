package io.github.lagom130.lab.old.controller;

import io.github.lagom130.lab.old.dto.ApplyDTO;
import io.github.lagom130.lab.old.dto.AuditDTO;
import io.github.lagom130.lab.globalResponse.Result;
import io.github.lagom130.lab.old.service.ApplyService;
import jakarta.annotation.Resource;
import org.springframework.web.bind.annotation.RestController;

/**
 * @author lujc
 * @date 2023/10/23.
 */
@RestController
public class ApplyController {
    @Resource
    private ApplyService applyService;

    public Result<String> apply(ApplyDTO dto) {
        return new Result<String>().success(applyService.apply(dto));
    }

    public void cancel(ApplyDTO dto) {

    }

    public void audit(AuditDTO dto) {

    }

    public void query(Integer id) {

    }
}
