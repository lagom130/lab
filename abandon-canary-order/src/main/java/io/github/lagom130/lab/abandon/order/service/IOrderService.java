package io.github.lagom130.lab.abandon.order.service;

import io.github.lagom130.lab.abandon.order.entity.Order;
import com.baomidou.mybatisplus.extension.service.IService;
import io.seata.spring.annotation.GlobalTransactional;

/**
 * <p>
 *  服务类
 * </p>
 *
 * @author lagom
 * @since 2023-10-14
 */
public interface IOrderService extends IService<Order> {

    Order create(String userId, String commodityCode, int orderCount);
}
