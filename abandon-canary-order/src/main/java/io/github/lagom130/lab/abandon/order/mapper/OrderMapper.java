package io.github.lagom130.lab.abandon.order.mapper;

import io.github.lagom130.lab.abandon.order.entity.Order;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;

/**
 * <p>
 *  Mapper 接口
 * </p>
 *
 * @author lagom
 * @since 2023-10-14
 */
@Mapper
public interface OrderMapper extends BaseMapper<Order> {

}
