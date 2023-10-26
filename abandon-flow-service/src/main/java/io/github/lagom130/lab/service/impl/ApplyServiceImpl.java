package io.github.lagom130.lab.service.impl;

import io.github.lagom130.lab.entity.Apply;
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
 * @since 2023-10-26
 */
@Service
public class ApplyServiceImpl extends ServiceImpl<ApplyMapper, Apply> implements IApplyService {

}
