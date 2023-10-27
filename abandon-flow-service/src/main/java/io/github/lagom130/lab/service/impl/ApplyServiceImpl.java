package io.github.lagom130.lab.service.impl;

import io.github.lagom130.lab.client.MetaClient;
import io.github.lagom130.lab.dto.ApplyDto;
import io.github.lagom130.lab.entity.Apply;
import io.github.lagom130.lab.entity.ApplySlot;
import io.github.lagom130.lab.entity.Audit;
import io.github.lagom130.lab.enums.ApplyStatusEnum;
import io.github.lagom130.lab.mapper.ApplyMapper;
import io.github.lagom130.lab.mapper.AuditMapper;
import io.github.lagom130.lab.service.IApplyService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import io.github.lagom130.lab.service.IAuditService;
import jakarta.annotation.Resource;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

/**
 * <p>
 *  服务实现类
 * </p>
 *
 * @author lagom
 * @since 2023-10-26
 */
@Service
public class ApplyServiceImpl extends ServiceImpl<ApplyMapper, Apply> implements IApplyService {
    @Resource
    private MetaClient metaClient;
    @Resource
    private IAuditService auditService;
    public Long apply(ApplyDto applyDto) {
        Apply apply = new Apply();
        BeanUtils.copyProperties(applyDto, apply);
        apply.setStatus(ApplyStatusEnum.AUDITING);
        apply.setAppliedTime(LocalDateTime.now());
        apply.setId(metaClient.getSnowflakeId());
        apply.setNowPointer(0);
        List<ApplySlot> slots = apply.getSlots();
        ApplySlot applySlot = slots.get(0);
        List<Audit> audits = applySlot.getAuditors().stream().map(auditor -> {
            Audit audit = new Audit();
            audit.setApplyId(apply.getId());
            audit.setType(applySlot.getType());
            audit.setAuditOrder(applySlot.getAuditOrder());
            audit.setOperatorId(auditor.getUserId());
            audit.setOperatorName(auditor.getUsername());
            audit.setId(metaClient.getSnowflakeId());
            return audit;
        }).collect(Collectors.toList());
        this.save(apply);
        auditService.saveBatch(audits);
        return apply.getId();
    }
}
