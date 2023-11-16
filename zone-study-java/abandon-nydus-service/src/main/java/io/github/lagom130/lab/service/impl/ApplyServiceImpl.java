package io.github.lagom130.lab.service.impl;

import io.github.lagom130.lab.entity.ResourceApply;
import io.github.lagom130.lab.mapper.ApplyMapper;
import io.github.lagom130.lab.service.IApplyService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;

/**
 * <p>
 *  服务实现类
 * </p>
 *
 * @author lagom
 * @since 2023-10-29
 */
@Service
public class ApplyServiceImpl extends ServiceImpl<ApplyMapper, ResourceApply> implements IApplyService {

}
