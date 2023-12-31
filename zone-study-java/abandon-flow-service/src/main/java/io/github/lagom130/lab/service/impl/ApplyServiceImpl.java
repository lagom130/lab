package io.github.lagom130.lab.service.impl;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import io.github.lagom130.lab.client.MetaClient;
import io.github.lagom130.lab.dto.ApplyDto;
import io.github.lagom130.lab.entity.Apply;
import io.github.lagom130.lab.entity.ApplySlot;
import io.github.lagom130.lab.entity.Audit;
import io.github.lagom130.lab.enums.ApplyStatusEnum;
import io.github.lagom130.lab.mapper.ApplyMapper;
import io.github.lagom130.lab.service.IApplyService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import io.github.lagom130.lab.service.IAuditService;
import io.github.lagom130.lab.vo.ApplyListVo;
import io.github.lagom130.lab.vo.ApplyVo;
import jakarta.annotation.Resource;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

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
    @Transactional
    public Long apply(ApplyDto applyDto) {
        Apply apply = new Apply();
        BeanUtils.copyProperties(applyDto, apply);
        apply.setStatus(ApplyStatusEnum.AUDITING);
        if(apply.getAppliedTime() == null) apply.setAppliedTime(LocalDateTime.now());
        apply.setId(metaClient.getSnowflakeId());
        apply.setNowPointer(0);
        List<ApplySlot> slots = apply.getSlots();
        ApplySlot applySlot = slots.get(0);
        List<Audit> audits = applySlot.getAuditors().stream().map(auditor -> {
            Audit audit = new Audit();
            audit.setApplyId(apply.getId());
            audit.setBizType(apply.getBizType());
            audit.setType(applySlot.getType());
            audit.setAuditOrder(applySlot.getAuditOrder());
            audit.setOperatorUser(auditor.getUserId());
            audit.setOperatorUsername(auditor.getUsername());
            audit.setId(metaClient.getSnowflakeId());
            return audit;
        }).collect(Collectors.toList());
        this.save(apply);
        auditService.saveBatch(audits);
        return apply.getId();
    }

    @Override
    public ApplyVo getOneById(Long id) {
        Apply apply = this.getById(id);
        return new ApplyVo(apply);
    }

    @Override
    public List<ApplyListVo> getPage(Integer page, Integer size) {
        return this.lambdaQuery().select(Apply::getId, Apply::getApplyUsername, Apply::getAppliedTime, Apply::getStatus)
                .list(new Page<>(page, size)).stream().map(ApplyListVo::new).collect(Collectors.toList());
    }
}
