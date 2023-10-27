package io.github.lagom130.lab.service;

import io.github.lagom130.lab.dto.ApplyDto;
import io.github.lagom130.lab.entity.Apply;
import com.baomidou.mybatisplus.extension.service.IService;
import org.springframework.beans.BeanUtils;

import java.time.LocalDateTime;

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

}
