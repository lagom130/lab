package io.github.lagom130.lab.service;

import io.github.lagom130.lab.dto.AuditDto;
import io.github.lagom130.lab.entity.Audit;
import com.baomidou.mybatisplus.extension.service.IService;
import io.github.lagom130.lab.vo.AuditDetailVo;

/**
 * <p>
 *  服务类
 * </p>
 *
 * @author lagom
 * @since 2023-10-26
 */
public interface IAuditService extends IService<Audit> {
    AuditDetailVo getDetail(Long id);

    void operate(Long id, AuditDto auditDto);


}
