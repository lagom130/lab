package io.github.lagom130.lab.old.service;

import io.github.lagom130.lab.old.dto.ApplyDTO;
import io.github.lagom130.lab.old.dto.AuditDTO;
import io.github.lagom130.lab.entity.Apply;
import io.github.lagom130.lab.entity.Audit;
import io.github.lagom130.lab.entity.FlowItem;
import org.springframework.beans.BeanUtils;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.UUID;
import java.util.stream.Collectors;

/**
 * @author lujc
 * @date 2023/10/23.
 */
@Service
public class ApplyService {

    @Transactional
    public String apply(ApplyDTO applyDTO) {
        // TODO:check
        Apply apply = new Apply();
        BeanUtils.copyProperties(applyDTO, apply);
        apply.setCode(UUID.randomUUID().toString());
        // TODO: save
        FlowItem flowItem = apply.getFlow().get(0);
        List<Audit> audits = flowItem.getAuditorIds().stream().map(auditorId -> {
            Audit audit = new Audit();
            audit.setApplyId(apply.getId());
            audit.setOrder(flowItem.getOrder());
            audit.setCondition(apply.getCondition());
            audit.setOperatorId(auditorId);
            return audit;
        }).collect(Collectors.toList());
        // TODO: save
        return apply.getCode();
    }

    public void audit(String code, AuditDTO auditDTO) {
        //TODO: get Apply
        Apply apply = new Apply();
        // TODO:
        List<Audit> audits = new ArrayList<>();
        // TODO:
        Audit thisAudit = new Audit();
        thisAudit.setPass(auditDTO.getPass());
        // save
        int analysisResult = this.analysis(thisAudit.getCondition(), audits.stream().map(Audit::getPass).collect(Collectors.toList()));
        switch (analysisResult) {
            case 1:
                // TODO:
                break;
            case -1:
                // TODO:
                break;
            case 0:
            default:
                break;
        }
    }

    private int analysis(String condition, List<Boolean> passList) {
        return switch (condition) {
            case "ANY":
                if (passList.stream().anyMatch(pass -> pass!=null && pass)) {
                    yield 1;
                } else if(passList.stream().noneMatch(Objects::isNull)) {
                    yield -1;
                }
                yield 0;
            case "ALL":
                if (passList.stream().allMatch(pass -> pass!=null && pass)) {
                    yield 1;
                } else if(passList.stream().anyMatch(pass -> pass!=null && !pass)) {
                    yield -1;
                }
                yield 0;
            case "HALF":
                int size = passList.size();
                if (passList.stream().filter(pass -> pass!=null && pass).count()>=size/2) {
                    yield 1;
                } else if(passList.stream().filter(pass -> pass!=null && !pass).count()>size/2) {
                    yield -1;
                }
                yield 0;
            default:
                yield 0;
        };
    }
}
