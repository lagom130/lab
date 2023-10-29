package io.github.lagom130.lab.service;

import io.github.lagom130.lab.dto.ApplyDto;
import io.github.lagom130.lab.entity.Apply;
import com.baomidou.mybatisplus.extension.service.IService;
import io.github.lagom130.lab.vo.ApplyListVo;
import io.github.lagom130.lab.vo.ApplyVo;

import java.util.List;

/**
 * <p>
 *  服务类
 * </p>
 *
 * @author lagom
 * @since 2023-10-26
 */
public interface IApplyService extends IService<Apply> {

    Long apply(ApplyDto applyDto);

    ApplyVo getOneById(Long id);
    List<ApplyListVo> getPage(Integer page, Integer size);
}
