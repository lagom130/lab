package io.github.lagom130.lab.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import io.github.lagom130.lab.client.MetaClient;
import io.github.lagom130.lab.dto.AuditDto;
import io.github.lagom130.lab.entity.Apply;
import io.github.lagom130.lab.entity.ApplySlot;
import io.github.lagom130.lab.entity.Audit;
import io.github.lagom130.lab.enums.ApplyStatusEnum;
import io.github.lagom130.lab.enums.AuditTypeEnum;
import io.github.lagom130.lab.mapper.AuditMapper;
import io.github.lagom130.lab.service.IApplyService;
import io.github.lagom130.lab.service.IAuditService;
import io.github.lagom130.lab.vo.AuditDetailVo;
import jakarta.annotation.Resource;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Map;
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
public class AuditServiceImpl extends ServiceImpl<AuditMapper, Audit> implements IAuditService {
    @Resource
    private MetaClient metaClient;
    @Resource
    private IApplyService applyService;

    @Override
    public AuditDetailVo getDetail(Long id) {
        return this.baseMapper.getAuditDetail(id);
    }

    @Override
    @Transactional
    public void operate(Long id, AuditDto auditDto) {
        Audit thisAudit = this.getById(id);
        Apply apply = applyService.getById(thisAudit.getApplyId());
        List<Audit> audits = this.lambdaQuery()
                .eq(Audit::getApplyId, apply.getId())
                .eq(Audit::getAuditOrder, thisAudit.getAuditOrder())
                .list();
        Map<Boolean, Long> passGroupCount = audits.stream()
                .filter(audit -> !id.equals(audit.getId()))
                .collect(Collectors.groupingBy(Audit::getPass, Collectors.counting()));
        BeanUtils.copyProperties(auditDto, thisAudit);
        this.save(thisAudit);
        passGroupCount.put(thisAudit.getPass(), passGroupCount.get(thisAudit.getPass())+1);
        int thisAuditSize = apply.getSlots().get(apply.getNowPointer()).getAuditors().size();
        if(AuditTypeEnum.ANY.equals(thisAudit.getType())
                || (AuditTypeEnum.HALF.equals(thisAudit.getType()) && passGroupCount.get(thisAudit.getPass())>= thisAuditSize/2
                || (AuditTypeEnum.ALL.equals(thisAudit.getType()) && passGroupCount.get(thisAudit.getPass()) == thisAuditSize))
        ) {
            if (thisAudit.getPass() == Boolean.TRUE) {
                if (apply.getNowPointer() == apply.getSlots().size() - 1) {
                    apply.setStatus(ApplyStatusEnum.PASSED);
                    apply.setFinishedTime(auditDto.getOperatedTime());
                    // TODO: send msg to biz service
                } else {
                    apply.setNowPointer(apply.getNowPointer() + 1);
                    ApplySlot applySlot = apply.getSlots().get(apply.getNowPointer());
                    List<Audit> nextAudits = applySlot.getAuditors().stream().map(auditor -> {
                        Audit nextAudit = new Audit();
                        nextAudit.setApplyId(apply.getId());
                        nextAudit.setType(applySlot.getType());
                        nextAudit.setAuditOrder(applySlot.getAuditOrder());
                        nextAudit.setOperatorUser(auditor.getUserId());
                        nextAudit.setOperatorUsername(auditor.getUsername());
                        nextAudit.setId(metaClient.getSnowflakeId());
                        return nextAudit;
                    }).collect(Collectors.toList());
                    this.saveBatch(nextAudits);
                }
            } else {
                apply.setStatus(ApplyStatusEnum.REFUSED);
                apply.setFinishedTime(auditDto.getOperatedTime());
                // TODO: send msg to biz service
            }
            //this order is over, unAudits don`t need to operate,so remove them
            this.remove(lambdaQuery()
                    .eq(Audit::getApplyId, apply.getId())
                    .eq(Audit::getAuditOrder, thisAudit.getAuditOrder())
                    .eq(Audit::getPass, null)
            );
            applyService.updateById(apply);
        }
    }
}
