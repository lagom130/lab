package io.github.lagom130.lab.service.impl;

import io.github.lagom130.lab.dto.AuditDto;
import io.github.lagom130.lab.entity.Audit;
import io.github.lagom130.lab.mapper.AuditMapper;
import io.github.lagom130.lab.service.IAuditService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import io.github.lagom130.lab.vo.AuditDetailVo;
import org.springframework.stereotype.Service;

/**
 * <p>
 *  服务实现类
 * </p>
 *
 * @author lagom
 * @since 2023-10-26
 */
@Service
public class AuditServiceImpl extends ServiceImpl<AuditMapper, Audit> implements IAuditService {

    @Override
    public AuditDetailVo getDetail(Long id) {
        return null;
    }

    @Override
    public void operate(Long id, AuditDto auditDto) {

    }
}
